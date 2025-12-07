"""
core/engine.py
Motor de projeção financeira INTEGRADO com Builders.
Versão 4.0 - FINAL e FUNCIONAL

Processa:
- Gatilhos de contratação do TeamBuilder
- Transições de tier do InfraBuilder  
- Fases de marketing do MarketingBuilder
- Canais diferenciados do ChannelsBuilder
- Todas as colunas necessárias para o Dashboard
"""

from typing import Dict, Any, Optional, List
import pandas as pd
import numpy as np

from .config import ConfigFinanceira


def _safe_div(a: float, b: float, default: float = 0.0) -> float:
    """Divisão segura que retorna um valor padrão em caso de erro ou divisão por zero."""
    try:
        if b == 0 or np.isnan(b) or np.isinf(b):
            return default
        result = a / b
        if np.isnan(result) or np.isinf(result):
            return default
        return result
    except (ZeroDivisionError, TypeError, ValueError):
        return default


class MotorProjecaoFinanceira:
    """
    Motor de projeção mês a mês integrado com builders.
    
    Uso:
        motor = MotorProjecaoFinanceira(config)
        df = motor.executar_projecao(meses=36)
        kpis = motor.calcular_kpis()
    """

    def __init__(self, config: ConfigFinanceira):
        if not isinstance(config, ConfigFinanceira):
            raise TypeError("config deve ser uma instância de ConfigFinanceira")
        
        self.config = config
        self.projecao_df: Optional[pd.DataFrame] = None
        self.kpis: Optional[Dict[str, Any]] = None
        
        # Log de eventos (para auditoria/insights)
        self.eventos: List[Dict] = []

        # 🔥 NOVO: Importe os builders (só carrega se existirem)
        try:
            from .builders.revenue_builder import RevenueBuilder
            self._revenue_builder = RevenueBuilder(config)
            self._has_revenue_builder = True
        except ImportError:
            self._has_revenue_builder = False
        
        try:
            from .builders.channels_builder import ChannelsBuilder
            self._channels_builder = ChannelsBuilder(config)
            self._has_channels_builder = True
        except ImportError:
            self._has_channels_builder = False
        
        try:
            from .builders.capital_builder import CapitalBuilder
            self._capital_builder = CapitalBuilder(config)
            self._has_capital_builder = True
        except ImportError:
            self._has_capital_builder = False
        
        try:
            from .builders.marketing_builder import MarketingBuilder
            self._marketing_builder = MarketingBuilder(config)
            self._has_marketing_builder = True
        except ImportError:
            self._has_marketing_builder = False

    def _registrar_evento(self, mes: int, tipo: str, descricao: str, valor: float = 0):
        """Registra evento para auditoria"""
        self.eventos.append({
            'mes': mes,
            'tipo': tipo,
            'descricao': descricao,
            'valor': valor
        })

    def _processar_gatilhos_contratacao(self, mes: int, metricas: dict):
        """
        Processa gatilhos de contratação do TeamBuilder.
        
        Args:
            mes: Mês atual
            metricas: Dict com mrr, usuarios, lucro, caixa
        """
        if not hasattr(self.config, 'cargos_planejados'):
            return
        
        for cargo in self.config.cargos_planejados:
            if not cargo.ativo and cargo.avaliar_gatilhos(mes, metricas):
                cargo.contratar(mes)
                self._registrar_evento(
                    mes, 
                    'CONTRATACAO',
                    f"Contratado: {cargo.nome} ({cargo.cargo_funcao})",
                    cargo.salario_base
                )

    def _calcular_tier_infraestrutura(self, usuarios: int) -> tuple:
        """
        Calcula tier de infraestrutura baseado em usuários.
        
        Returns:
            (numero_tier, custo_mensal)
        """
        if not hasattr(self.config, 'tiers_infraestrutura'):
            # Fallback: usa lógica antiga
            if usuarios <= self.config.infra_tier1_limite:
                return (1, self.config.infra_tier1_custo_fixo)
            elif usuarios <= self.config.infra_tier2_limite:
                return (2, self.config.infra_tier2_custo_fixo)
            else:
                excedente = max(0, usuarios - self.config.infra_tier2_limite)
                return (3, self.config.infra_tier2_custo_fixo + excedente * self.config.infra_tier3_custo_por_usuario)
        
        # Usa InfraBuilder
        for tier in sorted(self.config.tiers_infraestrutura, key=lambda t: t.numero):
            if tier.limite_usuarios_min <= usuarios <= tier.limite_usuarios_max:
                return (tier.numero, tier.calcular_custo(usuarios))
            elif usuarios > tier.limite_usuarios_max and tier == self.config.tiers_infraestrutura[-1]:
                return (tier.numero, tier.calcular_custo(usuarios))
        
        return (1, 0.0)

    def _calcular_marketing_fase(self, mes: int, mrr: float, lucro_bruto: float, novos_pagantes: float) -> tuple:
        """
        Calcula custo de marketing baseado na fase ativa.
        
        Returns:
            (fase_numero, custo_mensal)
        """
        if not hasattr(self.config, 'fases_marketing'):
            # Fallback: usa lógica antiga
            if mes <= self.config.marketing_fase1_duracao_meses:
                return (1, self.config.marketing_fase1_custo_fixo)
            else:
                return (2, max(0.0, lucro_bruto * self.config.marketing_fase2_perc_lucro_bruto))
        
        # Usa MarketingBuilder
        for fase in self.config.fases_marketing:
            if fase.mes_inicio <= mes and (fase.mes_fim is None or mes <= fase.mes_fim):
                custo = fase.calcular_orcamento(mrr, lucro_bruto, novos_pagantes)
                return (fase.numero, custo)
        
        return (1, 0.0)

    def _calcular_custos_equipe(self, mes: int, metricas: dict) -> tuple:
        """
        Calcula custos de equipe usando TeamBuilder.
        
        Returns:
            (custo_clt, custo_pj, custo_fundador)
        """
        if not hasattr(self.config, 'cargos_planejados'):
            # Fallback: usa lógica antiga do fundador
            saldo_caixa = metricas.get('caixa', 0)
            inicio_ok = mes >= self.config.salario_fundador_mes_inicio_ideal
            caixa_ok = saldo_caixa > self.config.salario_fundador_caixa_minimo_seguranca
            salario_fundador = self.config.salario_fundador_valor if (inicio_ok and caixa_ok) else 0.0
            return (0.0, 0.0, salario_fundador)
        
        custo_clt = 0.0
        custo_pj = 0.0
        custo_fundador = 0.0
        
        for cargo in self.config.cargos_planejados:
            custo = cargo.calcular_custo_mensal(mes, metricas)
            
            if cargo.tipo.value == 'fundador':
                custo_fundador += custo
            elif cargo.tipo.value == 'clt':
                custo_clt += custo
            elif cargo.tipo.value == 'pj':
                custo_pj += custo
        
        return (custo_clt, custo_pj, custo_fundador)

    def _calcular_custos_ferramentas(self, mes: int, num_usuarios: int = 0) -> float:
        """Calcula custo total de ferramentas SaaS usando o método de cada objeto."""
        if not hasattr(self.config, 'ferramentas_saas') or not self.config.ativar_ferramentas:
            return 0.0
        
        custo_total = 0.0
        for ferramenta in self.config.ferramentas_saas:
            # A lógica de cálculo agora está encapsulada no próprio objeto FerramentaSaaS
            custo_total += ferramenta.calcular_custo(mes, num_usuarios)

        return custo_total

    def executar_projecao(self, meses: int = 36) -> pd.DataFrame:
        """
        Executa a projeção financeira mês a mês com integração total dos builders.
        
        Gera TODAS as colunas necessárias para o dashboard.
        """
        cfg = self.config
        
        # Define TODAS as colunas que o dashboard espera
        colunas = [
            # Identificação
            'mes',
            
            # Funil de Aquisição
            'Usuarios_Iniciais', 'Visitantes', 'Novos_Trials', 'Novos_Pagantes',
            'Usuarios_Perdidos', 'Usuarios_Finais',
            
            # Taxas de Conversão (para análise)
            'Taxa_Conv_Trial', 'Taxa_Conv_Pagante', 'Taxa_Conv_Geral',
            
            # Receita
            'MRR', 'ARR', 'ARPU',
            
            # COGS Detalhado
            'Custo_IA', 'Impostos', 'Taxas_Pagamento', 'Comissoes_Afiliados', 'COGS_Total',
            
            # Margens
            'Lucro_Bruto', 'Margem_Bruta_Pct',
            
            # OPEX Detalhado
            'Custo_Infra', 'Tier_Infra',
            'Custo_Marketing', 'Fase_Marketing',
            'Salario_Fundador', 'Custo_Pessoal_CLT', 'Custo_Pessoal_PJ',
            'Custo_Escritorio', 'Custo_Ferramentas', 'Custo_Servicos_Profissionais',
            'Custo_Depreciacao', 'Custo_Despesas_Anuais',
            'OPEX_Total',
            
            # Resultado
            'EBITDA', 'Resultado_Operacional', 'Lucro_Liquido',
            
            # Fluxo de Caixa
            'Aportes', 'Fluxo_Caixa', 'Saldo_Caixa',
            
            # Métricas de Análise
            'CAC_Mensal', 'LTV', 'LTV_CAC_Ratio', 'Payback_Meses',
            
            # Receita Detalhada (para tabelas)
            'Receita_Total', 'Churn_Absoluto'
        ]
        
        registros = []
        
        # Inicializações
        saldo_caixa = float(cfg.capital_inicial_caixa or 0.0)
        visitantes = float(cfg.visitantes_mes_1 or 0.0)
        usuarios = 0.0
        acum_novos_pagantes = 0.0
        acum_marketing = 0.0
        tier_atual = 1
        fase_marketing_atual = 1
        
        # Loop principal
        for mes in range(1, meses + 1):
            
            # ============================================================
            # AQUISIÇÃO E RETENÇÃO
            # ============================================================
            
            if mes > 1:
                visitantes *= (1 + cfg.taxa_crescimento_trafego_mensal)
            
            # Usa taxas médias dos canais (se configurado)
            taxa_conv_trial = cfg.taxa_conversao_visitante_trial
            taxa_conv_pagante = cfg.taxa_conversao_trial_pagante
            
            novos_trials = visitantes * taxa_conv_trial
            novos_pagantes = novos_trials * taxa_conv_pagante
            taxa_conv_geral = taxa_conv_trial * taxa_conv_pagante
            
            usuarios_iniciais = usuarios
            usuarios_perdidos = usuarios * cfg.churn_mensal
            usuarios = max(0.0, usuarios + novos_pagantes - usuarios_perdidos)
            
            # ============================================================
            # RECEITA
            # ============================================================
            
            arpu = cfg.arpu_medio
            mrr = usuarios * arpu
            arr = mrr * 12
            receita_total = mrr  # Pode incluir receita não-recorrente no futuro
            
            # ============================================================
            # COGS DETALHADO
            # ============================================================
            
            custo_ia = usuarios * cfg.custo_ia_por_usuario if cfg.ativar_custo_ia else 0.0
            impostos = mrr * cfg.aliquota_impostos if cfg.ativar_impostos else 0.0
            
            taxas_pagamento = 0.0
            if cfg.ativar_taxas_pgto:
                taxas_pagamento = (novos_pagantes * cfg.taxa_pagamento_fixa_por_transacao) + \
                                 (mrr * cfg.taxa_pagamento_percentual)
            
            comissoes_afiliados = 0.0
            if cfg.ativar_comissoes_afiliado and hasattr(cfg, 'comissao_afiliados') and cfg.comissao_afiliados:
                if mes >= cfg.comissao_afiliados.mes_inicio_programa:
                    comissoes_afiliados = mrr * cfg.comissao_afiliados.percentual_sobre_venda * \
                                         cfg.comissao_afiliados.percentual_vendas_via_afiliados
            
            cogs_total = custo_ia + impostos + taxas_pagamento + comissoes_afiliados
            lucro_bruto = mrr - cogs_total
            margem_bruta_pct = _safe_div(lucro_bruto, mrr, 0.0)
            
            # ============================================================
            # MÉTRICAS PARA GATILHOS
            # ============================================================
            
            metricas = {
                'mrr': mrr,
                'usuarios': usuarios,
                'lucro': lucro_bruto,
                'caixa': saldo_caixa,
                'mes': mes
            }
            
            # ============================================================
            # GATILHOS DE CONTRATAÇÃO
            # ============================================================
            
            self._processar_gatilhos_contratacao(mes, metricas)
            
            # ============================================================
            # OPEX DETALHADO
            # ============================================================
            
            # Infraestrutura (com transição de tier)
            tier_atual, custo_infra = self._calcular_tier_infraestrutura(int(usuarios))
            
            # Marketing (com fases)
            fase_marketing_atual, custo_marketing = self._calcular_marketing_fase(
                mes, mrr, lucro_bruto, novos_pagantes
            )
            
            # Equipe (com gatilhos)
            custo_clt, custo_pj, salario_fundador = self._calcular_custos_equipe(mes, metricas)
            
            # Ferramentas
            custo_ferramentas = self._calcular_custos_ferramentas(mes, int(usuarios))
            
            # Escritório
            custo_escritorio = 0.0
            if cfg.ativar_escritorio and mes >= cfg.escritorio_mes_inicio:
                custo_escritorio = cfg.escritorio_custo_total_mensal
            
            # Serviços Profissionais
            custo_servicos = 0.0
            if cfg.ativar_servicos_profs:
                if mes >= cfg.contabilidade_mes_inicio:
                    custo_servicos += cfg.contabilidade_mensal
                if mes >= cfg.advogado_mes_inicio:
                    custo_servicos += cfg.advogado_retainer_mensal
                custo_servicos += cfg.consultorias_outras_mensal
            
            # Depreciação
            custo_depreciacao = 0.0
            if cfg.ativar_depreciacao:
                for ativo in cfg.ativos_depreciaveis:
                    custo_depreciacao += ativo.calcular_depreciacao_mensal(mes)
            
            # Despesas Anuais
            custo_despesas_anuais = 0.0
            if cfg.ativar_despesas_anuais:
                for desp in cfg.despesas_anuais:
                    if desp.ativo and mes >= desp.mes_inicio:
                        if desp.mes_fim is None or mes <= desp.mes_fim:
                            custo_despesas_anuais += desp.valor_mensal_rateado
            
            opex_total = (
                custo_infra + custo_marketing + salario_fundador +
                custo_clt + custo_pj + custo_escritorio +
                custo_ferramentas + custo_servicos +
                custo_depreciacao + custo_despesas_anuais
            )
            
            # ============================================================
            # RESULTADO E FLUXO DE CAIXA
            # ============================================================
            
            ebitda = lucro_bruto - opex_total
            resultado_operacional = ebitda - custo_depreciacao
            
            # Lucro Líquido (sem impostos sobre lucro por enquanto, pois startups no Simples não pagam IR/CSLL até certo limite)
            lucro_liquido = resultado_operacional
            
            # Aportes
            aporte = cfg.aporte_mensal_fixo if mes <= cfg.meses_aporte_fixo else 0.0
            
            fluxo_caixa = lucro_liquido + aporte
            saldo_caixa += fluxo_caixa
            
            # ============================================================
            # MÉTRICAS DE ANÁLISE
            # ============================================================
            
            cac_mensal = _safe_div(custo_marketing, novos_pagantes, np.nan)
            ltv = cfg.calcular_ltv()
            ltv_cac_ratio = _safe_div(ltv, cac_mensal, np.nan)
            payback_meses = _safe_div(cac_mensal, (lucro_bruto / usuarios if usuarios > 0 else 0), np.nan)
            
            acum_novos_pagantes += novos_pagantes
            acum_marketing += custo_marketing
            
            # ============================================================
            # REGISTRO DO MÊS
            # ============================================================
            
            registros.append({
                'mes': mes,
                'Usuarios_Iniciais': round(usuarios_iniciais, 2),
                'Visitantes': round(visitantes, 0),
                'Novos_Trials': round(novos_trials, 2),
                'Novos_Pagantes': round(novos_pagantes, 2),
                'Usuarios_Perdidos': round(usuarios_perdidos, 2),
                'Usuarios_Finais': round(usuarios, 2),
                'Taxa_Conv_Trial': round(taxa_conv_trial * 100, 2),
                'Taxa_Conv_Pagante': round(taxa_conv_pagante * 100, 2),
                'Taxa_Conv_Geral': round(taxa_conv_geral * 100, 2),
                'MRR': round(mrr, 2),
                'ARR': round(arr, 2),
                'ARPU': round(arpu, 2),
                'Custo_IA': round(custo_ia, 2),
                'Impostos': round(impostos, 2),
                'Taxas_Pagamento': round(taxas_pagamento, 2),
                'Comissoes_Afiliados': round(comissoes_afiliados, 2),
                'COGS_Total': round(cogs_total, 2),
                'Lucro_Bruto': round(lucro_bruto, 2),
                'Margem_Bruta_Pct': round(margem_bruta_pct * 100, 2),
                'Custo_Infra': round(custo_infra, 2),
                'Tier_Infra': tier_atual,
                'Custo_Marketing': round(custo_marketing, 2),
                'Fase_Marketing': fase_marketing_atual,
                'Salario_Fundador': round(salario_fundador, 2),
                'Custo_Pessoal_CLT': round(custo_clt, 2),
                'Custo_Pessoal_PJ': round(custo_pj, 2),
                'Custo_Escritorio': round(custo_escritorio, 2),
                'Custo_Ferramentas': round(custo_ferramentas, 2),
                'Custo_Servicos_Profissionais': round(custo_servicos, 2),
                'Custo_Depreciacao': round(custo_depreciacao, 2),
                'Custo_Despesas_Anuais': round(custo_despesas_anuais, 2),
                'OPEX_Total': round(opex_total, 2),
                'EBITDA': round(ebitda, 2),
                'Resultado_Operacional': round(resultado_operacional, 2),
                'Lucro_Liquido': round(lucro_liquido, 2),
                'Aportes': round(aporte, 2),
                'Fluxo_Caixa': round(fluxo_caixa, 2),
                'Saldo_Caixa': round(saldo_caixa, 2),
                'CAC_Mensal': round(cac_mensal, 2) if not np.isnan(cac_mensal) else np.nan,
                'LTV': round(ltv, 2),
                'LTV_CAC_Ratio': round(ltv_cac_ratio, 2) if not np.isnan(ltv_cac_ratio) else np.nan,
                'Payback_Meses': round(payback_meses, 2) if not np.isnan(payback_meses) else np.nan,
                'Receita_Total': round(receita_total, 2),
                'Churn_Absoluto': round(usuarios_perdidos, 2)
            })
        
        # ============================================================
        # FINALIZAÇÃO
        # ============================================================
        
        df = pd.DataFrame.from_records(registros, columns=colunas)
        df.fillna(value=np.nan, inplace=True)

        # ===== PASSO 2: RevenueBuilder (SEMPRE PRIMEIRO) =====
        # Gera MRR_Lite, MRR_Trader, MRR_Pro, Waterfall
        if self._has_revenue_builder and hasattr(self.config, 'receita'):
            if self.config.receita.get('planos'):
                print("🔧 Aplicando RevenueBuilder...")
                df = self._revenue_builder.gerar_series_temporais(df)
                print(f"   ✅ {len(self.config.receita['planos'])} planos processados")
            else:
                print("⚠️ RevenueBuilder configurado mas sem planos")
        
        # ===== PASSO 3: MarketingBuilder (SE EXISTIR) =====
        # Gera orçamento de marketing para CAC real
        if self._has_marketing_builder:
            print("🔧 Aplicando MarketingBuilder...")
            orcamento_mensal = []
            for mes_iter in range(1, meses + 1):
                # Usa seu método existente
                custo = self._marketing_builder.calcular_custo_para_mes(
                    mes=mes_iter,
                    lucro_bruto=df.loc[mes_iter-1, 'Lucro_Bruto']
                )
                orcamento_mensal.append(custo)
            
            # Salva no DataFrame
            df['Custo_Marketing_Total'] = orcamento_mensal
            print(f"   ✅ Orçamento de marketing calculado")
        
        # ===== PASSO 4: ChannelsBuilder (APÓS MARKETING) =====
        # Gera funil de conversão usando orçamento real
        if self._has_channels_builder and hasattr(self.config, 'canais_aquisicao'):
            if self.config.canais_aquisicao:
                print("🔧 Aplicando ChannelsBuilder...")
                
                # Pegar orçamento do marketing se disponível
                orcamento_series = None
                if 'Custo_Marketing_Total' in df.columns:
                    orcamento_series = df['Custo_Marketing_Total']
                
                df = self._channels_builder.gerar_series_temporais(
                    df,
                    orcamento_mensal=orcamento_series
                )
                print(f"   ✅ {len(self.config.canais_aquisicao)} canais processados")
        
        # ===== PASSO 5: CapitalBuilder (SEMPRE POR ÚLTIMO) =====
        # Gera runway e milestones com todos os dados disponíveis
        if self._has_capital_builder:
            print("🔧 Aplicando CapitalBuilder...")
            df = self._capital_builder.gerar_series_temporais(df)
            print("   ✅ Runway e milestones calculados")
            
        self.projecao_df = df
        
        return df

    def calcular_kpis(self) -> Dict[str, Any]:
        """
        Calcula os KPIs principais a partir do DataFrame de projeção.
        """
        if self.projecao_df is None:
            raise RuntimeError("Execute executar_projecao() antes de calcular_kpis()")
        
        df = self.projecao_df.copy()
        kpis = {}

        # Break-even
        be_df = df[df['Resultado_Operacional'] > 0]
        kpis['Break_Even_Mes'] = int(be_df.iloc[0]['mes']) if not be_df.empty else None

        # Payback
        capital_inicial = abs(self.config.capital_inicial_caixa or 0.0)
        pb_df = df[df['Saldo_Caixa'] > capital_inicial]
        kpis['Payback_Investimento_Mes'] = int(pb_df.iloc[0]['mes']) if not pb_df.empty else None

        # Vale da Morte
        if not df.empty:
            kpis['Vale_da_Morte_Minimo_Caixa'] = float(df['Saldo_Caixa'].min())
            kpis['Vale_da_Morte_Mes'] = int(df.loc[df['Saldo_Caixa'].idxmin(), 'mes'])
        else:
            kpis['Vale_da_Morte_Minimo_Caixa'] = 0.0
            kpis['Vale_da_Morte_Mes'] = 0

        # Runway
        negativo_df = df[df['Saldo_Caixa'] < 0]
        if not negativo_df.empty:
            kpis['Runway_Meses'] = int(negativo_df.iloc[0]['mes'] - 1)
        else:
            kpis['Runway_Meses'] = f">= {len(df)}"

        # Unit Economics
        kpis['LTV_Final'] = float(self.config.calcular_ltv())
        total_marketing = df['Custo_Marketing'].sum()
        total_novos = df['Novos_Pagantes'].sum()
        kpis['CAC_Medio_Periodo'] = float(_safe_div(total_marketing, total_novos, np.nan))
        kpis['LTV_CAC_Ratio_Final'] = float(_safe_div(kpis['LTV_Final'], kpis['CAC_Medio_Periodo'], np.nan))
        kpis['CAC_Payback_Meses_Config'] = float(self.config.calcular_cac_payback_meses())

        # Snapshots Anuais
        for ano in [1, 2, 3]:
            mes_final_ano = ano * 12
            if len(df) >= mes_final_ano:
                kpis[f'MRR_Ano{ano}'] = float(df.iloc[mes_final_ano - 1]['MRR'])
                kpis[f'Usuarios_Ano{ano}'] = float(df.iloc[mes_final_ano - 1]['Usuarios_Finais'])

        kpis['Saldo_Caixa_Final'] = float(df.iloc[-1]['Saldo_Caixa']) if not df.empty else 0.0
        kpis['MRR_Final'] = float(df.iloc[-1]['MRR']) if not df.empty else 0.0
        kpis['Usuarios_Final'] = float(df.iloc[-1]['Usuarios_Finais']) if not df.empty else 0.0
        
        # Eventos de auditoria
        kpis['eventos'] = self.eventos
        
        self.kpis = kpis
        return kpis

    def obter_eventos_mes(self, mes: int) -> List[Dict]:
        """Retorna eventos que ocorreram em um mês específico"""
        return [e for e in self.eventos if e['mes'] == mes]

    def verificar_builders_ativos(self) -> dict:
        """
        Retorna status dos builders para o dashboard
        """
        return {
            'RevenueBuilder': self._has_revenue_builder and hasattr(self.config, 'receita') and self.config.receita.get('planos'),
            'ChannelsBuilder': self._has_channels_builder and hasattr(self.config, 'canais_aquisicao'),
            'CapitalBuilder': self._has_capital_builder,
            'MarketingBuilder': self._has_marketing_builder,
        }


# Função procedural para retrocompatibilidade
def gerar_projecao_financeira(premissas: Dict[str, Any], meses: int = 36) -> pd.DataFrame:
    """
    Função procedural para retrocompatibilidade.
    """
    cfg = ConfigFinanceira()
    for k, v in premissas.items():
        if hasattr(cfg, k):
            try:
                setattr(cfg, k, v)
            except Exception:
                pass
    
    motor = MotorProjecaoFinanceira(cfg)
    df = motor.executar_projecao(meses=meses)
    return df