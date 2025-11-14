"""
core/engine.py
Motor de projeção financeira consolidado para SAM.

Contém:
- MotorProjecaoFinanceira (classe com métodos completos)
- gerar_projecao_financeira (função procedural compatível)
"""

from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
from .config import ConfigFinanceira

def _safe_div(a: float, b: float, default: float = 0.0) -> float:
    try:
        if b == 0 or np.isnan(b):
            return default
        return a / b
    except Exception:
        return default


class MotorProjecaoFinanceira:
    """
    Motor de projeção mês a mês. Instanciar com uma ConfigFinanceira.
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

    # --- lógica de custo infra (mesma assinatura que seu config espera) ---
    def calcular_custo_infraestrutura(self, usuarios: int) -> float:
        cfg = self.config
        if usuarios <= cfg.infra_tier1_limite:
            return cfg.infra_tier1_custo_fixo if cfg.ativar_infra_tier1 else 0.0
        elif usuarios <= cfg.infra_tier2_limite:
            return cfg.infra_tier2_custo_fixo if cfg.ativar_infra_tier2 else 0.0
        else:
            if not cfg.ativar_infra_tier3:
                return 0.0
            adicionais = max(0, usuarios - cfg.infra_tier2_limite)
            return cfg.infra_tier2_custo_fixo + adicionais * cfg.infra_tier3_custo_por_usuario

    def calcular_custo_marketing(self, mes: int, lucro_bruto: float) -> float:
        cfg = self.config
        if not cfg.ativar_marketing:
            return 0.0
        if mes <= cfg.marketing_fase1_duracao_meses:
            return cfg.marketing_fase1_custo_fixo
        # fase 2: % sobre lucro bruto (não negativo)
        return max(0.0, lucro_bruto * cfg.marketing_fase2_perc_lucro_bruto)

    def calcular_salario_fundador(self, mes: int, saldo_caixa_anterior: float) -> float:
        cfg = self.config
        if not cfg.ativar_fundador:
            return 0.0
        inicio_ok = mes >= cfg.salario_fundador_mes_inicio_ideal
        caixa_ok = saldo_caixa_anterior > cfg.salario_fundador_caixa_minimo_seguranca
        return cfg.salario_fundador_valor if (inicio_ok and caixa_ok) else 0.0

    # --- Execução versão robusta, preserva colunas esperadas pelo app --- #
    def executar_projecao(self, meses: int = 36) -> pd.DataFrame:
        cfg = self.config

        # colunas esperadas (compatíveis com seu main.py)
        colunas = [
            'mes', 'Usuarios_Iniciais', 'Visitantes', 'Novos_Trials', 'Novos_Pagantes',
            'Usuarios_Perdidos', 'Usuarios_Finais', 'MRR', 'COGS', 'Custo_IA', 'Impostos',
            'Taxas_Pagamento', 'Comissoes_Afiliados', 'COGS_Total', 'Lucro_Bruto',
            'Custo_Infra', 'Custo_Marketing', 'Salario_Pago', 'Custo_Pessoal_CLT', 'Custo_Pessoal_PJ',
            'Custo_Escritorio', 'Custo_Ferramentas', 'Custo_Servicos_Profissionais',
            'Custo_Depreciacao', 'Custo_Despesas_Anuais', 'OPEX_Total',
            'Resultado_Operacional', 'Aporte', 'Fluxo_Caixa', 'Saldo_Caixa',
            'CAC_Mensal', 'LTV_CAC_Ratio_Mensal', 'arpu', 'ltv', 'cac'
        ]

        registros = []

        # inicializações
        saldo_caixa = float(cfg.capital_inicial_caixa if cfg.capital_inicial_caixa is not None else 0.0)
        visitantes = float(cfg.visitantes_mes_1 if cfg.visitantes_mes_1 is not None else 0.0)
        usuarios = 0.0  # inicialmente nenhum ativo previsto (o config pode ter overrides)
        acum_novos_pagantes = 0.0
        acum_marketing = 0.0

        for t in range(1, meses + 1):
            # tráfego / novos
            if t == 1:
                visitantes_mes = visitantes
            else:
                visitantes_mes = visitantes * (1 + cfg.taxa_crescimento_trafego_mensal)
                visitantes = visitantes_mes  # atualiza para próximo mês

            novos_trials = visitantes_mes * cfg.taxa_conversao_visitante_trial
            novos_pagantes = novos_trials * cfg.taxa_conversao_trial_pagante

            # churn e usuários
            usuarios_perdidos = usuarios * cfg.churn_mensal
            usuarios = max(0.0, usuarios + novos_pagantes - usuarios_perdidos)

            # receita
            arpu = float(cfg.arpu_medio)
            mrr = usuarios * arpu if cfg.ativar_receita_por_usuario else 0.0

            # COGS: custo IA + impostos + taxas + comissões afiliados (se ativo)
            custo_ia = usuarios * cfg.custo_ia_por_usuario if cfg.ativar_custo_ia else 0.0
            impostos = mrr * cfg.aliquota_impostos if cfg.ativar_impostos else 0.0

            # taxas pagamento: fixas por transação + percentual sobre mrr (aplicável só se ativado)
            taxas_pgto = 0.0
            if cfg.ativar_taxas_pgto:
                taxas_pgto = (novos_pagantes * cfg.taxa_pagamento_fixa_por_transacao) + (mrr * cfg.taxa_pagamento_percentual)

            comissoes_afiliados = 0.0
            if cfg.ativar_comissoes_afiliado and cfg.comissao_afiliados is not None:
                if t >= cfg.comissao_afiliados.mes_inicio_programa:
                    comissoes_afiliados = mrr * cfg.comissao_afiliados.percentual_sobre_venda * cfg.comissao_afiliados.percentual_vendas_via_afiliados

            cogs_total = custo_ia + impostos + taxas_pgto + comissoes_afiliados
            lucro_bruto = mrr - cogs_total

            # infra e marketing
            custo_infra = self.calcular_custo_infraestrutura(int(round(usuarios)))
            custo_marketing = self.calcular_custo_marketing(t, lucro_bruto)

            # salário fundador condicional
            salario_fundador = self.calcular_salario_fundador(t, saldo_caixa) if cfg.ativar_fundador else 0.0

            # pessoal CLT/PJ
            custo_clt = 0.0
            custo_pj = 0.0
            if cfg.ativar_equipe_clt or cfg.ativar_equipe_pj:
                for f in cfg.equipe:
                    custo = f.calcular_custo_mensal(t)
                    if f.tipo.upper() == "CLT":
                        custo_clt += custo
                    else:
                        custo_pj += custo

            # escritório
            custo_escritorio = cfg.escritorio_custo_total_mensal if (cfg.ativar_escritorio and t >= cfg.escritorio_mes_inicio) else 0.0

            # ferramentas SaaS
            custo_ferramentas = 0.0
            if cfg.ativar_ferramentas:
                for tool in cfg.ferramentas_saas:
                    custo_ferramentas += tool.calcular_custo(t)

            # serviços profissionais
            custo_servicos = 0.0
            if cfg.ativar_servicos_profs:
                if t >= cfg.contabilidade_mes_inicio:
                    custo_servicos += cfg.contabilidade_mensal
                if t >= cfg.advogado_mes_inicio:
                    custo_servicos += cfg.advogado_retainer_mensal
                custo_servicos += cfg.consultorias_outras_mensal

            # depreciacao ativos
            custo_depreciacao = 0.0
            if cfg.ativar_depreciacao:
                for ativo in cfg.ativos_depreciaveis:
                    custo_depreciacao += ativo.calcular_depreciacao_mensal(t)

            # despesas anuais rateadas
            custo_despesas_anuais = 0.0
            if cfg.ativar_despesas_anuais:
                for desp in cfg.despesas_anuais:
                    if desp.ativo and t >= desp.mes_inicio and (desp.mes_fim is None or t <= desp.mes_fim):
                        custo_despesas_anuais += desp.valor_mensal_rateado

            # OPEX
            opex_total = (
                custo_infra + custo_marketing + salario_fundador +
                custo_clt + custo_pj + custo_escritorio +
                custo_ferramentas + custo_servicos +
                custo_depreciacao + custo_despesas_anuais
            )

            # resultado e caixa
            resultado_operacional = lucro_bruto - opex_total
            aporte = cfg.aporte_mensal_fixo if t <= cfg.meses_aporte_fixo else 0.0
            fluxo_caixa = resultado_operacional + aporte
            saldo_caixa = saldo_caixa + fluxo_caixa

            # CAC / LTV
            cac_mensal = _safe_div(custo_marketing, novos_pagantes, default=np.nan)
            ltv = cfg.calcular_ltv()
            ltv_cac_ratio = _safe_div(ltv, cac_mensal, default=np.nan)

            # acumula para métricas médias
            acum_novos_pagantes += novos_pagantes
            acum_marketing += custo_marketing

            registros.append({
                'mes': t,
                'Usuarios_Iniciais': round(usuarios - novos_pagantes + usuarios_perdidos, 2),
                'Visitantes': round(visitantes_mes, 0),
                'Novos_Trials': round(novos_trials, 2),
                'Novos_Pagantes': round(novos_pagantes, 2),
                'Usuarios_Perdidos': round(usuarios_perdidos, 2),
                'Usuarios_Finais': round(usuarios, 2),
                'MRR': round(mrr, 2),
                'COGS': round(cogs_total, 2),
                'Custo_IA': round(custo_ia, 2),
                'Impostos': round(impostos, 2),
                'Taxas_Pagamento': round(taxas_pgto, 2),
                'Comissoes_Afiliados': round(comissoes_afiliados, 2),
                'COGS_Total': round(cogs_total, 2),
                'Lucro_Bruto': round(lucro_bruto, 2),
                'Custo_Infra': round(custo_infra, 2),
                'Custo_Marketing': round(custo_marketing, 2),
                'Salario_Pago': round(salario_fundador, 2),
                'Custo_Pessoal_CLT': round(custo_clt, 2),
                'Custo_Pessoal_PJ': round(custo_pj, 2),
                'Custo_Escritorio': round(custo_escritorio, 2),
                'Custo_Ferramentas': round(custo_ferramentas, 2),
                'Custo_Servicos_Profissionais': round(custo_servicos, 2),
                'Custo_Depreciacao': round(custo_depreciacao, 2),
                'Custo_Despesas_Anuais': round(custo_despesas_anuais, 2),
                'OPEX_Total': round(opex_total, 2),
                'Resultado_Operacional': round(resultado_operacional, 2),
                'Aporte': round(aporte, 2),
                'Fluxo_Caixa': round(fluxo_caixa, 2),
                'Saldo_Caixa': round(saldo_caixa, 2),
                'CAC_Mensal': round(cac_mensal, 2) if not np.isnan(cac_mensal) else np.nan,
                'LTV_CAC_Ratio_Mensal': round(ltv_cac_ratio, 2) if not np.isnan(ltv_cac_ratio) else np.nan,
                'arpu': round(arpu, 2),
                'ltv': round(ltv, 2),
                'cac': round(_safe_div(acum_marketing, acum_novos_pagantes, default=np.nan), 2) if acum_novos_pagantes > 0 else np.nan
            })

        df = pd.DataFrame.from_records(registros, columns=colunas)
        # Conserta tipos e ordenação
        df.fillna(value=np.nan, inplace=True)
        self.projecao_df = df
        return df

    # --- KPIs compatíveis com o app --- #
    def calcular_kpis(self) -> Dict[str, Any]:
        if self.projecao_df is None:
            raise RuntimeError("Execute executar_projecao() antes de calcular_kpis()")
        df = self.projecao_df.copy()
        kpis = {}

        # Break-even: primeiro mês com Resultado_Operacional > 0
        be = df[df['Resultado_Operacional'] > 0]
        kpis['Break_Even_Mes'] = int(be.iloc[0]['mes']) if not be.empty else None

        # Payback: primeiro mês com Saldo_Caixa > 0 (após considerar aporte inicial)
        pb = df[df['Saldo_Caixa'] > 0]
        kpis['Payback_Investimento_Mes'] = int(pb.iloc[0]['mes']) if not pb.empty else None

        # Vale da Morte
        kpis['Vale_da_Morte_Minimo_Caixa'] = float(df['Saldo_Caixa'].min())
        kpis['Vale_da_Morte_Mes'] = int(df.loc[df['Saldo_Caixa'].idxmin(), 'mes'])

        # Runway aproximado (meses com saldo negativo consecutivos do início)
        negative_mask = df['Saldo_Caixa'] < 0
        if negative_mask.any():
            first_neg_index = int(df[negative_mask].index[0])
            kpis['Runway_Meses'] = int(first_neg_index)  # meses antes de entrar negativo
        else:
            kpis['Runway_Meses'] = f">= {len(df)}"

        # Unit economics (base config + média CAC)
        kpis['LTV_Final'] = float(self.config.calcular_ltv())
        # CAC médio calculado como total marketing / novos pagantes (segurança)
        total_marketing = df['Custo_Marketing'].sum()
        total_novos = df['Novos_Pagantes'].sum()
        kpis['CAC_Medio_Periodo'] = float(_safe_div(total_marketing, total_novos, default=np.nan))
        kpis['LTV_CAC_Ratio_Final'] = float(_safe_div(kpis['LTV_Final'], kpis['CAC_Medio_Periodo'], default=np.nan))
        kpis['CAC_Payback_Meses_Config'] = float(self.config.calcular_cac_payback_meses())

        # Snapshot ano1, ano2, ano3 (se existirem)
        if len(df) >= 12:
            kpis['MRR_Ano1'] = float(df.iloc[11]['MRR'])
            kpis['Usuarios_Ano1'] = float(df.iloc[11]['Usuarios_Finais'])
        else:
            kpis['MRR_Ano1'] = None
            kpis['Usuarios_Ano1'] = None
        if len(df) >= 24:
            kpis['MRR_Ano2'] = float(df.iloc[23]['MRR'])
            kpis['Usuarios_Ano2'] = float(df.iloc[23]['Usuarios_Finais'])
        if len(df) >= 36:
            kpis['MRR_Ano3'] = float(df.iloc[35]['MRR'])
            kpis['Usuarios_Ano3'] = float(df.iloc[35]['Usuarios_Finais'])
            kpis['Saldo_Caixa_Final'] = float(df.iloc[35]['Saldo_Caixa'])
        else:
            kpis['MRR_Ano3'] = float(df.iloc[-1]['MRR'])
            kpis['Usuarios_Ano3'] = float(df.iloc[-1]['Usuarios_Finais'])
            kpis['Saldo_Caixa_Final'] = float(df.iloc[-1]['Saldo_Caixa'])

        self.kpis = kpis
        return kpis


# Procedural wrapper: gerar_projecao_financeira (compatível com app main)
def gerar_projecao_financeira(premissas: Dict[str, Any], meses: int = 36) -> pd.DataFrame:
    """
    Função procedural utilitária que aceita um dicionário de premissas
    (compatível com a estrutura usada em notebooks e no main.py) e retorna o DataFrame.
    Isso facilita integração rápida com o frontend.
    """
    # constrói um objeto ConfigFinanceira baseado nas premissas recebidas (não destrói o CONFIG global)
    cfg = ConfigFinanceira()
    # Mapeamento defensivo das premissas para atributos do config
    for k, v in premissas.items():
        if hasattr(cfg, k):
            try:
                setattr(cfg, k, v)
            except Exception:
                pass
    # usa o motor de classe para compatibilidade total
    motor = MotorProjecaoFinanceira(cfg)
    df = motor.executar_projecao(meses=meses)
    return df
