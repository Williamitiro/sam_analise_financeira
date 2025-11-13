"""
SAM Financial Model - Motor de Projeção (Versão 2.0 - Completa)
Executa as projeções financeiras mês a mês, integrando-se com o config.py.

Este arquivo é o "cérebro" do aplicativo. Ele contém toda a lógica de cálculo.
Uma interface gráfica (GUI) não precisa saber *como* calcular, apenas precisa
instanciar esta classe, chamar seus métodos e ler os resultados.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
from config import ConfigFinanceira

class MotorProjecaoFinanceira:
    """
    Motor de simulação financeira para o SAM.
    
    Executa projeções de 36 meses aplicando lógicas complexas:
    - Funil de aquisição com crescimento composto
    - Infraestrutura escalável em tiers
    - Marketing em fases (fixo → % lucro)
    - Salário condicional baseado em caixa
    - Cálculo completo de OPEX (Pessoal, Escritório, SaaS, etc.)
    """
    
    def __init__(self, config: ConfigFinanceira):
        """
        Inicializa o motor com uma configuração específica.
        
        Args:
            config (ConfigFinanceira): Objeto com todas as premissas do modelo.
        """
        self.config = config
        self.projecao_df: Optional[pd.DataFrame] = None
        self.kpis: Optional[Dict] = None
    
    # --- MÉTODOS DE CÁLCULO DE CUSTOS INDIVIDUAIS ---
    
    def calcular_custo_infraestrutura(self, usuarios: int) -> float:
        """
        Calcula custo de infraestrutura baseado em tiers escaláveis.
        
        TIER 1 (0-100): R$ 209/mês (Validação MT5)
        TIER 2 (101-500): R$ 5.559/mês (API Profissional)
        TIER 3 (501+): TIER 2 + R$ 1,50/usuário adicional
        """
        if usuarios <= self.config.infra_tier1_limite:
            return self.config.infra_tier1_custo_fixo
        
        elif usuarios <= self.config.infra_tier2_limite:
            return self.config.infra_tier2_custo_fixo
        
        else:  # TIER 3
            usuarios_adicionais = usuarios - self.config.infra_tier2_limite
            custo_variavel = usuarios_adicionais * self.config.infra_tier3_custo_por_usuario
            return self.config.infra_tier2_custo_fixo + custo_variavel
    
    def calcular_custo_marketing(self, mes: int, lucro_bruto: float) -> float:
        """
        Calcula gasto de marketing em 2 fases.
        
        FASE 1 (meses 1-3): Gasto fixo de validação
        FASE 2 (mês 4+): % do lucro bruto (nunca negativo)
        """
        if mes <= self.config.marketing_fase1_duracao_meses:
            return self.config.marketing_fase1_custo_fixo
        else:
            gasto = lucro_bruto * self.config.marketing_fase2_perc_lucro_bruto
            return max(0, gasto)  # Nunca negativo
    
    def calcular_salario_fundador(self, mes: int, saldo_caixa_anterior: float) -> float:
        """
        Aplica lógica condicional DURA para salário.
        
        REGRA: Só paga se:
        1. mes >= mes_inicio_ideal E
        2. saldo_caixa_anterior > caixa_minimo_seguranca
        """
        inicio_ok = mes >= self.config.salario_fundador_mes_inicio_ideal
        caixa_ok = saldo_caixa_anterior > self.config.salario_fundador_caixa_minimo_seguranca
        
        if inicio_ok and caixa_ok:
            return self.config.salario_fundador_valor
        else:
            return 0.0

    # --- [ADIÇÃO] MÉTODO PRINCIPAL DE CÁLCULO DE OPEX ---
    
    def _calcular_opex_total_detelhado(self, mes: int, usuarios: int, novos_pagantes: float, mrr: float) -> float:
        """
        [NOVO E ESSENCIAL] Calcula o OPEX total de forma completa, usando todas as listas do config.py.
        
        Este é o método que integra o motor com a complexidade do seu arquivo de configuração.
        Ele soma todos os custos operacionais para um mês específico.
        
        Args:
            mes (int): O mês atual da projeção (1, 2, 3...).
            usuarios (int): Número de usuários finais do mês.
            novos_pagantes (float): Número de novos clientes pagantes no mês.
            mrr (float): Receita recorrente mensal do mês.
        
        Returns:
            float: O valor total do OPEX para o mês.
        """
        custo_total = 0.0

        # 1. Custos de Infraestrutura (já existente)
        custo_infra = self.calcular_custo_infraestrutura(usuarios)
        custo_total += custo_infra

        # 2. Custos de Marketing (já existente)
        # Nota: O lucro_bruto ainda não foi calculado aqui, então vamos passar como argumento
        # Para simplificar, vamos calcular o marketing de forma fixa aqui e ajustar no loop principal
        # ou podemos calcular o marketing de forma percentual no loop principal.
        # A forma mais limpa é calcular o marketing no loop principal e passar o valor.
        # Vamos manter a lógica original no loop principal para não quebrar.
        # custo_marketing = self.calcular_custo_marketing(mes, lucro_bruto) # Isso será calculado no loop
        # custo_total += custo_marketing

        # 3. Salário do Fundador (já existente)
        # Será calculado no loop principal por depender do saldo de caixa anterior.
        # salario_fundador = self.calcular_salario_fundador(mes, saldo_caixa_anterior)
        # custo_total += salario_fundador

        # [ADIÇÃO] 4. Custos de Pessoal (CLT e PJ)
        for funcionario in self.config.equipe:
            custo_total += funcionario.calcular_custo_mensal(mes)

        # [ADIÇÃO] 5. Custos de Escritório e Operação
        if mes >= self.config.escritorio_mes_inicio:
            custo_total += self.config.escritorio_custo_total_mensal

        # [ADIÇÃO] 6. Ferramentas SaaS
        for ferramenta in self.config.ferramentas_saas:
            custo_total += ferramenta.calcular_custo(mes)

        # [ADIÇÃO] 7. Serviços Profissionais
        if mes >= self.config.contabilidade_mes_inicio:
            custo_total += self.config.contabilidade_mensal
        if mes >= self.config.advogado_mes_inicio:
            custo_total += self.config.advogado_retainer_mensal
        
        custo_total += self.config.consultorias_outras_mensal

        # [ADIÇÃO] 8. Depreciação de Ativos
        for ativo in self.config.ativos_depreciaveis:
            custo_total += ativo.calcular_depreciacao_mensal(mes)

        # [ADIÇÃO] 9. Despesas Anuais (Rateadas)
        for despesa_anual in self.config.despesas_anuais:
            custo_total += despesa_anual.valor_mensal_rateado
        
        # [ADIÇÃO] 10. Custos Variáveis Adicionais
        # Taxas de Meios de Pagamento
        custo_transacoes = (novos_pagantes * self.config.taxa_pagamento_fixa_por_transacao) + \
                           (mrr * self.config.taxa_pagamento_percentual)
        custo_total += custo_transacoes

        # Comissões de Afiliados
        if self.config.comissao_afiliados and mes >= self.config.comissao_afiliados.mes_inicio_programa:
            comissao_valor = mrr * self.config.comissao_afiliados.percentual_sobre_venda * \
                             self.config.comissao_afiliados.percentual_vendas_via_afiliados
            custo_total += comissao_valor
        
        return custo_total
    
    # --- MÉTODO PRINCIPAL DE EXECUÇÃO DA PROJEÇÃO ---
    
    def executar_projecao(self, meses: int = 36) -> pd.DataFrame:
        """
        Executa a projeção financeira completa.
        
        Returns:
            DataFrame com todas as métricas mês a mês
        """
        # Inicializa estrutura de dados
        colunas = [
            'Mes', 'Usuarios_Iniciais', 'Visitantes', 'Novos_Trials', 
            'Novos_Pagantes', 'Usuarios_Perdidos', 'Usuarios_Finais',
            'MRR', 'COGS', 'Impostos', 'Lucro_Bruto',
            'Custo_Infra', 'Custo_Marketing', 'Salario_Pago', 'OPEX_Total',
            'Resultado_Operacional', 'Aporte', 'Fluxo_Caixa', 'Saldo_Caixa',
            # [ADIÇÃO] Novas colunas para KPIs mensais
            'CAC_Mensal', 'LTV_CAC_Ratio_Mensal'
        ]
        
        dados = []
        
        # Condições iniciais
        saldo_caixa_anterior = self.config.capital_inicial_caixa
        usuarios_finais_anterior = 0
        visitantes_anterior = self.config.visitantes_mes_1
        
        # Loop mês a mês
        for t in range(1, meses + 1):
            # --- AQUISIÇÃO E RETENÇÃO ---
            usuarios_iniciais = usuarios_finais_anterior
            
            # Crescimento de tráfego (composto)
            if t > 1:
                visitantes = visitantes_anterior * (1 + self.config.taxa_crescimento_trafego_mensal)
            else:
                visitantes = visitantes_anterior
            
            # Funil de conversão (usando taxas do config)
            novos_trials = visitantes * self.config.taxa_conversao_visitante_trial
            novos_pagantes = novos_trials * self.config.taxa_conversao_trial_pagante
            
            # Churn
            usuarios_perdidos = usuarios_iniciais * self.config.churn_mensal
            
            # Usuários finais do mês
            usuarios_finais = usuarios_iniciais + novos_pagantes - usuarios_perdidos
            
            # --- RECEITA E LUCRO BRUTO ---
            mrr = usuarios_finais * self.config.arpu_medio
            cogs = usuarios_finais * self.config.custo_ia_por_usuario
            impostos = mrr * self.config.aliquota_impostos
            lucro_bruto = mrr - cogs - impostos
            
            # --- CUSTOS FIXOS (OPEX) ---
            # Cálculo dos custos individuais que dependem de lógica complexa
            custo_infra = self.calcular_custo_infraestrutura(int(usuarios_finais))
            custo_marketing = self.calcular_custo_marketing(t, lucro_bruto)
            salario_pago = self.calcular_salario_fundador(t, saldo_caixa_anterior)
            
            # [ALTERAÇÃO] Agora, calculamos o OPEX total usando o novo método detalhado
            # Passamos os valores necessários para o cálculo de custos variáveis
            opex_total = self._calcular_opex_total_detelhado(t, int(usuarios_finais), novos_pagantes, mrr)
            
            # [NOTA] O método `_calcular_opex_total_detelhado` já inclui custo_infra, marketing e salario_fundador.
            # Para evitar dupla contagem, temos duas opções:
            # 1. (Escolhida) Manter a chamada individual e somar apenas os custos NÃO inclusos no método detalhado.
            # 2. Refatorar o método detalhado para NÃO incluir esses três e somar tudo aqui.
            # Vou refatorar o método detalhado para ser mais limpo e somar tudo aqui.

            # --- [REFACTORING] Lógica de Cálculo de OPEX ---
            # Vamos calcular cada parte e somar no final para maior clareza.
            
            # Custos Individuais com Lógica Complexa
            custo_infra = self.calcular_custo_infraestrutura(int(usuarios_finais))
            custo_marketing = self.calcular_custo_marketing(t, lucro_bruto)
            salario_pago = self.calcular_salario_fundador(t, saldo_caixa_anterior)

            # Custos Agregados do Config (sem lógica complexa interna)
            custo_pessoal = sum(f.calcular_custo_mensal(t) for f in self.config.equipe)
            custo_escritorio = self.config.escritorio_custo_total_mensal if t >= self.config.escritorio_mes_inicio else 0.0
            custo_ferramentas = sum(f.calcular_custo(t) for f in self.config.ferramentas_saas)
            custo_servicos = (self.config.contabilidade_mensal if t >= self.config.contabilidade_mes_inicio else 0.0) + \
                             (self.config.advogado_retainer_mensal if t >= self.config.advogado_mes_inicio else 0.0) + \
                             self.config.consultorias_outras_mensal
            custo_depreciacao = sum(a.calcular_depreciacao_mensal(t) for a in self.config.ativos_depreciaveis)
            custo_despesas_anuais = sum(d.valor_mensal_rateado for d in self.config.despesas_anuais)
            
            # Custos Variáveis
            custo_transacoes = (novos_pagantes * self.config.taxa_pagamento_fixa_por_transacao) + \
                               (mrr * self.config.taxa_pagamento_percentual)
            custo_comissoes = 0.0
            if self.config.comissao_afiliados and t >= self.config.comissao_afiliados.mes_inicio_programa:
                custo_comissoes = mrr * self.config.comissao_afiliados.percentual_sobre_venda * \
                                  self.config.comissao_afiliados.percentual_vendas_via_afiliados

            # Soma de Tudo
            opex_total = (custo_infra + custo_marketing + salario_pago + custo_pessoal +
                          custo_escritorio + custo_ferramentas + custo_servicos +
                          custo_depreciacao + custo_despesas_anuais + custo_transacoes +
                          custo_comissoes)
            
            # --- FLUXO DE CAIXA ---
            resultado_operacional = lucro_bruto - opex_total
            
            # Aporte do fundador
            aporte = self.config.aporte_mensal_fixo if t <= self.config.meses_aporte_fixo else 0
            
            fluxo_caixa = resultado_operacional + aporte
            saldo_caixa_atual = saldo_caixa_anterior + fluxo_caixa
            
            # --- [ADIÇÃO] CÁLCULO DE KPIS MENSAIS ---
            cac_mensal = custo_marketing / novos_pagantes if novos_pagantes > 0 else 0
            # LTV vem do config, mas podemos calcular o ratio mensal
            ltv = self.config.calcular_ltv()
            ltv_cac_ratio_mensal = ltv / cac_mensal if cac_mensal > 0 else 0
            
            # --- REGISTRA DADOS DO MÊS ---
            dados.append({
                'Mes': t,
                'Usuarios_Iniciais': round(usuarios_iniciais, 2),
                'Visitantes': round(visitantes, 0),
                'Novos_Trials': round(novos_trials, 2),
                'Novos_Pagantes': round(novos_pagantes, 2),
                'Usuarios_Perdidos': round(usuarios_perdidos, 2),
                'Usuarios_Finais': round(usuarios_finais, 2),
                'MRR': round(mrr, 2),
                'COGS': round(cogs, 2),
                'Impostos': round(impostos, 2),
                'Lucro_Bruto': round(lucro_bruto, 2),
                'Custo_Infra': round(custo_infra, 2),
                'Custo_Marketing': round(custo_marketing, 2),
                'Salario_Pago': round(salario_pago, 2),
                'OPEX_Total': round(opex_total, 2),
                'Resultado_Operacional': round(resultado_operacional, 2),
                'Aporte': round(aporte, 2),
                'Fluxo_Caixa': round(fluxo_caixa, 2),
                'Saldo_Caixa': round(saldo_caixa_atual, 2),
                'CAC_Mensal': round(cac_mensal, 2),
                'LTV_CAC_Ratio_Mensal': round(ltv_cac_ratio_mensal, 2)
            })
            
            # Atualiza variáveis para próxima iteração
            saldo_caixa_anterior = saldo_caixa_atual
            usuarios_finais_anterior = usuarios_finais
            visitantes_anterior = visitantes
        
        # Cria DataFrame
        self.projecao_df = pd.DataFrame(dados, columns=colunas)
        
        # --- GUI HOOK: O resultado final está em self.projecao_df. A GUI pode usar este DataFrame para popular tabelas e gráficos. ---
        return self.projecao_df
    
    def calcular_kpis(self) -> Dict:
        """
        Calcula os principais KPIs do negócio a partir da projeção final.
        
        Returns:
            Dicionário com métricas de viabilidade
        """
        if self.projecao_df is None:
            raise ValueError("Execute executar_projecao() primeiro")
        
        df = self.projecao_df
        kpis = {}
        
        # --- KPIS DE VIABILIDADE ---
        # Ponto de Equilíbrio (Break-Even)
        break_even = df[df['Resultado_Operacional'] > 0]
        if not break_even.empty:
            kpis['Break_Even_Mes'] = int(break_even.iloc[0]['Mes'])
        else:
            kpis['Break_Even_Mes'] = None
        
        # Payback do Investimento
        payback = df[df['Saldo_Caixa'] > 0]
        if not payback.empty:
            kpis['Payback_Investimento_Mes'] = int(payback.iloc[0]['Mes'])
        else:
            kpis['Payback_Investimento_Mes'] = None
        
        # Vale da Morte (Necessidade Máxima de Caixa)
        kpis['Vale_da_Morte_Minimo_Caixa'] = float(df['Saldo_Caixa'].min())
        mes_vale = int(df.loc[df['Saldo_Caixa'].idxmin(), 'Mes'])
        kpis['Vale_da_Morte_Mes'] = mes_vale
        
        # Runway (Meses até caixa negativo)
        saldo_negativo = df[df['Saldo_Caixa'] < 0]
        if not saldo_negativo.empty:
            kpis['Runway_Meses'] = int(saldo_negativo.iloc[0]['Mes']) - 1
        else:
            kpis['Runway_Meses'] = "> 36"
        
        # --- [ADIÇÃO] KPIS DE UNIT ECONOMICS E NEGÓCIO ---
        # Métricas de Unit Economics (valores finais ou médios)
        kpis['LTV_Final'] = self.config.calcular_ltv()
        kpis['LTV_CAC_Ratio_Final'] = self.config.calcular_ltv_cac_ratio()
        kpis['CAC_Payback_Meses_Config'] = self.config.calcular_cac_payback_meses()
        
        # CAC Médio do Período
        cac_medio = df['Custo_Marketing'].sum() / df['Novos_Pagantes'].sum()
        kpis['CAC_Medio_Periodo'] = cac_medio

        # Métricas finais (Ano 3)
        ultimo_mes = df.iloc[-1]
        kpis['MRR_Ano3'] = float(ultimo_mes['MRR'])
        kpis['Usuarios_Ano3'] = float(ultimo_mes['Usuarios_Finais'])
        kpis['Saldo_Caixa_Final'] = float(ultimo_mes['Saldo_Caixa'])
        
        # Métricas anuais
        kpis['MRR_Ano1'] = float(df.iloc[11]['MRR'])
        kpis['MRR_Ano2'] = float(df.iloc[23]['MRR'])
        
        kpis['Usuarios_Ano1'] = float(df.iloc[11]['Usuarios_Finais'])
        kpis['Usuarios_Ano2'] = float(df.iloc[23]['Usuarios_Finais'])
        
        self.kpis = kpis
        return kpis
    
    def gerar_relatorio_texto(self) -> str:
        """Gera relatório textual dos KPIs. Útil para CLI ou para exportar."""
        if self.kpis is None:
            self.calcular_kpis()
        
        relatorio = """
╔════════════════════════════════════════════════════════════════╗
║          RELATÓRIO DE VIABILIDADE FINANCEIRA - SAM             ║
╚════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════
📊 INDICADORES DE VIABILIDADE
═══════════════════════════════════════════════════════════════
"""
        
        # Break-Even
        if self.kpis['Break_Even_Mes']:
            relatorio += f"✅ Ponto de Equilíbrio: Mês {self.kpis['Break_Even_Mes']}\n"
        else:
            relatorio += "❌ Ponto de Equilíbrio: NÃO ATINGIDO em 36 meses\n"
        
        # Payback
        if self.kpis['Payback_Investimento_Mes']:
            relatorio += f"✅ Payback do Investimento: Mês {self.kpis['Payback_Investimento_Mes']}\n"
        else:
            relatorio += "❌ Payback do Investimento: NÃO ATINGIDO em 36 meses\n"
        
        relatorio += f"""
💰 Vale da Morte (Menor Saldo): R$ {self.kpis['Vale_da_Morte_Minimo_Caixa']:,.2f} (Mês {self.kpis['Vale_da_Morte_Mes']})
🏃 Runway: {self.kpis['Runway_Meses']} meses

═══════════════════════════════════════════════════════════════
💵 MÉTRICAS DE UNIT ECONOMICS
═══════════════════════════════════════════════════════════════
📈 LTV (Lifetime Value): R$ {self.kpis['LTV_Final']:,.2f}
📊 LTV/CAC Ratio: {self.kpis['LTV_CAC_Ratio_Final']:.2f}x
   {'✅ SAUDÁVEL (> 3.0)' if self.kpis['LTV_CAC_Ratio_Final'] > 3 else '⚠️  ATENÇÃO (< 3.0)'}
💳 CAC Médio do Período: R$ {self.kpis['CAC_Medio_Periodo']:,.2f}
⏳ CAC Payback (Config): {self.kpis['CAC_Payback_Meses_Config']:.1f} meses

═══════════════════════════════════════════════════════════════
📆 CRESCIMENTO PROJETADO
═══════════════════════════════════════════════════════════════
Ano 1 (Mês 12):
  • Usuários: {self.kpis['Usuarios_Ano1']:.0f}
  • MRR: R$ {self.kpis['MRR_Ano1']:,.2f}

Ano 2 (Mês 24):
  • Usuários: {self.kpis['Usuarios_Ano2']:.0f}
  • MRR: R$ {self.kpis['MRR_Ano2']:,.2f}

Ano 3 (Mês 36):
  • Usuários: {self.kpis['Usuarios_Ano3']:.0f}
  • MRR: R$ {self.kpis['MRR_Ano3']:,.2f}
  • Saldo de Caixa Final: R$ {self.kpis['Saldo_Caixa_Final']:,.2f}

═══════════════════════════════════════════════════════════════
"""
        # --- GUI HOOK: A GUI pode pegar esta string e exibi-la em um widget de texto. ---
        return relatorio
    
    def exportar_para_excel(self, caminho: str = "projecao_sam.xlsx"):
        """Exporta projeção e KPIs para Excel. Ótimo funcionalidade para o usuário final."""
        if self.projecao_df is None or self.kpis is None:
            raise ValueError("Execute executar_projecao() e calcular_kpis() primeiro")
        
        with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
            # Aba 1: Projeção detalhada
            self.projecao_df.to_excel(writer, sheet_name='Projeção', index=False)
            
            # Aba 2: KPIs
            kpis_df = pd.DataFrame(list(self.kpis.items()), columns=['KPI', 'Valor'])
            kpis_df.to_excel(writer, sheet_name='KPIs', index=False)
            
            # Aba 3: Configuração usada
            config_df = pd.DataFrame(list(self.config.to_dict().items()), columns=['Parâmetro', 'Valor'])
            config_df.to_excel(writer, sheet_name='Configuração', index=False)
        
        # --- GUI HOOK: A GUI pode chamar este método a partir de um botão "Exportar Excel" e exibir uma mensagem de sucesso. ---
        print(f"✅ Projeção exportada para: {caminho}")
        return caminho
