# ============================================================================
# CÉLULA 04 - MOTOR FINANCEIRO V7.0 INVESTOR-GRADE (MUDANÇAS CIRÚRGICAS)
# ============================================================================
# MUDANÇAS NESTA VERSÃO:
# 1. ✅ 4 novos alertas embutidos (OPEX=0, margem M3+, burn >50%, runway <6mo)
# 2. ✅ Usa benchmarks de PREMISSAS (não hardcoded)
# 3. ✅ Tag versão v7.0
# 4. ✅ Parâmetro 'meta_runway_minimo_meses' adicionado
# 
# PRESERVADO (sem mudanças):
# - Loop mensal (não semanal)
# - Estrutura de cálculos
# - Lógica de negócio
# ============================================================================

def executar_motor_fintech_v7_investor_grade(p, seed=None, variacao_params=None, modo_debug=False):
    """
    Motor de Projeção Financeira V7.0 - Investor-Grade
    
    NOVIDADES V7.0:
    - Sistema de alertas expandido (6 tipos de validação)
    - Usa benchmarks realistas de PREMISSAS (zero hardcoded)
    - Compatível com PREMISSAS V7.0 (granularidade semanal via função separada)
    
    Args:
        p (dict): PREMISSAS completo (fonte única de verdade)
        seed (int): Seed para reprodutibilidade Monte Carlo
        variacao_params (dict): Sobrescritas para Monte Carlo
        modo_debug (bool): Imprime logs detalhados
    
    Returns:
        tuple: (df_mensal, df_anual, metricas_chave, alertas)
    """
    
    import pandas as pd
    import numpy as np
    from datetime import datetime
    
    # ========================================================================
    # SEÇÃO 0: SETUP INICIAL
    # ========================================================================
    inicio_exec = datetime.now()
    
    # Cópia de premissas (permite Monte Carlo)
    p_run = p.copy()
    if variacao_params:
        for k, v in variacao_params.items():
            p_run[k] = v
    
    # Seed para reprodutibilidade
    if seed is None: 
        seed = p_run.get('seed_fixa', 42)
    np.random.seed(int(seed))
    
    # Parâmetros temporais
    meses = int(p_run['meses_projecao'])
    datas = pd.date_range(start=p_run['data_inicio'], periods=meses, freq='MS')
    
    # Sistema de alertas
    alertas = []
    
    if modo_debug:
        print(f"🔧 [DEBUG] Motor V7.0 - {meses} meses (Seed: {seed})")
    
    # ========================================================================
    # SEÇÃO 1: CRIAÇÃO DOS VETORES
    # ========================================================================
    
    dados = {}
    
    metricas_vetores = [
        # GROWTH & AQUISIÇÃO
        'trafego_total', 'trafego_pago', 'trafego_organico',
        'trials_total', 'trials_pagos', 'trials_organicos',
        'novos_pagantes_total', 'novos_ads', 'novos_organicos', 'novos_afiliados',
        'reativacoes', 'taxa_trafego_trial', 'taxa_trial_pago', 'eficiencia_time',
        
        # BASE DE USUÁRIOS
        'usuarios_ativos', 'usuarios_lite', 'usuarios_trader', 'usuarios_pro',
        'churn_usuarios', 'churn_mrr', 'upgrades_lite_trader',
        
        # RECEITAS
        'receita_bruta', 'receita_assinaturas', 'receita_b2b',
        'receita_lite', 'receita_trader', 'receita_pro',
        'mrr', 'arr', 'arpu',
        'crescimento_mrr_mom', 'crescimento_mrr_yoy', 'net_new_mrr',
        
        # DEDUÇÕES
        'impostos', 'aliquota_efetiva', 'taxas_pagamento',
        'inadimplencia', 'chargeback', 'total_deducoes', 'receita_liquida',
        
        # COGS
        'custo_ia_lite', 'custo_ia_trader', 'custo_ia_pro', 'custo_ia_total',
        'comissao_afiliados', 'custo_suporte_variavel', 'total_cogs',
        'margem_bruta', 'margem_bruta_pct',
        
        # INFRAESTRUTURA
        'custo_infra_fixo', 'infra_tier_ativo',
        
        # RECURSOS HUMANOS
        'headcount_total', 'headcount_fundadores', 'headcount_dev', 'headcount_cs',
        'custo_pessoal', 'salarios_brutos', 'encargos',
        
        # OPEX
        'gasto_marketing', 'gasto_instagram', 'gasto_facebook', 'gasto_youtube', 'gasto_google',
        'cpc_blended', 'custo_escritorio', 'custo_contabilidade',
        'despesas_viagens', 'despesas_conselho', 'despesas_freelancer', 'despesas_beneficios',
        'total_opex',
        
        # RESULTADO
        'margem_contribuicao', 'margem_contribuicao_pct',
        'ebitda', 'ebitda_margin',
        'depreciacao', 'ebit', 'ebit_margin',
        'lucro_liquido', 'margem_liquida',
        
        # FLUXO DE CAIXA
        'fluxo_operacional', 'fluxo_investimento', 'fluxo_financiamento',
        'aportes_capital', 'capex', 'distribuicao_lucros',
        'caixa', 'burn_rate', 'runway_meses',
        
        # UNIT ECONOMICS
        'ltv', 'cac_blended', 'cac_paid', 'ltv_cac',
        'payback_meses', 'payback_semanas', 'vida_media_cliente',
        'churn_rate', 'retention_rate',
        'regra_40', 'burn_multiple'
    ]
    
    for metrica in metricas_vetores:
        dados[metrica] = np.zeros(meses)
    
    # ========================================================================
    # SEÇÃO 2: VARIÁVEIS DE ESTADO
    # ========================================================================
    
    # Base de clientes
    usuarios_ativos = p_run['usuarios_pagos_iniciais']
    base_lite = int(usuarios_ativos * p_run['mix_lite'])
    base_trader = int(usuarios_ativos * p_run['mix_trader'])
    base_pro = int(usuarios_ativos * p_run['mix_pro'])
    
    # Financeiro
    caixa_atual = p_run['caixa_inicial'] - p_run['capex_inicial']
    historico_receita_12m = []
    
    # Growth
    trafego_base = p_run['trafego_inicial']
    pool_churned_users = 0
    
    # Gatilhos operacionais
    flags = {
        'fundador_ativado': False,
        'dev_contratado': False,
        'cs_contratado': False,
        'escritorio_aberto': False
    }
    
    regime_atual = 'simples'
    
    # ========================================================================
    # SEÇÃO 3: LOOP MENSAL (CORAÇÃO DO MOTOR)
    # ========================================================================
    
    for mes in range(meses):
        mes_numero = mes + 1
        mes_calendario = datas[mes].month
        
        if modo_debug and mes % 6 == 0:
            print(f"   📅 M{mes_numero}")
        
        # ====================================================================
        # 3.1 GROWTH ENGINE
        # ====================================================================
        
        # Sazonalidade
        fator_sazon = p_run['sazonalidade_trafego'].get(mes_calendario, 1.0)
        
        # Taxa de crescimento
        if mes_numero <= 6:
            taxa_crescimento = p_run['crescimento_trafego_mes_1_6']
        elif mes_numero <= 12:
            taxa_crescimento = p_run['crescimento_trafego_mes_7_12']
       else:
            taxa_crescimento = p_run['crescimento_trafego_mes_13_plus']
        
        if mes > 0:
            trafego_base *= (1 + taxa_crescimento)
        
        # Budget de Marketing
        if mes == 0:
            budget_mkt = p_run['marketing_fixo_mensal']
        else:
            budget_calc = dados['receita_bruta'][mes-1] * p_run['marketing_perc_receita']
            budget_mkt = np.clip(budget_calc, p_run['marketing_fixo_mensal'], p_run['marketing_teto'])
        
        dados['gasto_marketing'][mes] = budget_mkt
        
        # Distribui por canal
        dados['gasto_instagram'][mes] = budget_mkt * p_run['canal_instagram_pct']
        dados['gasto_facebook'][mes] = budget_mkt * p_run['canal_facebook_pct']
        dados['gasto_youtube'][mes] = budget_mkt * p_run['canal_youtube_pct']
        dados['gasto_google'][mes] = budget_mkt * p_run['canal_google_pct']
        
        # CPC Blended
        cpc_blended = (
            p_run['cpc_instagram'] * p_run['canal_instagram_pct'] +
            p_run['cpc_facebook'] * p_run['canal_facebook_pct'] +
            p_run['cpc_google'] * p_run['canal_google_pct'] +
            p_run['cpc_youtube'] * p_run['canal_youtube_pct']
        )
        dados['cpc_blended'][mes] = cpc_blended
        
        # Conversão Blended
        conv_blended = (
            p_run['conv_instagram'] * p_run['canal_instagram_pct'] +
            p_run['conv_facebook'] * p_run['canal_facebook_pct'] +
            p_run['conv_google'] * p_run['canal_google_pct'] +
            p_run['conv_youtube'] * p_run['canal_youtube_pct']
        )
        
        # Tráfego Pago
        visitas_pagas = (budget_mkt / max(cpc_blended, 0.01)) * fator_sazon
        dados['trafego_pago'][mes] = visitas_pagas
        trials_pagos = visitas_pagas * conv_blended
        dados['trials_pagos'][mes] = trials_pagos
        
        # Tráfego Orgânico
        fator_organico = p_run['fator_visitas_organicas_por_pagante']
        visitas_organicas = (trafego_base + usuarios_ativos * fator_organico) * fator_sazon
        dados['trafego_organico'][mes] = visitas_organicas
        trials_organicos = visitas_organicas * p_run['taxa_visitante_para_trial']
        dados['trials_organicos'][mes] = trials_organicos
        
        # Total
        dados['trafego_total'][mes] = visitas_pagas + visitas_organicas
        dados['trials_total'][mes] = trials_pagos + trials_organicos
        dados['taxa_trafego_trial'][mes] = dados['trials_total'][mes] / dados['trafego_total'][mes] if dados['trafego_total'][mes] > 0 else 0
        
        # Eficiência do Time (Ramp-up)
        eficiencia = min(1.0, p_run['ramp_up_inicial'] + (mes * p_run['ramp_up_incremento']))
        dados['eficiencia_time'][mes] = eficiencia
        
        # Conversão para Pagantes
        novos_pagantes_bruto = dados['trials_total'][mes] * p_run['taxa_trial_para_pagante'] * eficiencia
        dados['taxa_trial_pago'][mes] = p_run['taxa_trial_para_pagante'] * eficiencia
        
        # Split por canal
        pct_afiliado = p_run['pct_usuarios_via_afiliado'] if p_run.get('modelo_afiliado_habilitado', False) else 0
        novos_via_afiliado = novos_pagantes_bruto * pct_afiliado
        novos_restantes = novos_pagantes_bruto - novos_via_afiliado
        
        ratio_paid = trials_pagos / (trials_pagos + trials_organicos) if (trials_pagos + trials_organicos) > 0 else 0
        novos_paid = novos_restantes * ratio_paid
        novos_organic = novos_restantes * (1 - ratio_paid)
        
        dados['novos_afiliados'][mes] = int(novos_via_afiliado)
        dados['novos_ads'][mes] = int(novos_paid)
        dados['novos_organicos'][mes] = int(novos_organic)
        dados['novos_pagantes_total'][mes] = dados['novos_afiliados'][mes] + dados['novos_ads'][mes] + dados['novos_organicos'][mes]
        
        # Reativações
        if pool_churned_users > 0:
            reativacoes = int(pool_churned_users * p_run['taxa_reativacao_base_cancelada'])
            dados['reativacoes'][mes] = reativacoes
        else:
            reativacoes = 0
        
        # ====================================================================
        # 3.2 CHURN & RETENÇÃO
        # ====================================================================
        
        churn_rate = max(p_run['churn_maturidade'], p_run['churn_inicial'] - (mes * p_run['churn_decaimento_mensal']))
        dados['churn_rate'][mes] = churn_rate
        dados['retention_rate'][mes] = 1 - churn_rate
        
        churn_usuarios = int(usuarios_ativos * churn_rate)
        dados['churn_usuarios'][mes] = churn_usuarios
        
        if mes > 0:
            dados['churn_mrr'][mes] = dados['mrr'][mes-1] * churn_rate
        
        pool_churned_users += churn_usuarios - reativacoes
        
        # Atualiza base
        usuarios_ativos = max(0, usuarios_ativos + dados['novos_pagantes_total'][mes] - churn_usuarios + reativacoes)
        dados['usuarios_ativos'][mes] = int(usuarios_ativos)
        
        # Upgrades
        upgrades = int(base_lite * p_run.get('taxa_upgrade_lite_trader', 0.02))
        dados['upgrades_lite_trader'][mes] = upgrades
        
        # Recalcula mix
        base_lite = int(usuarios_ativos * p_run['mix_lite']) - upgrades
        base_trader = int(usuarios_ativos * p_run['mix_trader']) + upgrades
        base_pro = int(usuarios_ativos * p_run['mix_pro'])
        
        diff = int(usuarios_ativos) - (base_lite + base_trader + base_pro)
        base_lite += diff
        
        dados['usuarios_lite'][mes] = max(0, base_lite)
        dados['usuarios_trader'][mes] = max(0, base_trader)
        dados['usuarios_pro'][mes] = max(0, base_pro)
        
        # ====================================================================
        # 3.3 RECEITAS
        # ====================================================================
        
        rec_lite = dados['usuarios_lite'][mes] * p_run['preco_lite']
        rec_trader = dados['usuarios_trader'][mes] * p_run['preco_trader']
        rec_pro = dados['usuarios_pro'][mes] * p_run['preco_pro']
        
        dados['receita_lite'][mes] = rec_lite
        dados['receita_trader'][mes] = rec_trader
        dados['receita_pro'][mes] = rec_pro
        
        receita_assinaturas = rec_lite + rec_trader + rec_pro
        dados['receita_assinaturas'][mes] = receita_assinaturas
        
        dados['mrr'][mes] = receita_assinaturas
        dados['arr'][mes] = receita_assinaturas * 12
        dados['arpu'][mes] = receita_assinaturas / usuarios_ativos if usuarios_ativos > 0 else 0
        
        # B2B
        rec_b2b = 0
        if np.random.random() < (p_run['b2b_probabilidade_anual'] / 12):
            rec_b2b = p_run['b2b_setup_fee']
            dados['receita_b2b'][mes] = rec_b2b
        
        dados['receita_bruta'][mes] = receita_assinaturas + rec_b2b
        
        # Crescimento MRR
        if mes > 0:
            dados['crescimento_mrr_mom'][mes] = ((dados['mrr'][mes] / dados['mrr'][mes-1]) - 1) * 100 if dados['mrr'][mes-1] > 0 else 0
            dados['net_new_mrr'][mes] = dados['mrr'][mes] - dados['mrr'][mes-1]
        
        if mes >= 12:
            dados['crescimento_mrr_yoy'][mes] = ((dados['mrr'][mes] / dados['mrr'][mes-12]) - 1) * 100 if dados['mrr'][mes-12] > 0 else 0
        
        # ====================================================================
        # 3.4 DEDUÇÕES & IMPOSTOS
        # ====================================================================
        
        historico_receita_12m.append(dados['receita_bruta'][mes])
        if len(historico_receita_12m) > 12:
            historico_receita_12m.pop(0)
        
        receita_rolling_12m = sum(historico_receita_12m)
        
        if receita_rolling_12m > p_run['threshold_regime_tributario']:
            regime_atual = 'lucro_presumido'
            aliquota = p_run['imposto_lucro_presumido']
        else:
            regime_atual = 'simples'
            aliquota = p_run['imposto_simples_inicial']
        
        dados['aliquota_efetiva'][mes] = aliquota
        dados['impostos'][mes] = dados['receita_bruta'][mes] * aliquota
        
        # Inadimplência
        taxa_inadimp = (
            p_run['taxa_inadimplencia_cartao'] * p_run['mix_pagamento_cartao'] +
            p_run['taxa_inadimplencia_pix'] * p_run['mix_pagamento_pix'] +
            p_run['taxa_inadimplencia_boleto'] * p_run['mix_pagamento_boleto']
        )
        dados['inadimplencia'][mes] = dados['receita_bruta'][mes] * taxa_inadimp
        
        receita_arrecadavel = dados['receita_bruta'][mes] - dados['inadimplencia'][mes]
        
        # Taxas de pagamento
        taxa_processamento = (
            p_run['taxa_processamento_cartao'] * p_run['mix_pagamento_cartao'] +
            p_run['taxa_processamento_pix'] * p_run['mix_pagamento_pix'] +
            p_run['taxa_processamento_boleto'] * p_run['mix_pagamento_boleto']
        )
        dados['taxas_pagamento'][mes] = receita_arrecadavel * taxa_processamento
        
        dados['chargeback'][mes] = dados['receita_bruta'][mes] * p_run['taxa_chargeback']
        dados['total_deducoes'][mes] = dados['impostos'][mes] + dados['taxas_pagamento'][mes] + dados['inadimplencia'][mes] + dados['chargeback'][mes]
        dados['receita_liquida'][mes] = dados['receita_bruta'][mes] - dados['total_deducoes'][mes]
        
        # ====================================================================
        # 3.5 CUSTOS VARIÁVEIS (COGS)
        # ====================================================================
        
        dados['custo_ia_lite'][mes] = dados['usuarios_lite'][mes] * p_run['custo_ia_lite']
        dados['custo_ia_trader'][mes] = dados['usuarios_trader'][mes] * p_run['custo_ia_trader']
        dados['custo_ia_pro'][mes] = dados['usuarios_pro'][mes] * p_run['custo_ia_pro']
        dados['custo_ia_total'][mes] = dados['custo_ia_lite'][mes] + dados['custo_ia_trader'][mes] + dados['custo_ia_pro'][mes]
        
        # Comissões afiliados
        if p_run.get('modelo_afiliado_habilitado', False):
            if p_run.get('comissao_afiliado_tipo') == 'primeira_mensalidade':
                comissao = dados['novos_afiliados'][mes] * dados['arpu'][mes] * p_run.get('comissao_afiliado_pct', 0.20)
            else:
                comissao = dados['novos_afiliados'][mes] * p_run.get('comissao_afiliado_fixo', 50.0)
            dados['comissao_afiliados'][mes] = comissao
        
        # Suporte variável
        dados['custo_suporte_variavel'][mes] = (usuarios_ativos / 1000) * p_run['custo_suporte_por_1000_users']
        
        dados['total_cogs'][mes] = dados['custo_ia_total'][mes] + dados['comissao_afiliados'][mes] + dados['custo_suporte_variavel'][mes]
        dados['margem_bruta'][mes] = dados['receita_liquida'][mes] - dados['total_cogs'][mes]
        dados['margem_bruta_pct'][mes] = (dados['margem_bruta'][mes] / dados['receita_bruta'][mes]) * 100 if dados['receita_bruta'][mes] > 0 else 0
        
        # ====================================================================
        # 3.6 INFRAESTRUTURA (TIER AUTOMÁTICO)
        # ====================================================================
        
        if usuarios_ativos <= p_run['infra_tier_1_limite']:
            tier = 1
        elif usuarios_ativos <= p_run['infra_tier_2_limite']:
            tier = 2
        elif usuarios_ativos <= p_run['infra_tier_3_limite']:
            tier = 3
        else:
            tier = 4
        
        dados['infra_tier_ativo'][mes] = tier
        
        prefixo = f"t{tier}_"
        custo_infra = sum([v for k, v in p_run.items() if k.startswith(prefixo)])
        dados['custo_infra_fixo'][mes] = custo_infra
        
        # ====================================================================
        # 3.7 RECURSOS HUMANOS (GATILHOS)
        # ====================================================================
        
        headcount_atual = 0
        custo_pessoal_mes = 0
        
        # Fundador
        if dados['mrr'][mes] >= p_run['trigger_fundador'] and not flags['fundador_ativado']:
            flags['fundador_ativado'] = True
        
        if flags['fundador_ativado']:
            headcount_atual += 1
            dados['headcount_fundadores'][mes] = 1
            custo_pessoal_mes += p_run['salario_fundador'] * (1 + p_run['encargos_trabalhistas'])
        
        # Dev
        if usuarios_ativos >= p_run['trigger_dev'] and not flags['dev_contratado']:
            flags['dev_contratado'] = True
        
        if flags['dev_contratado']:
            headcount_atual += 1
            dados['headcount_dev'][mes] = 1
            custo_pessoal_mes += p_run['salario_dev_senior'] * (1 + p_run['encargos_trabalhistas'])
        
        # CS
        if usuarios_ativos >= p_run['trigger_cs'] and not flags['cs_contratado']:
            flags['cs_contratado'] = True
        
        if flags['cs_contratado']:
            headcount_atual += 1
            dados['headcount_cs'][mes] = 1
            custo_pessoal_mes += p_run['salario_cs'] * (1 + p_run['encargos_trabalhistas'])
        
        dados['headcount_total'][mes] = headcount_atual
        dados['custo_pessoal'][mes] = custo_pessoal_mes
        dados['salarios_brutos'][mes] = custo_pessoal_mes / (1 + p_run['encargos_trabalhistas']) if custo_pessoal_mes > 0 else 0
        dados['encargos'][mes] = dados['custo_pessoal'][mes] - dados['salarios_brutos'][mes]
        
        # ====================================================================
        # 3.8 DESPESAS OPERACIONAIS (OPEX)
        # ====================================================================
        
        # Escritório
        if dados['mrr'][mes] >= p_run.get('trigger_escritorio', 65000):
            dados['custo_escritorio'][mes] = p_run['custo_escritorio_base']
        
        dados['custo_contabilidade'][mes] = p_run['custo_contabilidade_adv'] + p_run['custo_juridico_compliance']
        
        # Viagens
        if dados['receita_bruta'][mes] >= p_run.get('trigger_viagens_receita', 35000):
            dados['despesas_viagens'][mes] = max(
                p_run['verba_viagens_base'], 
                dados['receita_bruta'][mes] * p_run['verba_viagens_pct_receita']
            )
        
        # Conselho
        if dados['mrr'][mes] >= p_run.get('trigger_conselho_mrr', 100000):
            dados['despesas_conselho'][mes] = p_run['conselho_jeton']
        
        # Freelancers
        if mes % 3 == 0 and dados['receita_bruta'][mes] >= p_run.get('trigger_freelancer_receita', 30000):
            dados['despesas_freelancer'][mes] = p_run['freelancers_trimestral']
        
        # Benefícios Executivos
        lucro_acumulado_12m = dados['lucro_liquido'][max(0, mes-11):mes+1].sum()
        if lucro_acumulado_12m >= p_run.get('trigger_beneficios_lucro', 80000):
            dados['despesas_beneficios'][mes] = p_run['beneficios_executivos']
        
        # Total OPEX
        dados['total_opex'][mes] = (
            dados['gasto_marketing'][mes] +
            dados['custo_infra_fixo'][mes] +
            dados['custo_pessoal'][mes] +
            dados['custo_escritorio'][mes] +
            dados['custo_contabilidade'][mes] +
            dados['despesas_viagens'][mes] +
            dados['despesas_conselho'][mes] +
            dados['despesas_freelancer'][mes] +
            dados['despesas_beneficios'][mes]
        )
        
        # ====================================================================
        # 3.9 RESULTADO CONTÁBIL
        # ====================================================================
        
        dados['margem_contribuicao'][mes] = dados['margem_bruta'][mes] - dados['gasto_marketing'][mes]
        dados['margem_contribuicao_pct'][mes] = (dados['margem_contribuicao'][mes] / dados['receita_bruta'][mes]) * 100 if dados['receita_bruta'][mes] > 0 else 0
        
        dados['ebitda'][mes] = dados['margem_bruta'][mes] - dados['total_opex'][mes]
        dados['ebitda_margin'][mes] = (dados['ebitda'][mes] / dados['receita_bruta'][mes]) * 100 if dados['receita_bruta'][mes] > 0 else 0
        
        # Depreciação
        if mes == 0:
            dados['depreciacao'][mes] = p_run['capex_inicial'] / p_run['tempo_depreciacao_equipamento_meses']
        elif mes == 24:
            dados['depreciacao'][mes] = (p_run['capex_inicial'] + p_run['capex_recorrente_24m']) / p_run['tempo_depreciacao_equipamento_meses']
        else:
            dados['depreciacao'][mes] = dados['depreciacao'][mes-1] if mes > 0 else 0
        
        dados['ebit'][mes] = dados['ebitda'][mes] - dados['depreciacao'][mes]
        dados['ebit_margin'][mes] = (dados['ebit'][mes] / dados['receita_bruta'][mes]) * 100 if dados['receita_bruta'][mes] > 0 else 0
        
        dados['lucro_liquido'][mes] = dados['ebit'][mes]
        dados['margem_liquida'][mes] = (dados['lucro_liquido'][mes] / dados['receita_bruta'][mes]) * 100 if dados['receita_bruta'][mes] > 0 else 0
        
        # ====================================================================
        # 3.10 FLUXO DE CAIXA
        # ====================================================================
        
        dados['fluxo_operacional'][mes] = dados['lucro_liquido'][mes] + dados['depreciacao'][mes]
        
        # Investimentos
        if mes == 0:
            dados['capex'][mes] = 0
        elif mes == 24:
            dados['capex'][mes] = p_run['capex_recorrente_24m']
        
        dados['fluxo_investimento'][mes] = -dados['capex'][mes]
        
        # Financiamento
        if mes < p_run['meses_aporte']:
            dados['aportes_capital'][mes] = p_run['aporte_mensal']
        
        # Distribuição
        if dados['lucro_liquido'][mes] > 0:
            dados['distribuicao_lucros'][mes] = dados['lucro_liquido'][mes] * p_run['percentual_distribuicao']
        
        dados['fluxo_financiamento'][mes] = dados['aportes_capital'][mes] - dados['distribuicao_lucros'][mes]
        
        # Caixa final
        fluxo_total = dados['fluxo_operacional'][mes] + dados['fluxo_investimento'][mes] + dados['fluxo_financiamento'][mes]
        caixa_atual += fluxo_total
        dados['caixa'][mes] = caixa_atual
        
        # Burn Rate
        if dados['lucro_liquido'][mes] < 0:
            dados['burn_rate'][mes] = abs(dados['lucro_liquido'][mes])
        
        # Runway
        if dados['burn_rate'][mes] > 0:
            dados['runway_meses'][mes] = caixa_atual / dados['burn_rate'][mes]
        else:
            dados['runway_meses'][mes] = np.inf
        
        # ====================================================================
        # 3.11 UNIT ECONOMICS
        # ====================================================================
        
        dados['vida_media_cliente'][mes] = 1 / churn_rate if churn_rate > 0 else np.inf
        
        # CAC
        if dados['novos_pagantes_total'][mes] > 0:
            dados['cac_blended'][mes] = dados['gasto_marketing'][mes] / dados['novos_pagantes_total'][mes]
            if dados['novos_ads'][mes] > 0:
                dados['cac_paid'][mes] = dados['gasto_marketing'][mes] / dados['novos_ads'][mes]
        
        # LTV
        margem_contrib_unit = dados['margem_bruta'][mes] / usuarios_ativos if usuarios_ativos > 0 else 0
        dados['ltv'][mes] = margem_contrib_unit * dados['vida_media_cliente'][mes] if dados['vida_media_cliente'][mes] != np.inf else margem_contrib_unit * 100
        
        # LTV/CAC
        if dados['cac_blended'][mes] > 0:
            dados['ltv_cac'][mes] = dados['ltv'][mes] / dados['cac_blended'][mes]
        
        # Payback
        if margem_contrib_unit > 0 and dados['cac_blended'][mes] > 0:
            dados['payback_meses'][mes] = dados['cac_blended'][mes] / margem_contrib_unit
            dados['payback_semanas'][mes] = dados['payback_meses'][mes] * 4.33
        
        # Regra dos 40
        taxa_crescimento_arr = dados['crescimento_mrr_yoy'][mes] if mes >= 12 else 0
        dados['regra_40'][mes] = taxa_crescimento_arr + dados['margem_liquida'][mes]
        
        # Burn Multiple
        if dados['net_new_mrr'][mes] > 0 and dados['burn_rate'][mes] > 0:
            dados['burn_multiple'][mes] = dados['burn_rate'][mes] / dados['net_new_mrr'][mes]
        
        # ====================================================================
        # 3.12 ALERTAS EMBUTIDOS (V7.0 - EXPANDIDO) ⭐⭐⭐
        # ====================================================================
        
        # ALERTA 1: Caixa negativo
        if dados['caixa'][mes] < 0 and 'caixa_negativo' not in [a['tipo'] for a in alertas]:
            alertas.append({
                'mes': mes_numero,
                'tipo': 'caixa_negativo',
                'severidade': 'CRITICO',
                'valor': dados['caixa'][mes],
                'mensagem': f'💀 Caixa NEGATIVO: R${dados["caixa"][mes]/1000:.1f}k',
                'acao': 'PARAR TUDO - Buscar investimento emergencial ou fechar operação'
            })
        
        # ALERTA 2: LTV/CAC muito baixo (benchmark de PREMISSAS!) ✅
        ltv_cac_min = p_run.get('benchmark_ltv_cac_critico', 1.0)
        if dados['ltv_cac'][mes] < ltv_cac_min and mes > 6:
            alertas.append({
                'mes': mes_numero,
                'tipo': 'ltv_cac_critico',
                'severidade': 'CRITICO',
                'valor': dados['ltv_cac'][mes],
                'mensagem': f'⚠️ LTV/CAC {dados["ltv_cac"][mes]:.1f}x < {ltv_cac_min}x',
                'acao': 'Reduzir CAC ou aumentar pricing/retenção urgente'
            })
        
        # ALERTA 3: OPEX zero após M1 (NOVO V7.0) ⭐
        if mes > 0 and dados['total_opex'][mes] == 0:
            alertas.append({
                'mes': mes_numero,
                'tipo': 'opex_zero',
                'severidade': 'ERRO',
                'valor': 0,
                'mensagem': f'❌ OPEX zero em M{mes_numero} - verificar cálculo',
                'acao': 'Revisar infra + marketing + RH - provavelmente bug no motor'
            })
        
        # ALERTA 4: Margem contribuição negativa M3+ (NOVO V7.0) ⭐
        if dados['margem_contribuicao'][mes] < 0:
            if mes <= 2:
                # OK - esperado M0-M2 (benchmark de PREMISSAS!)
                margem_esperada_m0 = p_run.get('benchmark_margem_contrib_m0', -0.60)
                alertas.append({
                    'mes': mes_numero,
                    'tipo': 'margem_negativa_esperado',
                    'severidade': 'INFO',
                    'valor': dados['margem_contribuicao_pct'][mes],
                    'mensagem': f'ℹ️ Margem contrib {dados["margem_contribuicao_pct"][mes]:.0f}% negativa (esperado M0-M2: {margem_esperada_m0*100:.0f}%)',
                    'acao': 'Acelerar aquisição para diluir custos fixos'
                })
            else:
                # CRÍTICO - não deveria ser negativa M3+
                alertas.append({
                    'mes': mes_numero,
                    'tipo': 'margem_negativa_critico',
                    'severidade': 'CRITICO',
                    'valor': dados['margem_contribuicao_pct'][mes],
                    'mensagem': f'🚨 Margem contrib {dados["margem_contribuicao_pct"][mes]:.0f}% AINDA negativa em M{mes_numero}',
                    'acao': 'Revisar pricing (+50%) OU reduzir marketing (-30%) urgente'
                })
        
        # ALERTA 5: Burn rate > 50% receita (NOVO V7.0) ⭐
        burn_pct = (dados['burn_rate'][mes] / dados['receita_bruta'][mes]) * 100 if dados['receita_bruta'][mes] > 0 else 0
        if dados['burn_rate'][mes] > 0 and burn_pct > 50:
            alertas.append({
                'mes': mes_numero,
                'tipo': 'burn_alto',
                'severidade': 'ATENCAO',
                'valor': burn_pct,
                'mensagem': f'⚡ Queima R${dados["burn_rate"][mes]/1000:.1f}k = {burn_pct:.0f}% da receita',
                'acao': 'Reduzir custos fixos (-20%) OU acelerar crescimento receita (+30%)'
            })
        
        # ALERTA 6: Runway < 6 meses (NOVO V7.0 - benchmark de PREMISSAS!) ⭐
        runway_minimo = p_run.get('meta_runway_minimo_meses', 6)
        if dados['runway_meses'][mes] < runway_minimo and dados['runway_meses'][mes] != np.inf:
            alertas.append({
                'mes': mes_numero,
                'tipo': 'runway_baixo',
                'severidade': 'CRITICO',
                'valor': dados['runway_meses'][mes],
                'mensagem': f'⏰ Sobrevivência: {dados["runway_meses"][mes]:.1f} meses < {runway_minimo} meses',
                'acao': 'Buscar investimento IMEDIATO ou reduzir burn 50% nos próximos 30 dias'
            })
    
    # ========================================================================
    # SEÇÃO 4: MONTAGEM DO DATAFRAME FINAL
    # ========================================================================
    
    df_mensal = pd.DataFrame(dados)
    df_mensal.insert(0, 'data', datas)
    df_mensal.insert(1, 'mes', range(1, meses + 1))
    df_mensal.insert(2, 'ano', [d.year for d in datas])
    
    # Agrupamento anual
    df_anual = df_mensal.groupby('ano').agg({
        'receita_bruta': 'sum',
        'total_deducoes': 'sum',
        'receita_liquida': 'sum',
        'total_cogs': 'sum',
        'margem_bruta': 'sum',
        'gasto_marketing': 'sum',
        'custo_pessoal': 'sum',
        'total_opex': 'sum',
        'ebitda': 'sum',
        'lucro_liquido': 'sum',
        'mrr': 'last',
        'arr': 'last',
        'usuarios_ativos': 'last',
        'caixa': 'last'
    }).reset_index()
    
    # Métricas Chave
    metricas_chave = {
        'usuarios_final': int(df_mensal['usuarios_ativos'].iloc[-1]),
        'mrr_final': df_mensal['mrr'].iloc[-1],
        'arr_final': df_mensal['arr'].iloc[-1],
        'caixa_final': df_mensal['caixa'].iloc[-1],
        'ltv_media': df_mensal['ltv'].mean(),
        'cac_medio': df_mensal['cac_blended'].replace(0, np.nan).mean(),
        'churn_medio': df_mensal['churn_rate'].mean() * 100,
        'payback_medio_meses': df_mensal['payback_meses'].replace(0, np.nan).mean(),
        'total_alertas': len(alertas),
        'alertas_criticos': len([a for a in alertas if a.get('severidade') == 'CRITICO']),
        'tempo_exec_segundos': (datetime.now() - inicio_exec).total_seconds()
    }
    
    if modo_debug:
        print(f"\n✅ Motor V7.0 concluído em {metricas_chave['tempo_exec_segundos']:.2f}s")
        print(f"📊 {metricas_chave['usuarios_final']} usuários | MRR R${metricas_chave['mrr_final']/1000:.1f}k")
        print(f"⚠️  {metricas_chave['total_alertas']} alertas ({metricas_chave['alertas_criticos']} críticos)")
    
    return df_mensal, df_anual, metricas_chave, alertas


# ============================================================================
# EXECUTAR MOTOR
# ============================================================================
print("✅ Motor V7.0 Investor-Grade carregado")
print("\n🎯 Para executar:")
print("   df_mensal, df_anual, metricas, alertas = executar_motor_fintech_v7_investor_grade(PREMISSAS)")
print("\n⭐ NOVIDADES V7.0:")
print("   • 6 alertas embutidos (caixa, LTV/CAC, OPEX, margem, burn, runway)")
print("   • Usa benchmarks de PREMISSAS (zero hardcoded)")
print("   • Compatível com granularidade semanal (via função separada)")
