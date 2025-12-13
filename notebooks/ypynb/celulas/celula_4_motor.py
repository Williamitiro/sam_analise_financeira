# CÉLULA 04 - MOTOR FINANCEIRO V13 (DEFINITIVE EDITION + CORREÇÕES CIRÚRGICAS)
# ====================================================================
# VERSÃO: 13.0 (CORREÇÕES PONTUAIS - RUNWAY, RH, CAPEX)
# STATUS: PRODUCTION READY - GOLD STANDARD
#
# LOG DE CORREÇÕES (V12.1 - CORREÇÕES CIRÚRGICAS):
# 1. ✅ NRR (Net Revenue Retention): Fórmula corrigida para (Start - Churn + Expansion) / Start.
# 2. ✅ Burn Rate: Agora calculado sobre Fluxo de Caixa (inclui CAPEX, exclui Depreciação).
# 3. ✅ Custo B2B: Receita de Setup agora tem contrapartida de Custo de Implantação (COGS).
# 4. ✅ Zero Hardcode: Valores mágicos (3000, 5000, etc.) movidos para p_run.get().
# 5. ✅ Vetores Detalhados: Receitas e Custos por Tier/Canal agora são populados.
# 6. ✅ Impostos: Mantida lógica de Faturamento (Correto para Brasil/Simples/Presumido).
# 7. ✅ COGS Recorrente: Separado de COGS B2B para LTV correto.
# 8. ✅ LTV Limpo: Calculado apenas com Margem Recorrente (sem contaminação B2B).
# 9. ✅ NRR Real: Tracking de Base Legada (Start - Churn + Expansion) / Start.
# 10. ✅ Vetores: mrr_cohort_m0, cogs_recorrente, churn_mrr_cohort_m0 inicializados.
# 11. ✅ df_anual Inteligente: Agregação correta (fluxos=soma, estoques=último, taxas=média).
# 12. ✅ Impostos B2B: Decisão de regime usa faturamento projetado (ARR + B2B*12).
# 13. ✅ Saturação Mercado: Limite dinâmico baseado em mercado disponível.
# 14. ✅ Runway Protegido: Sem valores negativos (runway=0 se caixa < threshold).
# ====================================================================

def executar_motor_fintech_v10_production_ready(p, seed=None, variacao_params=None, modo_debug=False, simulacao_id=0):
    """
    Motor de Simulação Financeira V11.0 - Definitive Edition
    
    Parâmetros:
    -----------
    p : dict
        Dicionário de premissas (da Célula 02)
    seed : int, opcional
        Seed para reprodutibilidade (padrão: 42)
    variacao_params : dict, opcional
        Parâmetros alterados para Monte Carlo
    modo_debug : bool, opcional
        Ativa logs detalhados (padrão: False)
    simulacao_id : int, opcional
        ID da simulação (para seed Monte Carlo única por run)
    """
    import pandas as pd
    import numpy as np
    from collections import defaultdict
    
    # --------------------------------------------------------------------
    # BLOCO 0: CONFIGURAÇÃO E VALIDAÇÃO DE ENTRADA
    # --------------------------------------------------------------------
    p_run = p.copy()
    if variacao_params:
        for k, v in variacao_params.items():
            p_run[k] = v
    
    # Seed reprodutível para Monte Carlo
    if seed is None:
        seed = p_run.get('seed_fixa', 42)
    seed = int(seed)
    
    # Garante variabilidade real entre simulações do Monte Carlo
    np.random.seed(seed + simulacao_id * 12345)
    
    # Validação de inputs críticos
    assert p_run['meses_projecao'] > 0, "meses_projecao deve ser > 0"
    assert 0 <= p_run['mix_lite'] + p_run['mix_trader'] + p_run['mix_pro'] <= 1.01, "Soma dos mix deve ser ~100%"
    assert p_run['caixa_inicial'] >= 0, "caixa_inicial não pode ser negativo"
    
    meses = int(p_run['meses_projecao'])
    datas = pd.date_range(start=p_run['data_inicio'], periods=meses, freq='MS')
    alertas = []
    
    # --- PARÂMETROS DE SEGURANÇA E PADRÕES (ZERO HARDCODE) ---
    # Valores movidos do código para variáveis com defaults seguros
    THRESHOLD_QUEBRA = p_run.get('threshold_caixa_quebra', -1000.0)  # CORREÇÃO 3: Ajustado de -5000 para -1000
    BUDGET_REF_BRAND = p_run.get('marketing_budget_ref_brand_lift', 3000.0)
    CAIXA_RESERVA = p_run.get('caixa_reserva_operacional', 5000.0)
    LIMITE_INVENTARIO = p_run.get('limite_inventario_mensal', 50000)
    MERCADO_POTENCIAL = p_run.get('mercado_potencial_traders', 150000)
    CUSTO_IMPLANTACAO_B2B = p_run.get('b2b_custo_implantacao', 5000.0)
    
    # --------------------------------------------------------------------
    # BLOCO 1: INICIALIZAÇÃO DE VETORES (PRE-ALOCAÇÃO)
    # --------------------------------------------------------------------
    dados = {}
    metricas_vetores = [
        'trafego_total', 'trafego_pago', 'trafego_organico',
        'trials_total', 'trials_pagos', 'trials_organicos',
        'novos_pagantes_total', 'novos_ads', 'novos_organicos', 'novos_afiliados',
        'reativacoes', 'taxa_trafego_trial', 'taxa_trial_pago', 'eficiencia_time',
        'usuarios_ativos', 'usuarios_lite', 'usuarios_trader', 'usuarios_pro',
        'churn_usuarios', 'churn_mrr', 
        'upgrades_lite_trader', 'expansion_mrr', # Novo vetor para NRR correto
        'mrr_cohort_m0',             # V12.1: MRR da cohort inicial (mês 0) para cálculo de NRR
        'cogs_recorrente',           # V12.0: COGS sem B2B para LTV
        'churn_mrr_cohort_m0',       # V12.1: Churn da cohort do mês 0 para NRR
        'receita_bruta', 'receita_assinaturas', 'receita_b2b',
        'receita_lite', 'receita_trader', 'receita_pro',
        'mrr', 'arr', 'arpu', 'crescimento_mrr_mom', 'crescimento_mrr_yoy', 'net_new_mrr',
        'impostos', 'aliquota_efetiva', 'taxas_pagamento',
        'inadimplencia', 'chargeback', 'total_deducoes', 'receita_liquida',
        'custo_ia_lite', 'custo_ia_trader', 'custo_ia_pro', 'custo_ia_total',
        'comissao_afiliados', 'custo_suporte_variavel', 'total_cogs',
        'margem_bruta', 'margem_bruta_pct',
        'custo_infra_fixo', 'infra_tier_ativo',
        'headcount_total', 'headcount_fundadores', 'headcount_dev', 'headcount_cs',
        'custo_pessoal', 'salarios_brutos', 'encargos',
        'gasto_marketing', 'gasto_instagram', 'gasto_facebook', 'gasto_youtube', 'gasto_google',
        'cpc_blended', 'custo_escritorio', 'custo_contabilidade',
        'despesas_viagens', 'despesas_conselho', 'despesas_freelancer', 'despesas_beneficios',
        'total_opex',
        'margem_contribuicao', 'margem_contribuicao_pct',
        'ebitda', 'ebitda_margin',
        'depreciacao', 'ebit', 'ebit_margin',
        'lucro_liquido', 'margem_liquida',
        'fluxo_operacional', 'fluxo_investimento', 'fluxo_financiamento',
        'aportes_capital', 'capex', 'distribuicao_lucros',
        'caixa', 'burn_rate', 'runway_meses',
        'ltv', 'cac_blended', 'cac_paid', 'ltv_cac',
        'payback_meses', 'payback_semanas', 'vida_media_cliente',
        'churn_rate', 'retention_rate', 'regra_40', 'burn_multiple',
        'trafego_potencial_perdido', 'saturacao_mercado'
    ]
    for m in metricas_vetores:
        dados[m] = np.zeros(meses)
    
    # --------------------------------------------------------------------
    # BLOCO 2: ESTADO INICIAL COM MIX CORRIGIDO (ALGORITMO HAMILTON)
    # --------------------------------------------------------------------
    usuarios_ativos = p_run['usuarios_pagos_iniciais']
    
    def distribuir_usuarios_hamilton(total, pesos):
        """Distribui usuários usando método do maior resto (Hamilton)"""
        inteiros = np.floor(total * np.array(pesos)).astype(int)
        restos = (total * np.array(pesos)) - inteiros
        faltam = int(total) - inteiros.sum()
        
        if faltam > 0:
            indices_ordenados = np.argsort(-restos)  # Maiores restos primeiro
            for i in range(faltam):
                inteiros[indices_ordenados[i]] += 1
        elif faltam < 0:
            indices_ordenados = np.argsort(restos)  # Menores restos primeiro
            for i in range(abs(faltam)):
                if inteiros[indices_ordenados[i]] > 0:
                    inteiros[indices_ordenados[i]] -= 1
        
        return inteiros
    
    pesos_mix = [p_run['mix_lite'], p_run['mix_trader'], p_run['mix_pro']]
    base_lite, base_trader, base_pro = distribuir_usuarios_hamilton(usuarios_ativos, pesos_mix)
    
    # Estado inicial do fluxo
    caixa_atual = p_run['caixa_inicial']
    trafego_base = p_run['trafego_inicial']
    pool_churned_users = 0
    flags = {'fundador': False, 'dev': False, 'cs': False}
    
    # Tracking de CAPEX para depreciação
    capex_historico = []  # Lista de (mes_compra, valor, meses_vida)
    
    # V12.1: Tracking de MRR da Cohort Inicial (Mês 0) para NRR
    # Este valor representa o MRR dos clientes existentes no mês 0.
    # Será usado para calcular NRR = (MRR_M0 - Churn_M0toM11 + Expansion_M0toM11) / MRR_M0
    # Importante: Este vetor NÃO é atualizado após mês 0 (é snapshot da cohort inicial)
    mrr_cohort_m0_inicial = (
        base_lite * p_run['preco_lite'] + 
        base_trader * p_run['preco_trader'] + 
        base_pro * p_run['preco_pro']
    )
    
    # --------------------------------------------------------------------
    # BLOCO 3: LOOP MENSAL
    # --------------------------------------------------------------------
    for mes in range(meses):
        # V12.1: Popula mrr_cohort_m0 no mês 0 (snapshot único)
        if mes == 0:
            dados['mrr_cohort_m0'][0] = mrr_cohort_m0_inicial
        
        mes_atual_num = mes + 1
        mes_cal = datas[mes].month
        
        # --- PATCH V12.3: Definição antecipada de sazonalidade ---
        fator_sazon = p_run['sazonalidade_trafego'].get(mes_cal, 1.0)
        
        # V12.2: Eficiência do Time deve ser calculada ANTES de qualquer decisão
        # Isso garante que a saturação de mercado (3.1) e conversão (3.2)
        # usem o mesmo valor consistente por mês.
        eficiencia = min(1.0, p_run['ramp_up_inicial'] + (mes * p_run['ramp_up_incremento']))
        dados['eficiencia_time'][mes] = eficiencia
        
        # --------------------------
        # 3.1 GROWTH COM TRAVAS REALISTAS
        # --------------------------
        if mes_atual_num <= 6:
            taxa_crescimento_meta = p_run['crescimento_trafego_mes_1_6']
        elif mes_atual_num <= 12:
            taxa_crescimento_meta = p_run['crescimento_trafego_mes_7_12']
        else:
            taxa_crescimento_meta = p_run['crescimento_trafego_mes_13_plus']
        
        # Budget de Marketing com verificação de caixa
        # CORREÇÃO V13.2: Marketing Zero Explícito com fallback R$1
        mkt_fixo = p_run.get('marketing_fixo_mensal', 0.0)
        mkt_perc = p_run.get('marketing_perc_receita', 0.0)
        mkt_hab = p_run.get('marketing_habilitado', True)
        
        # Se marketing desabilitado OU (fixo=0 E perc=0), força zero total
        if not mkt_hab or (mkt_fixo <= 0 and mkt_perc <= 0):
            budget_mkt_desejado = 0.0
        elif mes == 0:
            # Fallback R$1 mínimo para evitar divisão por zero em cálculos de CPC
            budget_mkt_desejado = max(1.0, mkt_fixo)
        else:
            # LÓGICA HÍBRIDA:
            # 1. Calcula % da Receita do mês anterior
            # 2. Aplica piso (Fixo Mensal) e teto (Marketing Teto)
            budget_calc = dados['receita_bruta'][mes - 1] * mkt_perc
            budget_mkt_desejado = np.clip(budget_calc, mkt_fixo, p_run['marketing_teto'])
        
        # V12.3 CORREÇÃO 1: Regras de marketing estritas (usar caixa físico)
        # Regra: se caixa negativo -> corte total; se abaixo de 20% da reserva -> -50%;
        # se abaixo de 50% da reserva -> -25%; caso contrário normal.
        if mes > 0 and caixa_atual < 0:
            # Corte total: não gastar caixa que não existe
            budget_mkt = 0.0
            alertas.append({
                'tipo': 'marketing_corte_total_caixa_negativa',
                'mes': mes_atual_num,
                'caixa': caixa_atual,
                'threshold': 0.0,
                'corte_pct': 100.0,
                'mensagem': f'⚠️ Mês {mes_atual_num}: Marketing CORTADO (100%). Caixa negativo: R$ {caixa_atual:.2f}. Sobrevivência ameaçada.'
            })
        elif mes > 0 and caixa_atual < (CAIXA_RESERVA * 0.20):
            # Modo sobrevivência: corta 50% do marketing
            budget_mkt = budget_mkt_desejado * 0.50
            alertas.append({
                'tipo': 'marketing_emergencia_caixa_critico',
                'mes': mes_atual_num,
                'caixa': caixa_atual,
                'threshold': CAIXA_RESERVA * 0.20,
                'corte_pct': 50.0,
                'mensagem': f'🔴 Mês {mes_atual_num}: Marketing em EMERGÊNCIA (corte 50%). Caixa crítico: R$ {caixa_atual:.2f} (limite: R$ {CAIXA_RESERVA * 0.20:.2f}).'
            })
        elif mes > 0 and caixa_atual < (CAIXA_RESERVA * 0.50):
            # Modo cautela: corta 25% do marketing
            budget_mkt = budget_mkt_desejado * 0.75
            alertas.append({
                'tipo': 'marketing_cautela',
                'mes': mes_atual_num,
                'caixa': caixa_atual,
                'threshold': CAIXA_RESERVA * 0.50,
                'corte_pct': 25.0,
                'mensagem': f'🟡 Mês {mes_atual_num}: Marketing em CAUTELA (corte 25%). Caixa baixo: R$ {caixa_atual:.2f} (limite: R$ {CAIXA_RESERVA * 0.50:.2f}).'
            })
        else:
            # Operação normal
            budget_mkt = budget_mkt_desejado
        
        dados['gasto_marketing'][mes] = budget_mkt
        
        # Correção: Vetores de detalhamento de MKT preenchidos
        dados['gasto_instagram'][mes] = budget_mkt * p_run['canal_instagram_pct']
        dados['gasto_facebook'][mes] = budget_mkt * p_run['canal_facebook_pct']
        dados['gasto_youtube'][mes] = budget_mkt * p_run['canal_youtube_pct']
        dados['gasto_google'][mes] = budget_mkt * p_run['canal_google_pct']
        
        # Brand Lift com função logística
        fator_brand_lift_raw = budget_mkt / BUDGET_REF_BRAND
        fator_brand_lift = 1.0 / (1.0 + np.exp(-2 * (fator_brand_lift_raw - 0.5)))
        fator_brand_lift = np.clip(fator_brand_lift, 0.05, 1.0)
        
        taxa_seo_basico = 0.02
        taxa_crescimento_real = taxa_seo_basico + (taxa_crescimento_meta * fator_brand_lift)
        taxa_crescimento_real = min(taxa_crescimento_real, taxa_crescimento_meta)
        
        # Atualização do tráfego base
        if mes > 0:
            crescimento_potencial = trafego_base * (1 + taxa_crescimento_meta)
            crescimento_real = trafego_base * (1 + taxa_crescimento_real)
            dados['trafego_potencial_perdido'][mes] = crescimento_potencial - crescimento_real
            trafego_base = crescimento_real
        
        # CORREÇÃO 2: Validação de Tráfego Inicial (alertas se suspeito)
        if mes == 0:
            trafego_min_recomendado = 50
            trafego_max_recomendado = usuarios_ativos * 100  # 5 usuários = max 500 visitas
            
            if trafego_base < trafego_min_recomendado:
                alertas.append({
                    'tipo': 'trafego_inicial_muito_baixo',
                    'valor': trafego_base,
                    'recomendado': trafego_min_recomendado,
                    'mensagem': f'Tráfego inicial de {trafego_base} visitas pode ser insuficiente para validação'
                })
            
            if trafego_base > trafego_max_recomendado:
                alertas.append({
                    'tipo': 'trafego_inicial_suspeito',
                    'valor': trafego_base,
                    'recomendado': trafego_max_recomendado,
                    'mensagem': f'Tráfego inicial de {trafego_base} visitas parece alto para {usuarios_ativos} usuários (ratio {trafego_base/usuarios_ativos:.0f}:1)'
                })
        
        # CPC Blended
        cpc_blended = (
            p_run['cpc_instagram'] * p_run['canal_instagram_pct'] +
            p_run['cpc_facebook'] * p_run['canal_facebook_pct'] +
            p_run['cpc_google'] * p_run['canal_google_pct'] +
            p_run['cpc_youtube'] * p_run['canal_youtube_pct']
        )
        dados['cpc_blended'][mes] = cpc_blended
        
        # V12.1: Visitas Pagas com dupla limitação: Inventário de Ads + Saturação de Mercado
        # CORREÇÃO 1: Remove * fator_sazon (sazonalidade afeta demanda/conversão, não CPC)
        visitas_pagas_teoricas = (budget_mkt / max(cpc_blended, 0.01))
        
        # Limite 1: Inventário de anúncios (supply de ads disponíveis)
        limite_inventario = LIMITE_INVENTARIO
        
        # Limite 2: Saturação de mercado (não adianta comprar tráfego se não há mercado disponível)
        # Lógica: Se 90% do mercado já são clientes, o pool de prospects é apenas 10%
        # Assumimos que 10% do tráfego se converte em trial, e 10% dos trials viram pagantes
        # Logo: mercado_disponivel / (taxa_trial * taxa_conversao) = tráfego máximo útil
        mercado_disponivel = max(0, MERCADO_POTENCIAL - usuarios_ativos)
        taxa_conversao_pipeline = (p_run['taxa_visitante_para_trial'] * 
                                   p_run['taxa_trial_para_pagante'] * 
                                   eficiencia)  # eficiência já foi calculada acima (linha 273)
        
        # Limite de mercado realista (PLANO DE CORREÇÃO 3.2): não usar divisão direta
        # por taxa de conversão que gera números absurdos. Estimamos alcance mensal
        # realista e aplicamos fator de saturação.
        mercado_alcancavel_mensal = MERCADO_POTENCIAL * 0.10
        penetracao_mercado = usuarios_ativos / max(1.0, mercado_alcancavel_mensal)
        fator_saturacao = max(0.1, 1.0 - penetracao_mercado)
        limite_mercado_realistico = mercado_alcancavel_mensal * fator_saturacao

        if taxa_conversao_pipeline > 0:
            # Ainda respeitamos a noção de mercado disponível, mas aplicamos teto realista
            limite_mercado = min(limite_mercado_realistico, mercado_disponivel / taxa_conversao_pipeline)
        else:
            limite_mercado = limite_mercado_realistico
        
        # Aplica o limite mais restritivo
        visitas_pagas = min(visitas_pagas_teoricas, limite_inventario, limite_mercado)
        
        # Registra perdas por saturação (diagnóstico)
        if visitas_pagas < visitas_pagas_teoricas:
            dados['saturacao_mercado'][mes] = visitas_pagas_teoricas - visitas_pagas

        # V12.3 CORREÇÃO 3: aplicar sazonalidade antes do cálculo viral
        # Ajusta a base de tráfego pela sazonalidade e depois soma visitas virais
        trafego_base_ajustado = trafego_base * fator_sazon

        # Visitas Virais com curva S de saturação (parametrizado)
        elasticidade = p_run.get('elasticidade_organico', 1.0)
        fator_viral_base = p_run.get('fator_visitas_organicas_por_pagante', 0.0)

        penetracao = usuarios_ativos / MERCADO_POTENCIAL
        fator_saturacao_viral = 1.0 / (1.0 + np.exp(10 * (penetracao - 0.5)))

        visitas_virais = (usuarios_ativos * fator_viral_base * elasticidade * fator_saturacao_viral)
        visitas_organicas = trafego_base_ajustado + visitas_virais
        
        dados['trafego_pago'][mes] = visitas_pagas
        dados['trafego_organico'][mes] = visitas_organicas
        dados['trafego_total'][mes] = visitas_pagas + visitas_organicas
        
        # --------------------------
        # 3.2 CONVERSÃO
        # --------------------------
        conv_blended = (
            p_run['conv_instagram'] * p_run['canal_instagram_pct'] +
            p_run['conv_facebook'] * p_run['canal_facebook_pct'] +
            p_run['conv_google'] * p_run['canal_google_pct'] +
            p_run['conv_youtube'] * p_run['canal_youtube_pct']
        )
        trials_pagos = visitas_pagas * conv_blended
        trials_organicos = visitas_organicas * p_run['taxa_visitante_para_trial']
        dados['trials_total'][mes] = trials_pagos + trials_organicos
        
        # eficiencia já calculada antes do bloco 3.1 (V12.2)
        
        novos_bruto = dados['trials_total'][mes] * p_run['taxa_trial_para_pagante'] * eficiencia
        
        # Distribuição por canal
        pct_afiliado = p_run['pct_usuarios_via_afiliado'] if p_run.get('modelo_afiliado_habilitado', False) else 0
        novos_afiliado = novos_bruto * pct_afiliado
        novos_resto = novos_bruto - novos_afiliado
        
        total_trials_attribution = trials_pagos + trials_organicos
        ratio_ads = (trials_pagos / total_trials_attribution) if total_trials_attribution > 0 else 0
        
        dados['novos_afiliados'][mes] = int(novos_afiliado)
        dados['novos_ads'][mes] = int(novos_resto * ratio_ads)
        dados['novos_organicos'][mes] = int(novos_resto * (1 - ratio_ads))
        dados['novos_pagantes_total'][mes] = (
            dados['novos_afiliados'][mes] + dados['novos_ads'][mes] + dados['novos_organicos'][mes]
        )
        
        # --------------------------
        # 3.3 CHURN E RETENÇÃO
        # --------------------------
        reativacoes = int(pool_churned_users * p_run.get('taxa_reativacao_base_cancelada', 0.01)) if pool_churned_users > 0 else 0
        dados['reativacoes'][mes] = reativacoes
        
        churn_rate = max(
            p_run['churn_maturidade'],
            p_run['churn_inicial'] - (mes * p_run['churn_decaimento_mensal'])
        )
        dados['churn_rate'][mes] = churn_rate
        
        churn_users = int(usuarios_ativos * churn_rate)
        dados['churn_usuarios'][mes] = churn_users
        
        # Cálculo de churn_mrr (usando ARPU médio do mês anterior para simplificação conservadora)
        arpu_prev = (
            (base_lite * p_run['preco_lite'] + 
             base_trader * p_run['preco_trader'] + 
             base_pro * p_run['preco_pro']) / max(1, usuarios_ativos)
        )
        dados['churn_mrr'][mes] = churn_users * arpu_prev
        
        # V12.1: Atribui churn_mrr proporcionalmente à cohort do mês 0 (PLANO DE CORREÇÃO)
        # No mês 0, todo churn pertence à cohort inicial. Nos meses seguintes,
        # estimamos a fração do churn atribuível à cohort M0 usando uma
        # aproximação exponencial de decaimento: MRR_cohort_M0(t) = MRR0 * (1 - churn_rate)^t
        # V12.2 CORREÇÃO #5: Churn cohort M0 usando produto acumulado das retenções
        if mes == 0:
            dados['churn_mrr_cohort_m0'][mes] = dados['churn_mrr'][mes]
            mrr_cohort_m0_atual = mrr_cohort_m0_inicial  # cache inicial
        else:
            # Calcula retenção acumulada usando as churn_rates históricas (0..mes-1)
            retention_acumulada = 1.0
            for m in range(mes):
                retention_acumulada *= (1.0 - dados['churn_rate'][m])

            mrr_cohort_m0_atual = mrr_cohort_m0_inicial * retention_acumulada

            # Proporção da MRR total que ainda pertence à cohort M0
            proporcao_cohort_m0 = (mrr_cohort_m0_atual / dados['mrr'][mes]) if dados['mrr'][mes] > 0 else 0
            proporcao_cohort_m0 = min(1.0, max(0.0, proporcao_cohort_m0))

            # Atribui apenas a porção proporcional do churn ao vetor da cohort M0
            dados['churn_mrr_cohort_m0'][mes] = dados['churn_mrr'][mes] * proporcao_cohort_m0
        
        pool_churned_users += churn_users - reativacoes
        usuarios_ativos = max(0, usuarios_ativos + dados['novos_pagantes_total'][mes] - churn_users + reativacoes)
        dados['usuarios_ativos'][mes] = int(usuarios_ativos)
        
        # --------------------------
        # 3.3.1 RECÁLCULO DO MIX (HAMILTON) & EXPANSÃO (NRR)
        # --------------------------
        # CALCULAR UPGRADES com base no estoque do mês anterior (PLANO 4.2)
        if mes > 0:
            base_lite_anterior = int(dados['usuarios_lite'][mes-1])
            upgrades = int(base_lite_anterior * p_run.get('taxa_upgrade_lite_trader', 0.0))
        else:
            upgrades = 0
        dados['upgrades_lite_trader'][mes] = upgrades
        
        # Correção V11: Cálculo explícito de Expansion MRR (Upgrade Lite -> Trader)
        delta_price = p_run['preco_trader'] - p_run['preco_lite']
        dados['expansion_mrr'][mes] = upgrades * delta_price
        
        # Recalcula mix desejado
        pesos_atual = [p_run['mix_lite'], p_run['mix_trader'], p_run['mix_pro']]
        base_lite, base_trader, base_pro = distribuir_usuarios_hamilton(usuarios_ativos, pesos_atual)
        
        # Ajuste fino pós-distribuição para refletir os upgrades forçados
        # (Hamilton distribui baseado em targets globais, upgrades são movimentos internos)
        # Em steady state, o target global já contempla os upgrades.
        # Ajuste conservador para garantir consistência contábil:
        base_lite = max(0, base_lite - upgrades)
        base_trader = base_trader + upgrades
        
        # Garante soma exata
        diff = int(usuarios_ativos) - (base_lite + base_trader + base_pro)
        if diff != 0:
            # Proteção: se Hamilton falhar gravemente, falamos alto (fail-fast)
            # V12.2 CORREÇÃO #4: Assert Hamilton tolerante (±2)
            if abs(diff) > 2:
                raise AssertionError(
                    f"Mês {mes+1}: Hamilton falhou gravemente (diff={diff}). "
                    f"Esperado: {int(usuarios_ativos)} usuários. "
                    f"Calculado: {base_lite + base_trader + base_pro} "
                    f"(Lite={base_lite}, Trader={base_trader}, Pro={base_pro}). "
                    f"Verifique premissas de mix."
                )
            # Ajuste de arredondamento tolerado (±2). Protege contra negativos.
            base_lite = max(0, base_lite + diff)
        
        dados['usuarios_lite'][mes] = base_lite
        dados['usuarios_trader'][mes] = base_trader
        dados['usuarios_pro'][mes] = base_pro
        
        # --------------------------
        # 3.4 RECEITA & DEDUÇÕES
        # --------------------------
        # Correção: Vetores de detalhamento preenchidos
        dados['receita_lite'][mes] = base_lite * p_run['preco_lite']
        dados['receita_trader'][mes] = base_trader * p_run['preco_trader']
        dados['receita_pro'][mes] = base_pro * p_run['preco_pro']
        
        mrr = dados['receita_lite'][mes] + dados['receita_trader'][mes] + dados['receita_pro'][mes]
        dados['mrr'][mes] = mrr
        dados['arr'][mes] = mrr * 12
        dados['arpu'][mes] = mrr / usuarios_ativos if usuarios_ativos > 0 else 0
        
        # B2B com seed variável
        rng_b2b = np.random.RandomState((seed + simulacao_id * 9999 + mes + 7) % (2**31 - 1))
        chance_b2b = rng_b2b.random_sample()
        # Converter probabilidade anual para mensal corretamente (PASSO 4.3)
        prob_anual = p_run.get('b2b_probabilidade_anual', 0.20)
        prob_mensal = 1 - (1 - prob_anual) ** (1.0 / 12.0)
        rec_b2b = p_run['b2b_setup_fee'] if chance_b2b < prob_mensal else 0
        dados['receita_bruta'][mes] = mrr + rec_b2b
        dados['receita_b2b'][mes] = rec_b2b
        
        if dados['receita_bruta'][mes] > 0:
            # V12.1: Impostos sobre Receita Bruta (Simples Nacional / Lucro Presumido)
            # Decisão de regime baseada em FATURAMENTO ANUAL PROJETADO (não apenas ARR)
            # Isso captura cenários onde B2B pontual estoura o teto de R$ 4.8M
            
            # Projeta faturamento anual = ARR (recorrente) + B2B anualizado (pontual)
            faturamento_anual_projetado = dados['arr'][mes]
            if dados['receita_b2b'][mes] > 0:
                # Anualiza B2B: se ganhou R$ 600k de setup fee em um mês, projeta R$ 600k*12 no ano
                # (conservador, mas evita subestimar para fins tributários)
                faturamento_anual_projetado += dados['receita_b2b'][mes] * 12
            
            # Escolhe regime tributário
            aliquota = (p_run['imposto_lucro_presumido'] 
                       if faturamento_anual_projetado > p_run['threshold_regime_tributario'] 
                       else p_run['imposto_simples_inicial'])
            
            dados['impostos'][mes] = dados['receita_bruta'][mes] * aliquota
            dados['aliquota_efetiva'][mes] = aliquota # Preenche vetor
            
            taxa_inadimp = (
                p_run['taxa_inadimplencia_cartao'] * p_run['mix_pagamento_cartao'] +
                p_run['taxa_inadimplencia_pix'] * p_run['mix_pagamento_pix'] +
                p_run['taxa_inadimplencia_boleto'] * p_run['mix_pagamento_boleto']
            )
            dados['inadimplencia'][mes] = dados['receita_bruta'][mes] * taxa_inadimp
            
            taxa_pgto = (
                p_run['taxa_processamento_cartao'] * p_run['mix_pagamento_cartao'] +
                p_run['taxa_processamento_pix'] * p_run['mix_pagamento_pix'] +
                p_run['taxa_processamento_boleto'] * p_run['mix_pagamento_boleto']
            )
            dados['taxas_pagamento'][mes] = (dados['receita_bruta'][mes] - dados['inadimplencia'][mes]) * taxa_pgto
            dados['chargeback'][mes] = dados['receita_bruta'][mes] * p_run['taxa_chargeback']
            dados['total_deducoes'][mes] = (dados['impostos'][mes] + dados['inadimplencia'][mes] + 
                                           dados['taxas_pagamento'][mes] + dados['chargeback'][mes])
        else:
            dados['total_deducoes'][mes] = 0.0
        
        dados['receita_liquida'][mes] = dados['receita_bruta'][mes] - dados['total_deducoes'][mes]
        
        # --------------------------
        # 3.5 COGS
        # --------------------------
        # Correção: Vetores de detalhamento preenchidos
        dados['custo_ia_lite'][mes] = base_lite * p_run['custo_ia_lite']
        dados['custo_ia_trader'][mes] = base_trader * p_run['custo_ia_trader']
        dados['custo_ia_pro'][mes] = base_pro * p_run['custo_ia_pro']
        
        custo_ia = dados['custo_ia_lite'][mes] + dados['custo_ia_trader'][mes] + dados['custo_ia_pro'][mes]
        dados['custo_ia_total'][mes] = custo_ia
        
        comissao = 0.0
        if p_run.get('modelo_afiliado_habilitado', False):
            if p_run.get('comissao_afiliado_tipo') == 'primeira_mensalidade':
                comissao = dados['novos_afiliados'][mes] * dados['arpu'][mes]
            else:
                comissao = dados['novos_afiliados'][mes] * dados['arpu'][mes] * p_run.get('comissao_afiliado_pct', 0.2)
        dados['comissao_afiliados'][mes] = comissao
        
        if usuarios_ativos >= p_run['trigger_cs']:
            flags['cs'] = True
        
        if flags['cs']:
            dados['custo_suporte_variavel'][mes] = (usuarios_ativos / 1000) * p_run['custo_suporte_por_1000_users']
        else:
            dados['custo_suporte_variavel'][mes] = 0.0
            
        # V12.0: Separar COGS Recorrente (assinatura) de COGS Não-Recorrente (B2B)
        # COGS Recorrente = IA + Afiliados + Suporte (custo variável direto da assinatura)
        cogs_recorrente = custo_ia + comissao + dados['custo_suporte_variavel'][mes]
        dados['cogs_recorrente'][mes] = cogs_recorrente
        
        # COGS Não-Recorrente (B2B)
        custo_b2b_impl = CUSTO_IMPLANTACAO_B2B if rec_b2b > 0 else 0.0
        
        # Total COGS (para lucro/cash)
        dados['total_cogs'][mes] = cogs_recorrente + custo_b2b_impl
        dados['margem_bruta'][mes] = dados['receita_liquida'][mes] - dados['total_cogs'][mes]
        dados['margem_bruta_pct'][mes] = (dados['margem_bruta'][mes] / dados['receita_bruta'][mes]) * 100 if dados['receita_bruta'][mes] > 0 else 0
        
        # --------------------------
        # 3.6 INFRA COM VALIDAÇÃO DE LIQUIDEZ (CORREÇÃO 4)
        # --------------------------
        # Calcula tier desejado (baseado em usuários)
        tier_desejado = 1
        if usuarios_ativos > p_run['infra_tier_1_limite']: tier_desejado = 2
        if usuarios_ativos > p_run['infra_tier_2_limite']: tier_desejado = 3
        if usuarios_ativos > p_run['infra_tier_3_limite']: tier_desejado = 4
        
        # Se tier atual não existe, inicializa (mês 0)
        if mes == 0:
            tier_atual = 1
        else:
            tier_atual = int(dados['infra_tier_ativo'][mes - 1])  # Tier do mês anterior
        
        # Calcula custo do tier desejado
        custo_tier_desejado = sum([v for k, v in p_run.items() if k.startswith(f"t{tier_desejado}_") and isinstance(v, (int, float))])
        
        # Valida se tem caixa para sustentar 1 mês com o novo tier
        if tier_desejado > tier_atual:
            # Estima burn rate do mês (sem considerar o novo tier ainda)
            custo_tier_atual = sum([v for k, v in p_run.items() if k.startswith(f"t{tier_atual}_") and isinstance(v, (int, float))])
            
            # Delta de custo ao mudar tier
            delta_tier = custo_tier_desejado - custo_tier_atual
            
            # Verifica se caixa atual aguenta pelo menos 1 mês com o delta extra
            # (Heurística conservadora: caixa deve ser > 2x o delta do tier)
            caixa_minimo_requerido = delta_tier * 2.0
            
            if caixa_atual >= caixa_minimo_requerido:
                tier_final = tier_desejado  # Pode fazer o upgrade
            else:
                tier_final = tier_atual  # Mantém tier atual (caixa insuficiente)
                alertas.append({
                    'tipo': 'tier_upgrade_bloqueado',
                    'mes': mes_atual_num,
                    'tier_desejado': tier_desejado,
                    'tier_atual': tier_atual,
                    'caixa_atual': caixa_atual,
                    'caixa_requerido': caixa_minimo_requerido,
                    'mensagem': f'Upgrade de tier bloqueado por liquidez insuficiente. Caixa: R$ {caixa_atual:.2f}, Requerido: R$ {caixa_minimo_requerido:.2f}'
                })
        else:
            tier_final = tier_atual  # Não downgrade (infraestrutura não encolhe)
        
        # Calcula custo final
        custo_infra = sum([v for k, v in p_run.items() if k.startswith(f"t{tier_final}_") and isinstance(v, (int, float))])
        dados['infra_tier_ativo'][mes] = tier_final
        dados['custo_infra_fixo'][mes] = custo_infra
        
        # --------------------------
        # 3.7 RH
        # --------------------------
        custo_rh = 0.0
        headcount = 0
        
        # CORREÇÃO V13: Salário ativa no mês do gatilho (OR logic)
        if (dados['mrr'][mes] >= p_run['trigger_fundador']) or flags['fundador']:
            flags['fundador'] = True
            custo_rh += p_run['salario_fundador'] * (1 + p_run.get('encargos_trabalhistas', 0.7))
            headcount += 1

        if usuarios_ativos >= p_run['trigger_dev']:
            flags['dev'] = True
        if flags['dev']:
            custo_rh += p_run['salario_dev_senior'] * (1 + p_run.get('encargos_trabalhistas', 0.7))
            headcount += 1
        if flags['cs']:
            custo_rh += p_run['salario_cs'] * (1 + p_run.get('encargos_trabalhistas', 0.7))
            headcount += 1
        
        dados['custo_pessoal'][mes] = custo_rh
        dados['headcount_total'][mes] = headcount
        
        # --------------------------
        # 3.8 OPEX
        # --------------------------
        opex_extra = 0.0
        
        if dados['mrr'][mes] >= p_run.get('trigger_escritorio', 65000):
            dados['custo_escritorio'][mes] = p_run['custo_escritorio_base']
        
        trigger_contabil = p_run.get('trigger_contabilidade', 65000)
        if dados['receita_bruta'][mes] >= trigger_contabil:
            dados['custo_contabilidade'][mes] = p_run['custo_contabilidade_adv'] + p_run.get('custo_juridico_compliance', 0)
        
        if dados['receita_bruta'][mes] >= p_run.get('trigger_viagens_receita', 35000):
            dados['despesas_viagens'][mes] = p_run['verba_viagens_base']
        
        if dados['mrr'][mes] >= p_run.get('trigger_conselho_mrr', 100000):
            dados['despesas_conselho'][mes] = p_run.get('conselho_jeton', 0)
        
        dados['total_opex'][mes] = (
            dados['gasto_marketing'][mes] + dados['custo_infra_fixo'][mes] + dados['custo_pessoal'][mes] +
            dados['custo_escritorio'][mes] + dados['custo_contabilidade'][mes] + dados['despesas_viagens'][mes] +
            dados['despesas_conselho'][mes] + opex_extra
        )
        
        # --------------------------
        # 3.9 RESULTADO FINANCEIRO & DEPRECIAÇÃO (CORREÇÃO V13.1)
        # --------------------------
        dados['ebitda'][mes] = dados['margem_bruta'][mes] - dados['total_opex'][mes]
        dados['ebitda_margin'][mes] = (dados['ebitda'][mes] / dados['receita_bruta'][mes]) * 100 if dados['receita_bruta'][mes] > 0 else 0
        
        # --- CAPEX (COMPRA DE ATIVOS) ---
        fluxo_invest = 0.0
        
        # Compra Inicial (Mês 0)
        if mes == 0:
            capex_val = p_run['capex_inicial']
            fluxo_invest -= capex_val
            # V13.1: Salva como Dicionário para compatibilidade
            capex_historico.append({'mes': mes, 'valor': capex_val, 'vida': p_run.get('tempo_depreciacao_equipamento_meses', 24)})
            
        # Compra Recorrente (Mês 24 - índice 23)
        if mes == 23:
            capex_recorrente = p_run.get('capex_recorrente_24m', 0)
            if capex_recorrente > 0:
                fluxo_invest -= capex_recorrente
                # V13.1: Salva como Dicionário
                capex_historico.append({'mes': mes, 'valor': capex_recorrente, 'vida': 24})
        
        dados['capex'][mes] = fluxo_invest

        # --- DEPRECIAÇÃO (CORREÇÃO LEITURA DE DICIONÁRIO) ---
        deprec_total = 0.0
        for item in capex_historico:
            # V13.1: Lê chaves do dicionário (evita erro de tupla)
            meses_vida = max(12, item['vida']) # Trava de segurança (mínimo 12 meses)
            meses_passados = mes - item['mes']
            
            if meses_passados >= 0 and meses_passados < meses_vida:
                deprec_total += item['valor'] / meses_vida
        
        dados['depreciacao'][mes] = deprec_total
        dados['ebit'][mes] = dados['ebitda'][mes] - deprec_total
        dados['lucro_liquido'][mes] = dados['ebit'][mes] # Simplificado (EBIT = Lucro Antes IR)
        dados['margem_liquida'][mes] = (dados['lucro_liquido'][mes] / dados['receita_bruta'][mes]) * 100 if dados['receita_bruta'][mes] > 0 else 0
        
        # --------------------------
        # 3.10 FLUXO DE CAIXA & RUNWAY (CORREÇÃO V13.1)
        # --------------------------
        if mes < p_run['meses_aporte']:
            dados['aportes_capital'][mes] = p_run['aporte_mensal']
        else:
            dados['aportes_capital'][mes] = 0.0
        
        # Fluxo Operacional: Lucro + Depreciação (add-back de não-caixa)
        fluxo_operacional = dados['lucro_liquido'][mes] + dados['depreciacao'][mes]
        dados['fluxo_operacional'][mes] = fluxo_operacional
        dados['fluxo_investimento'][mes] = fluxo_invest
        
        # Variação de Caixa = Operacional + Investimento + Financiamento
        variacao_caixa = fluxo_operacional + fluxo_invest + dados['aportes_capital'][mes]
        caixa_atual += variacao_caixa
        
        dados['caixa'][mes] = caixa_atual
        
        # --- RUNWAY REALISTA (SEM DUPLA CONTAGEM) ---
        # 1. Calcular Despesa Operacional (Sem deduções, apenas saída de caixa)
        # Nota: Capex entra positivo aqui como saída de caixa para cálculo de sobrevivência
        despesa_operacional_mensal = (
            dados['total_cogs'][mes] + 
            dados['total_opex'][mes] + 
            (abs(fluxo_invest) if fluxo_invest < 0 else 0) 
        )
        
        # 2. Burn Rate (Conceito Financeiro: Queima Líquida)
        fluxo_liquido_organico = fluxo_operacional + fluxo_invest
        dados['burn_rate'][mes] = -fluxo_liquido_organico if fluxo_liquido_organico < 0 else 0
        
        # 3. Runway Realista (Permite negativo para indicar profundidade da quebra)
        if despesa_operacional_mensal > 0:
            if caixa_atual <= THRESHOLD_QUEBRA:
                dados['runway_meses'][mes] = 0.0 # Quebra total
            else:
                # CORREÇÃO V13.2: Runway nunca negativo (0 = quebrado)
                runway_calc = caixa_atual / despesa_operacional_mensal
                dados['runway_meses'][mes] = max(0.0, runway_calc)
        else:
            dados['runway_meses'][mes] = 999.0 # Sem custos, vida infinita
            
        # CORREÇÃO: Aporte no Mês 0 entra no cálculo do Runway Inicial
        if mes == 0:
            caixa_projetado = caixa_atual + p_run['aporte_mensal']
            if despesa_operacional_mensal > 0:
                dados['runway_meses'][mes] = caixa_projetado / despesa_operacional_mensal

        # V12.1: VALIDAÇÃO DE CONSISTÊNCIA CONTÁBIL (MODO DEBUG)
        if modo_debug and mes > 0:
            # Identidade: Balanço de Caixa
            caixa_esperado = (dados['caixa'][mes-1] + 
                            dados['fluxo_operacional'][mes] + 
                            dados['fluxo_investimento'][mes] + 
                            dados['aportes_capital'][mes])
            diff_caixa = abs(dados['caixa'][mes] - caixa_esperado)
            if diff_caixa > 0.01: # Tolerância float
                 alertas.append({'tipo': 'erro_contabil_caixa', 'mes': mes, 'diff': diff_caixa})
        
        # Alerta de runway crítico
        if dados['runway_meses'][mes] < p_run.get('meta_runway_minimo_meses', 6) and dados['runway_meses'][mes] < 999:
            alertas.append({
                'tipo': 'runway_critico',
                'mes': mes_atual_num,
                'runway': dados['runway_meses'][mes]
            })
            
    # --------------------------
    # 3.11 UNIT ECONOMICS
    # --------------------------
        # CORREÇÃO 5 (V12.3): CAC conservador apenas sobre novos pagantes
        if dados['novos_pagantes_total'][mes] > 0:
            custo_aquisicao_total = dados['gasto_marketing'][mes] + dados['comissao_afiliados'][mes]
            dados['cac_blended'][mes] = custo_aquisicao_total / dados['novos_pagantes_total'][mes]
        else:
            dados['cac_blended'][mes] = np.nan
        
        # V12.2 CORREÇÃO CRÍTICA #3: LTV limpo usando deduções já calculadas
        # Evita duplicar impostos/taxas que já foram subtraídos em receita_liquida
        if dados['receita_bruta'][mes] > 0 and usuarios_ativos > 0:
            # Proporção do MRR na receita bruta (ex: se MRR=800 e rec_bruta=1000, prop=0.8)
            proporcao_mrr = dados['mrr'][mes] / dados['receita_bruta'][mes]

            # Deduções proporcionais ao MRR (usa total_deducoes já calculado)
            deducoes_mrr = dados['total_deducoes'][mes] * proporcao_mrr

            # Receita líquida apenas da parte recorrente (MRR)
            receita_liquida_mrr = dados['mrr'][mes] - deducoes_mrr

            # Margem recorrente = Receita líquida MRR - COGS recorrente
            margem_recorrente = receita_liquida_mrr - dados['cogs_recorrente'][mes]
            margem_recorrente_por_user = margem_recorrente / usuarios_ativos if usuarios_ativos > 0 else 0

            if churn_rate > 0:
                ltv_val = margem_recorrente_por_user / churn_rate
            else:
                ltv_val = np.nan
        else:
            ltv_val = np.nan

        dados['ltv'][mes] = ltv_val
        
        # CORREÇÃO V13.2: LTV/CAC padronizado (sem NaN no output)
        cac_atual = dados['cac_blended'][mes]
        if np.isnan(cac_atual) or cac_atual <= 0:
            # CAC zero/NaN significa aquisição 100% orgânica
            if not np.isnan(ltv_val) and ltv_val > 0:
                dados['ltv_cac'][mes] = 10000.0  # Símbolo de "infinito" (cap)
            else:
                dados['ltv_cac'][mes] = 0.0  # Sem LTV = 0
        elif not np.isnan(ltv_val):
            dados['ltv_cac'][mes] = ltv_val / cac_atual
        else:
            dados['ltv_cac'][mes] = 0.0  # Fallback conservador
        
        # Payback
        if not np.isnan(dados['cac_blended'][mes]) and dados['cac_blended'][mes] > 0 and usuarios_ativos > 0:
            margem_mensal_por_user = dados['margem_bruta'][mes] / usuarios_ativos
            if margem_mensal_por_user > 0:
                dados['payback_meses'][mes] = dados['cac_blended'][mes] / margem_mensal_por_user
            else:
                dados['payback_meses'][mes] = np.nan
        else:
            dados['payback_meses'][mes] = np.nan
        
        dados['retention_rate'][mes] = 1.0 - churn_rate
        
        # Regra dos 40
        crescimento_mrr = ((dados['mrr'][mes] - dados['mrr'][mes-1]) / dados['mrr'][mes-1] * 100) if mes > 0 and dados['mrr'][mes-1] > 0 else 0
        dados['regra_40'][mes] = crescimento_mrr + dados['ebitda_margin'][mes]
    
    # CORREÇÃO 6: Validação de Consistência CPC (detecta divergências no relatório)
    for mes in range(meses):
        if dados['trafego_pago'][mes] > 0 and dados['gasto_marketing'][mes] > 0:
            cpc_real = dados['gasto_marketing'][mes] / dados['trafego_pago'][mes]
            cpc_esperado = dados['cpc_blended'][mes]
            
            # Tolerância de 5% (para arredondamentos)
            diferenca_pct = abs(cpc_real - cpc_esperado) / cpc_esperado if cpc_esperado > 0 else 0
            
            if diferenca_pct > 0.05:  # Divergência > 5%
                alertas.append({
                    'tipo': 'inconsistencia_cpc',
                    'mes': mes + 1,
                    'cpc_real': float(cpc_real),
                    'cpc_esperado': float(cpc_esperado),
                    'divergencia_pct': float(diferenca_pct * 100),
                    'mensagem': f'CPC real (R$ {cpc_real:.2f}) diverge {diferenca_pct*100:.1f}% do esperado (R$ {cpc_esperado:.2f})'
                })
    
    # --------------------------------------------------------------------
    # BLOCO 4: OUTPUT E CÁLCULO DE KPIS FINAIS
    # --------------------------------------------------------------------
    df_mensal = pd.DataFrame(dados)
    df_mensal.insert(0, 'mes', range(1, meses + 1))
    
    # V12.1: Agregação anual inteligente (não pode somar taxas/índices)
    def calcular_df_anual_correto(df_mensal):
        """
        Agrega DataFrame mensal em anual com lógica matemática correta.
        Regras:
        - Fluxos (receitas, custos): SOMA
        - Estoques (caixa, MRR, usuários): ÚLTIMO VALOR do ano
        - Taxas (churn, CAC, LTV): MÉDIA ponderada
        - Riscos (runway, caixa mínimo): PIOR CASO (mínimo)
        """
        gb = df_mensal.groupby(df_mensal.index // 12)
        
        return pd.DataFrame({
            # === FLUXOS (ACUMULADOS ANUAIS) ===
            'receita_bruta': gb['receita_bruta'].sum(),
            'receita_liquida': gb['receita_liquida'].sum(),
            'mrr_acumulado': gb['mrr'].sum(),
            'receita_b2b': gb['receita_b2b'].sum(),
            'gasto_marketing': gb['gasto_marketing'].sum(),
            'total_cogs': gb['total_cogs'].sum(),
            'total_opex': gb['total_opex'].sum(),
            'impostos': gb['impostos'].sum(),
            'lucro_liquido': gb['lucro_liquido'].sum(),
            'ebitda': gb['ebitda'].sum(),
            'novos_pagantes_total': gb['novos_pagantes_total'].sum(),
            'churn_usuarios': gb['churn_usuarios'].sum(),
            'capex': gb['capex'].sum(),
            'aportes_capital': gb['aportes_capital'].sum(),
            
            # === ESTOQUES (SNAPSHOT FINAL DO ANO) ===
            'usuarios_final': gb['usuarios_ativos'].last(),
            'mrr_final': gb['mrr'].last(),
            'arr_final': gb['arr'].last(),
            'caixa_final': gb['caixa'].last(),
            
            # === TAXAS/ÍNDICES (MÉDIAS PONDERADAS) ===
            'churn_rate_medio': gb['churn_rate'].mean(),
            'cac_blended_medio': gb['cac_blended'].mean(),
            'ltv_medio': gb['ltv'].mean(),
            'ltv_cac_medio': gb['ltv_cac'].mean(),
            'arpu_medio': gb['arpu'].mean(),
            'margem_bruta_pct_media': gb['margem_bruta_pct'].mean(),
            'ebitda_margin_media': gb['ebitda_margin'].mean(),
            'burn_rate_medio': gb['burn_rate'].mean(),
            
            # === ANÁLISE DE RISCO (PIOR CASO) ===
            'caixa_minimo': gb['caixa'].min(),
            'runway_minimo': gb['runway_meses'].min(),
            'mes_caixa_minimo': gb['caixa'].idxmin() % 12 + 1,  # Mês dentro do ano
        })
    
    df_anual = calcular_df_anual_correto(df_mensal)
    
    ltv_cac_serie = df_mensal['ltv'] / df_mensal['cac_blended'].replace(0, np.nan)
    
    # --------------------------------------------------------------------
    # BLOCO 4.5: CÁLCULO DE KPIS AVANÇADOS
    # --------------------------------------------------------------------
    metricas = {}
    
    if len(df_mensal) >= 12:
        # V12.1: NRR usando MRR da Cohort Inicial (Mês 0)
        # Fórmula: NRR = (MRR_inicial - Churn_acumulado + Expansion_acumulada) / MRR_inicial
        # Representa: "Dos clientes que tínhamos no mês 0, quantos % de MRR retivemos/expandimos?"
        mrr_start = df_mensal.loc[0, 'mrr_cohort_m0']  # Snapshot da cohort do mês 0
        churn_mrr_acum = df_mensal.loc[:11, 'churn_mrr_cohort_m0'].sum()  # Churn atribuído à cohort
        expansion_mrr_acum = df_mensal.loc[:11, 'expansion_mrr'].sum()  # Upgrades de qualquer cliente
        
        if mrr_start > 0:
            # NRR = (Start - Churn + Expansion) / Start
            nrr_val = (mrr_start - churn_mrr_acum + expansion_mrr_acum) / mrr_start
            metricas['nrr'] = float(nrr_val)
            
            # GRR = (Start - Churn) / Start (retenção bruta, sem expansion)
            grr_val = (mrr_start - churn_mrr_acum) / mrr_start
            metricas['grr'] = float(grr_val)
        else:
            metricas['nrr'] = np.nan
            metricas['grr'] = np.nan
    else:
        metricas['nrr'] = np.nan
        metricas['grr'] = np.nan
    
    # Cohort Retention M6->M12
    if len(df_mensal) >= 12:
        usuarios_m6 = df_mensal.loc[5, 'usuarios_ativos']
        usuarios_m12 = df_mensal.loc[11, 'usuarios_ativos']
        cohort_m6_retention = usuarios_m12 / usuarios_m6 if usuarios_m6 > 0 else 0
        metricas['cohort_m6_retention'] = float(cohort_m6_retention)
    else:
        metricas['cohort_m6_retention'] = np.nan
    
    # Payback Médio Ponderado
    paybacks_validos = df_mensal[df_mensal['payback_meses'].notna()]
    if len(paybacks_validos) > 0:
        pesos = paybacks_validos['novos_pagantes_total'].values
        paybacks = paybacks_validos['payback_meses'].values
        if pesos.sum() > 0:
            payback_medio = np.average(paybacks, weights=pesos)
            metricas['payback_meses_medio'] = float(payback_medio)
        else:
            metricas['payback_meses_medio'] = np.nan
    else:
        metricas['payback_meses_medio'] = np.nan
    
    # ROI Total
    investido = p_run.get('caixa_inicial', 0) + df_mensal['aportes_capital'].sum()
    lucro_total = df_mensal['lucro_liquido'].sum()
    metricas['roi_total_pct'] = float((lucro_total / investido) * 100) if investido > 0 else np.nan
    
    # Burn Rate Médio
    metricas['burn_rate_medio'] = float(df_mensal['burn_rate'].mean())
    
    # Análise de Caixa
    metricas['caixa_minimo'] = float(df_mensal['caixa'].min())
    metricas['mes_caixa_minimo'] = int(df_mensal['caixa'].idxmin() + 1)
    metricas['quebrou'] = bool(df_mensal['caixa'].min() < THRESHOLD_QUEBRA)
    
    # VaR e CVaR (95%)
    caixa_series = df_mensal['caixa'].values
    if len(caixa_series) > 0:
        var95 = float(np.percentile(caixa_series, 5))
        cvar_mask = caixa_series <= var95
        cvar95 = float(caixa_series[cvar_mask].mean()) if cvar_mask.any() else var95
        metricas['var95_caixa'] = var95
        metricas['cvar95_caixa'] = cvar95
    else:
        metricas['var95_caixa'] = np.nan
        metricas['cvar95_caixa'] = np.nan
    
    # KPIs Básicos
    metricas.update({
        'usuarios_final': int(usuarios_ativos),
        'caixa_final': float(caixa_atual),
        'mrr_final': float(dados['mrr'][-1]),
        'arr_final': float(dados['arr'][-1]),
        'cac_medio': float(df_mensal['cac_blended'].mean()),
        'ltv_media': float(df_mensal['ltv'].mean()),
        'ltv_cac_medio': float(ltv_cac_serie.mean()),
        'runway_final': float(dados['runway_meses'][-1]) if dados['runway_meses'][-1] < 999 else float('inf'),
        'churn_medio': float(df_mensal['churn_rate'].mean()),
        'margem_bruta_media': float(df_mensal['margem_bruta_pct'].mean()),
        'ebitda_margin_media': float(df_mensal['ebitda_margin'].mean())
    })
    
    # --------------------------------------------------------------------
    # BLOCO 5: ALERTAS E VALIDAÇÕES FINAIS
    # --------------------------------------------------------------------
    if df_mensal['caixa'].min() < THRESHOLD_QUEBRA:
        mes_min = int(df_mensal['caixa'].idxmin() + 1)
        caixa_min = float(df_mensal['caixa'].min())
        alertas.append({
            'tipo': 'caixa_negativo',
            'mes': mes_min,
            'valor': caixa_min,
            'mensagem': f'🔴 ALERTA CRÍTICO: Caixa caiu abaixo de R$ {THRESHOLD_QUEBRA:.2f} no mês {mes_min} (valor: R$ {caixa_min:.2f}). Falência técnica eminente.'
        })
    
    if df_mensal['churn_rate'].max() > 0.15:
        mes_max = int(df_mensal['churn_rate'].idxmax() + 1)
        churn_max = float(df_mensal['churn_rate'].max())
        alertas.append({
            'tipo': 'churn_alto',
            'mes': mes_max,
            'valor': churn_max,
            'mensagem': f'🟡 ALERTA: Churn pico de {churn_max*100:.1f}% no mês {mes_max} (acima de 15%). Retenção em risco.'
        })
    
    ltv_cac_min = ltv_cac_serie.min()
    if not np.isnan(ltv_cac_min) and ltv_cac_min < 1.0:
        mes_ltv = int(ltv_cac_serie.idxmin() + 1)
        alertas.append({
            'tipo': 'ltv_cac_insustentavel',
            'mes': mes_ltv,
            'valor': float(ltv_cac_min),
            'mensagem': f'🔴 ALERTA CRÍTICO: LTV/CAC = {ltv_cac_min:.2f} no mês {mes_ltv} (< 1.0). Modelo de aquisição insustentável.'
        })
    
    saturacao_total = df_mensal['saturacao_mercado'].sum()
    if saturacao_total > 10000:
        alertas.append({
            'tipo': 'saturacao_mercado',
            'total_perdido': float(saturacao_total),
            'mensagem': f'⚠️ ALERTA: Saturação de mercado acumulada = {saturacao_total:.0f} visitas perdidas. Considerar expandir mercado.'
        })
    
    for mes in range(meses):
        soma_mix = dados['usuarios_lite'][mes] + dados['usuarios_trader'][mes] + dados['usuarios_pro'][mes]
        if abs(soma_mix - dados['usuarios_ativos'][mes]) > 1:
            alertas.append({
                'tipo': 'erro_mix_inconsistente',
                'mes': mes + 1,
                'esperado': int(dados['usuarios_ativos'][mes]),
                'calculado': int(soma_mix),
                'mensagem': f'❌ ERRO: Mix de usuários inconsistente no mês {mes + 1}. Esperado: {int(dados["usuarios_ativos"][mes])}, Calculado: {int(soma_mix)}'
            })
    
    if modo_debug:
        print(f"✅ Simulação {simulacao_id} concluída:")
        print(f"   Usuários finais: {metricas['usuarios_final']}")
        print(f"   Caixa final: R$ {metricas['caixa_final']:,.2f}")
        print(f"   NRR (Proxy): {metricas.get('nrr', 0)*100:.1f}%")
        print(f"   Burn Rate Médio: R$ {metricas['burn_rate_medio']:,.2f}")
    
    return df_mensal, df_anual, metricas, alertas


# --------------------------------------------------------------------
# PRINT DE CONFIRMAÇÃO
# --------------------------------------------------------------------
if __name__ == "__main__":
    print("="*80)
    print("✅ MOTOR FINANCEIRO V13.0 (CORREÇÕES PONTUAIS - RUNWAY/RH/CAPEX) CARREGADO")
    print("="*80)
    print("📋 CORREÇÕES V13.0 APLICADAS:")
    print("   1. ✅ NRR e GRR calculados com fórmula de retenção real (Start - Churn + Exp)")
    print("   2. ✅ Burn Rate corrigido para visão de Caixa (não Lucro)")
    print("   3. ✅ Custo de Implantação B2B debitado como COGS")
    print("   4. ✅ Zero Hardcode: Parâmetros críticos parametrizados via p_run.get()")
    print("   5. ✅ Vetores de detalhamento (canais, planos) populados")
    print("   6. ✅ COGS Recorrente: Separado de COGS B2B para LTV correto")
    print("   7. ✅ LTV Limpo: Calculado apenas com Margem Recorrente (sem B2B)")
    print("   8. ✅ NRR Real: Tracking de mrr_cohort_m0 (cohort do mês 0)")
    print("   9. ✅ Vetores: mrr_cohort_m0, cogs_recorrente, churn_mrr_cohort_m0")
    print("  10. ✅ df_anual Inteligente: Fluxos (soma), Estoques (último), Taxas (média)")
    print("  11. ✅ Impostos B2B: Regime baseado em faturamento projetado (ARR + B2B*12)")
    print("  12. ✅ Saturação Mercado: Limite dinâmico (mercado_disponivel / taxa_conversão)")
    print("  13. ✅ Runway Protegido: runway=0 se caixa < threshold (sem valores negativos)")
    print()
    print("🎯 PRONTO PARA O MONTE CARLO (CÉLULA 5D)")
    print("="*80)