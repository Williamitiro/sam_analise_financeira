# CÉLULA 3 — CONFIGURAÇÃO DE CENÁRIO IDEAL V3.0 (PREMISSAS INDEPENDENTES)
# ============================================================================
# OBJETIVO: Definir premissas FIXAS para o cenário Ideal (benchmark).
# IMPORTANTE: Este cenário NÃO herda do cenário Real/Estresse.
# ============================================================================

import copy

def obter_premissas_ideal():
    """
    Retorna um dicionário COMPLETO de premissas para o cenário Ideal.
    Estes valores são FIXOS e servem como benchmark de referência.
    """
    
    PREMISSAS_IDEAL = {
        # ====================================================================
        # 1. METADADOS & CONTROLE DE TEMPO
        # ====================================================================
        'meta_version': '9.0-ideal-benchmark',
        'meta_updated_at': '2025-12-13',
        
        'data_inicio': '2026-06-01',
        'meses_projecao': 36,
        'seed_fixa': 42,
        
        'semanas_por_mes': 4.33,
        'meses_por_ano': 12,

        # ====================================================================
        # 2. SAZONALIDADE (igual ao Real - mercado não muda)
        # ====================================================================
        'sazonalidade_trafego': {
            1: 1.30, 2: 1.10, 3: 1.15, 
            4: 1.00, 5: 1.05, 6: 1.00,
            7: 0.85, 8: 1.00, 9: 1.00, 
            10: 1.05, 11: 1.10, 12: 0.75
        },

        # ====================================================================
        # 3. AQUISIÇÃO & GROWTH (BENCHMARK OTIMISTA)
        # ====================================================================
        'usuarios_pagos_iniciais': 7,          # 2x do Real (benchmark)
        'trafego_inicial': 250,                 # 3x do Real (benchmark)
        
        # Metas de crescimento AGRESSIVAS (benchmark de mercado)
        'crescimento_trafego_mes_1_6': 0.20,    # 20% ao mês (vs 12% Real)
        'crescimento_trafego_mes_7_12': 0.10,   # 10% ao mês (vs 7% Real)
        'crescimento_trafego_mes_13_plus': 0.06,# 6% ao mês (vs 4% Real)

        'mercado_potencial_traders': 150000,
        'semanas_validacao_m0_m6': 26,

        # Funil OTIMIZADO (benchmark)
        'taxa_visitante_para_trial': 0.07,      # 7% (vs 5% Real)
        'taxa_trial_para_pagante': 0.14,        # 14% (vs 12% Real)
        
        # Eficiência (time já treinado no benchmark)
        'ramp_up_inicial': 0.50,                # 60% (vs 50% Real)
        'ramp_up_incremento': 0.08,
        
        # Crescimento orgânico mais forte
        'fator_visitas_organicas_por_pagante': 3.0,  #  (vs 2.5 Real)
        'taxa_crescimento_organico_base': 0.03,
        'elasticidade_organico': 0.70,
        'alerta_dependencia_organica_pct': 50.0,

        # ====================================================================
        # 4. CHURN & RETENÇÃO (BENCHMARK)
        # ====================================================================
        'churn_inicial': 0.12,                  # 12% (vs 12% Real)
        'churn_maturidade': 0.05,               # 5% (vs 6% Real)
        'churn_base': 0.06,
        'churn_decaimento_mensal': 0.002,
        'taxa_reativacao_base_cancelada': 0.02, # 2% (vs 1% Real)

        # ====================================================================
        # 5. PRICING & MIX (IGUAL AO REAL)
        # ====================================================================
        'preco_lite': 69.90, 
        'preco_trader': 99.90, 
        'preco_pro': 169.90,
        
        'mix_lite': 0.45,                       # Menos Lite no Ideal
        'mix_trader': 0.40,                     # Mais Trader
        'mix_pro': 0.15,
        'taxa_upgrade_lite_trader': 0.03,       # 3% upgrades (vs 2% Real)
        
        'mix_pagamento_cartao': 0.55, 
        'mix_pagamento_pix': 0.40, 
        'mix_pagamento_boleto': 0.05,
        
        'taxa_processamento_cartao': 0.045,
        'taxa_processamento_pix': 0.01,
        'taxa_processamento_boleto': 0.035,
        'taxa_chargeback': 0.004,               # Menor chargeback
        
        'taxa_inadimplencia_cartao': 0.04,      # Menor inadimplência
        'taxa_inadimplencia_pix': 0.07,
        'taxa_inadimplencia_boleto': 0.02,
        
        'imposto_simples_inicial': 0.06,
        'imposto_lucro_presumido': 0.1633,
        'threshold_regime_tributario': 4800000.00,

        # ====================================================================
        # 6. INFRAESTRUTURA (IGUAL AO REAL)
        # ====================================================================
        'custo_ia_lite': 3.00, 
        'custo_ia_trader': 5.00, 
        'custo_ia_pro': 13.00,
        
        'custo_ferramentas_base': 1.00,
        'custo_suporte_por_1000_users': 1.00,
        
        'infra_tier_1_limite': 500,
        'infra_tier_2_limite': 1500,
        'infra_tier_3_limite': 5000,
        'infra_tier_4_limite': 10000,

        't1_vps_app_api': 120.00, 
        't1_vps_windows_mt5': 180.00, 
        't1_database_managed': 80.00,
        't1_storage_s3': 20.00, 
        't1_ferramentas_dev': 300.00, 
        't1_observability': 0.00,
        't1_scraping_news': 100.00, 
        't1_dominio_dns': 10.00, 
        't1_email_transacional': 50.00,
        
        't2_api_dados_b3': 5000.00, 
        't2_compute_app': 450.00, 
        't2_database_primary': 350.00,
        't2_cache_redis': 120.00, 
        't2_storage_s3': 100.00, 
        't2_security_waf': 120.00,
        't2_ferramentas_dev': 600.00, 
        't2_observability': 250.00, 
        't2_suporte_ticket': 300.00,
        
        't3_api_dados_b3_pro': 7000.00, 
        't3_load_balancer': 200.00, 
        't3_compute_cluster': 1500.00,
        't3_db_primary_replica': 1200.00, 
        't3_cache_cluster': 400.00, 
        't3_data_warehouse': 500.00,
        't3_security_advanced': 500.00, 
        't3_ci_cd_pipeline': 300.00, 
        't3_observability_pro': 1000.00,
        
        't4_api_dados_institutional': 10000.00, 
        't4_k8s_cluster': 4500.00,
        't4_db_aurora_serverless': 3000.00, 
        't4_data_lake_engineering': 2000.00,
        't4_security_soc': 2500.00, 
        't4_support_enterprise': 1500.00, 
        't4_multi_region_backup': 1000.00,

        # ====================================================================
        # 7. MARKETING (BENCHMARK - COM BUDGET)
        # ====================================================================
        'marketing_habilitado': True,
        'marketing_fixo_mensal': 3500.00,       # R$5k fixo (benchmark tem budget)
        'marketing_perc_receita': 0.30,         # 30% reinvestimento
        'marketing_teto': 30000.00,

        'marketing_budget_ref_brand_lift': 3000.0,
        'limite_inventario_mensal': 50000,
        
        'canal_instagram_pct': 0.35, 'cpc_instagram': 0.50, 'conv_instagram': 0.04,
        'canal_facebook_pct': 0.20, 'cpc_facebook': 0.70, 'conv_facebook': 0.03,
        'canal_youtube_pct': 0.35, 'cpc_youtube': 2.50, 'conv_youtube': 0.10,
        'canal_google_pct': 0.10, 'cpc_google': 5.00, 'conv_google': 0.12,

        # ====================================================================
        # 8. PROGRAMA DE AFILIADOS
        # ====================================================================
        'modelo_afiliado_habilitado': False,
        'pct_usuarios_via_afiliado': 0.20,
        'comissao_afiliado_tipo': 'primeira_mensalidade',
        'comissao_afiliado_fixo': 50.00, 
        'comissao_afiliado_pct': 0.20, 
        'comissao_afiliado_meses': 12,

        # ====================================================================
        # 9. RH & EQUIPE (TRIGGERS MAIS CEDO)
        # ====================================================================
        'salario_fundador': 6000.00, 'trigger_fundador': 35000.00,  # Mais cedo
        'salario_dev_senior': 10000.00, 'trigger_dev': 650,          # Mais cedo
        'salario_cs': 4000.00, 'trigger_cs': 850,                   # Mais cedo
        'encargos_trabalhistas': 0.70,

        # ====================================================================
        # 10. GOVERNANÇA & B2B
        # ====================================================================
        'custo_escritorio_base': 3500.00, 
        'trigger_escritorio': 100000.00,
        
        'custo_contabilidade_adv': 1000.00,
        'custo_juridico_compliance': 100.00,
        'trigger_contabilidade': 50000.00,
        
        'verba_viagens_base': 1.00, 
        'verba_viagens_pct_receita': 0.02,
        'trigger_viagens_receita': 30000.00,
        
        'conselho_jeton': 3000.00, 
        'trigger_conselho_mrr': 80000.00,
        
        'freelancers_trimestral': 1000.00,
        'trigger_freelancer_receita': 20000.00,
        
        'beneficios_executivos': 5000.00, 
        'trigger_beneficios_lucro': 65000.00,
        
        'b2b_probabilidade_anual': 0.15,        # 15% (vs 10% Real)
        'b2b_setup_fee': 15000.00,
        'b2b_custo_implantacao': 5000.00,

        # ====================================================================
        # 11. CAPITAL (BENCHMARK COM MAIS CAIXA)
        # ====================================================================
        'caixa_inicial': 35000.00,              # R$35k (benchmark tem capital)
        'aporte_mensal': 3500.00,               # R$3.5k/mês
        'meses_aporte': 10,                     # 10 meses garantidos

        'threshold_caixa_quebra': -10000.0,
        'caixa_reserva_operacional': 5000.0,
        
        'capex_inicial': 1000.00,
        'capex_recorrente_24m': 12000.00,     
        'tempo_depreciacao_equipamento_meses': 24,

        # ====================================================================
        # 12. DISTRIBUIÇÃO DE LUCROS
        # ====================================================================
        'percentual_distribuicao': 0.00,
        'split_fundador': 0.50,
        'split_investidor': 0.50,

        # ====================================================================
        # 13. BENCHMARKS (REFERÊNCIA)
        # ====================================================================
        'benchmark_cac_m0': 400.0,
        'benchmark_cac_m6': 200.0,
        'benchmark_cac_m12': 180.0,
        'benchmark_cac_m36': 150.0,
        
        'benchmark_churn_m0': 0.08,
        'benchmark_churn_m6': 0.05,
        
        'benchmark_ltv_cac_m0': 3.0,
        'benchmark_ltv_cac_m6': 4.0,
        'benchmark_ltv_cac_m36': 5.0,
        
        'benchmark_payback_m0': 8.0,
        'benchmark_payback_m6': 6.0,
        
        # Benchmarks de mercado
        'benchmark_cac_min': 150,
        'benchmark_cac_max': 1500,
        'benchmark_ltv_bom_min': 500,
        'benchmark_ltv_excelente_min': 800,
        'benchmark_ltv_cac_min': 3,
        'benchmark_ltv_cac_bom': 5,
        'benchmark_ltv_cac_excelente': 5,
        'benchmark_ltv_cac_suspeito': 10,
        'benchmark_payback_excelente': 6,
        'benchmark_payback_alto': 18,
        'benchmark_churn_bom': 0.05,
        'benchmark_churn_max': 0.10,
        'benchmark_trial_min': 0.10,
        'benchmark_trial_bom': 0.12,
        'benchmark_trial_excelente': 0.15,
    }
    
    return PREMISSAS_IDEAL


def atualizar_premissas_ideais(premissas):
    """
    DEPRECATED: Função mantida para compatibilidade.
    Use obter_premissas_ideal() para obter premissas independentes.
    """
    # Apenas adiciona os benchmarks, mas NÃO deve ser usado para cenário ideal
    premissas.update({
        'benchmark_cac_min': 150,
        'benchmark_cac_max': 1500,
        'benchmark_ltv_bom_min': 500,
        'benchmark_ltv_excelente_min': 800,
        'benchmark_ltv_cac_min': 3,
        'benchmark_ltv_cac_bom': 5,
        'benchmark_ltv_cac_excelente': 5,
        'benchmark_ltv_cac_suspeito': 10,
        'benchmark_payback_excelente': 6,
        'benchmark_payback_alto': 18,
        'benchmark_churn_bom': 0.05,
        'benchmark_churn_max': 0.10,
        'benchmark_trial_min': 0.10,
        'benchmark_trial_bom': 0.12,
        'benchmark_trial_excelente': 0.15,
        'growth_m1_6_base': 0.10,
        'growth_m7_12_base': 0.08,
        'growth_m13_36_base': 0.05,
        'growth_m1_6_otimista': 0.15,
        'growth_m7_12_otimista': 0.10,
        'growth_m13_36_otimista': 0.07,
        'taxa_pagamento': 0.035,
        'impostos': 0.08,
        'modelo_afiliado': 'primeira_mensalidade',
        'pct_usuarios_via_afiliado': 0.20,
        'comissao_primeira_mensalidade': 1.0,
        'comissao_afiliado_fixo': 50.00,
        'comissao_afiliado_pct': 0.20,
        'comissao_afiliado_meses': 12,
    })
    return premissas
