# CÉLULA 02 - PREMISSAS V9.2 - GROWTH PARAMETRIZADO (ZERO HARDCODE)
# ============================================================================
# CORREÇÃO CRÍTICA: Crescimento orgânico agora depende do budget investido
# ============================================================================

PREMISSAS = {
    # ========================================================================
    # 1. METADADOS & CONTROLE DE TEMPO
    # ========================================================================
    'meta_version': '9.2-growth-parametrizado',
    'meta_updated_at': '2025-12-14',
    
    'data_inicio': '2026-06-01',
    'meses_projecao': 36,
    'seed_fixa': 42,
    
    'semanas_por_mes': 4.33,
    'meses_por_ano': 12,

    # ========================================================================
    # 2. SAZONALIDADE DO MERCADO (CALENDÁRIO B3)
    # ========================================================================
    'sazonalidade_trafego': {
        1: 1.30,  2: 1.10,  3: 1.15, 
        4: 1.00,  5: 1.05,  6: 1.00,
        7: 0.85,  8: 1.00,  9: 1.00, 
        10: 1.05, 11: 1.10, 12: 0.75
    },

    # ========================================================================
    # 3. AQUISIÇÃO, GROWTH & METAS (V9.2 - PARAMETRIZADO)
    # ========================================================================
    'usuarios_pagos_iniciais': 10,  # Ajustado de 5 para 10 (base mais estável)
    'trafego_inicial': 400,         # Ajustado de 250 para 400
    
    # --- NOVO: MODELO DE TIERS DE BUDGET PARA CRESCIMENTO ORGÂNICO ---
    # Cada tier define: budget mínimo, taxa de crescimento mensal orgânico
    # Lógica: Sem investimento = sem crescimento. Budget maior = mais SEO/conteúdo
    
    'growth_tiers': [
        # (budget_min, budget_max, taxa_crescimento_mensal, descrição)
        {'budget_min': 0,     'budget_max': 500,   'taxa': 0.000, 'nome': 'Hustle Manual (Zero Growth)'},
        {'budget_min': 500,   'budget_max': 1500,  'taxa': 0.005, 'nome': 'SEO Mínimo (0.5%/mês)'},
        {'budget_min': 1500,  'budget_max': 3000,  'taxa': 0.010, 'nome': 'SEO Básico (1.0%/mês)'},
        {'budget_min': 3000,  'budget_max': 6000,  'taxa': 0.018, 'nome': 'SEO Profissional (1.8%/mês)'},
        {'budget_min': 6000,  'budget_max': 15000, 'taxa': 0.025, 'nome': 'Content Marketing (2.5%/mês)'},
        {'budget_min': 15000, 'budget_max': 999999,'taxa': 0.030, 'nome': 'Growth Agressivo (3.0%/mês)'},
    ],
    
    # --- DEPRECATED (Mantidos para compatibilidade, mas NÃO USADOS no motor) ---
    'crescimento_trafego_mes_1_6': 0.0,      # IGNORADO (usar growth_tiers)
    'crescimento_trafego_mes_7_12': 0.0,     # IGNORADO (usar growth_tiers)
    'crescimento_trafego_mes_13_plus': 0.0,  # IGNORADO (usar growth_tiers)

    # Parâmetros de Mercado
    'mercado_potencial_traders': 150000,
    'semanas_validacao_m0_m6': 26,

    # --- FUNIL DE VENDAS ---
    'taxa_visitante_para_trial': 0.05,       # 5% dos visitantes testam
    'taxa_trial_para_pagante': 0.16,         # Ajustado de 12% para 16%
    
    # Eficiência do Time (Ramp-up)
    'ramp_up_inicial': 0.50,
    'ramp_up_incremento': 0.06,
    
    # --- CRESCIMENTO ORGÂNICO (VIRALIDADE) ---
    'fator_visitas_organicas_por_pagante': 3.5,  # Ajustado de 2.5 para 3.5
    'elasticidade_organico': 0.60,
    'alerta_dependencia_organica_pct': 50.0,

    # ========================================================================
    # 4. CHURN & RETENÇÃO
    # ========================================================================
    'churn_inicial': 0.12,
    'churn_maturidade': 0.05,                # Ajustado de 6% para 5%
    'churn_base': 0.07,
    'churn_decaimento_mensal': 0.003,        # Ajustado de 0.002 para 0.003
    'taxa_reativacao_base_cancelada': 0.02,

    # ========================================================================
    # 5. PRICING & MIX DE PRODUTOS
    # ========================================================================
    'preco_lite': 69.90, 
    'preco_trader': 99.90, 
    'preco_pro': 169.90,
    
    'mix_lite': 0.50,
    'mix_trader': 0.35,
    'mix_pro': 0.15,
    'taxa_upgrade_lite_trader': 0.03,        # Ajustado de 2% para 3%
    
    'mix_pagamento_cartao': 0.55, 
    'mix_pagamento_pix': 0.40, 
    'mix_pagamento_boleto': 0.05,
    
    'taxa_processamento_cartao': 0.045,
    'taxa_processamento_pix': 0.01,
    'taxa_processamento_boleto': 0.035,
    'taxa_chargeback': 0.005,
    
    'taxa_inadimplencia_cartao': 0.04,
    'taxa_inadimplencia_pix': 0.08,
    'taxa_inadimplencia_boleto': 0.02,
    
    'imposto_simples_inicial': 0.06,
    'imposto_lucro_presumido': 0.1633,
    'threshold_regime_tributario': 4800000.00,

    # ========================================================================
    # 6. INFRAESTRUTURA & CUSTOS VARIÁVEIS
    # ========================================================================
    'custo_ia_lite': 3.00, 
    'custo_ia_trader': 5.00, 
    'custo_ia_pro': 13.00,
    
    'custo_ferramentas_base': 1.00,
    'custo_suporte_por_1000_users': 1.00,
    
    'infra_tier_1_limite': 500,
    'infra_tier_2_limite': 1500,
    'infra_tier_3_limite': 5000,
    'infra_tier_4_limite': 10000,

    # TIER 1
    't1_vps_app_api': 120.00, 
    't1_vps_windows_mt5': 180.00, 
    't1_database_managed': 80.00,
    't1_storage_s3': 20.00, 
    't1_ferramentas_dev': 300.00, 
    't1_observability': 0.00,
    't1_scraping_news': 100.00, 
    't1_dominio_dns': 10.00, 
    't1_email_transacional': 50.00,
    
    # TIER 2
    't2_api_dados_b3': 5000.00, 
    't2_compute_app': 450.00, 
    't2_database_primary': 350.00,
    't2_cache_redis': 120.00, 
    't2_storage_s3': 100.00, 
    't2_security_waf': 120.00,
    't2_ferramentas_dev': 600.00, 
    't2_observability': 250.00, 
    't2_suporte_ticket': 300.00,
    
    # TIER 3
    't3_api_dados_b3_pro': 7000.00, 
    't3_load_balancer': 200.00, 
    't3_compute_cluster': 1500.00,
    't3_db_primary_replica': 1200.00, 
    't3_cache_cluster': 400.00, 
    't3_data_warehouse': 500.00,
    't3_security_advanced': 500.00, 
    't3_ci_cd_pipeline': 300.00, 
    't3_observability_pro': 1000.00,
    
    # TIER 4
    't4_api_dados_institutional': 10000.00, 
    't4_k8s_cluster': 4500.00,
    't4_db_aurora_serverless': 3000.00, 
    't4_data_lake_engineering': 2000.00,
    't4_security_soc': 2500.00, 
    't4_support_enterprise': 1500.00, 
    't4_multi_region_backup': 1000.00,

    # ========================================================================
    # 7. MARKETING (V9.2 - AJUSTADO)
    # ========================================================================
    'marketing_habilitado': True,
    'marketing_fixo_mensal': 2500.00,        # Ajustado de R$ 1.750 para R$ 2.500
    'marketing_perc_receita': 0.25,          # Ajustado de 40% para 25%
    'marketing_teto': 30000.00,              # Ajustado de R$ 25k para R$ 30k

    'marketing_budget_ref_brand_lift': 3000.0,  # DEPRECATED (não usado mais)
    'limite_inventario_mensal': 50000,
    
    # Mix de Canais
    'canal_instagram_pct': 0.35, 'cpc_instagram': 0.60, 'conv_instagram': 0.03,
    'canal_facebook_pct': 0.20,  'cpc_facebook': 0.80,  'conv_facebook': 0.02,
    'canal_youtube_pct': 0.35,   'cpc_youtube': 3.00,   'conv_youtube': 0.09,
    'canal_google_pct': 0.10,    'cpc_google': 6.00,    'conv_google': 0.12,

    # ========================================================================
    # 8. PROGRAMA DE AFILIADOS
    # ========================================================================
    'modelo_afiliado_habilitado': False,
    'pct_usuarios_via_afiliado': 0.15,
    'comissao_afiliado_tipo': 'primeira_mensalidade',
    'comissao_afiliado_fixo': 50.00, 
    'comissao_afiliado_pct': 0.20, 
    'comissao_afiliado_meses': 12,

    # ========================================================================
    # 9. RH & EQUIPE (GATILHOS AJUSTADOS)
    # ========================================================================
    'salario_fundador': 5000.00,    'trigger_fundador': 35000.00,  # Ajustado de 50k
    'salario_dev_senior': 10000.00, 'trigger_dev': 500,            # Ajustado de 750
    'salario_cs': 4500.00,          'trigger_cs': 800,             # Ajustado de 1000
    'encargos_trabalhistas': 0.70,

    # ========================================================================
    # 10. GOVERNANÇA, ADMIN & B2B
    # ========================================================================
    'custo_escritorio_base': 3500.00, 
    'trigger_escritorio': 150000.00,
    
    'custo_contabilidade_adv': 1000.00,
    'custo_juridico_compliance': 100.00,
    'trigger_contabilidade': 85000.00,
    
    'verba_viagens_base': 1.00, 
    'verba_viagens_pct_receita': 0.02,
    'trigger_viagens_receita': 45000.00,
    
    'conselho_jeton': 3000.00, 
    'trigger_conselho_mrr': 120000.00,
    
    'freelancers_trimestral': 1000.00,
    'trigger_freelancer_receita': 30000.00,
    
    'beneficios_executivos': 5000.00, 
    'trigger_beneficios_lucro': 100000.00, 
    
    'b2b_probabilidade_anual': 0.10, 
    'b2b_setup_fee': 15000.00,
    'b2b_custo_implantacao': 5000.00,

    # ========================================================================
    # 11. CAPITAL & CONTABILIDADE
    # ========================================================================
    'caixa_inicial': 5000.00,              # Ajustado de R$ 2k para R$ 5k
    'aporte_mensal': 3000.00,              # Ajustado de R$ 2k para R$ 3k
    'meses_aporte': 10,

    'threshold_caixa_quebra': -3000.0,
    'caixa_reserva_operacional': 5000.0,
    
    'capex_inicial': 1.00,
    'capex_recorrente_24m': 12000.00,     
    'tempo_depreciacao_equipamento_meses': 24,

    # ========================================================================
    # 12. DISTRIBUIÇÃO DE LUCROS
    # ========================================================================
    'percentual_distribuicao': 0.00,
    'split_fundador': 0.50,
    'split_investidor': 0.50,

    # ========================================================================
    # 13. BENCHMARKS & TRADUÇÕES
    # ========================================================================
    'benchmark_cac_m0': 500.0,
    'benchmark_cac_m6': 250.0,
    'benchmark_cac_m12': 250.0,
    'benchmark_cac_m36': 200.0,
    
    'benchmark_churn_m0': 0.12,
    'benchmark_churn_m6': 0.075,
    
    'benchmark_ltv_cac_m0': 2.0,
    'benchmark_ltv_cac_m6': 4.0,

    'benchmark_churn_atencao_pct': 5.0,
    'benchmark_churn_critico_pct': 7.0,
    'benchmark_margem_alvo_pct': 80.0,
    'benchmark_margem_critica_pct': 70.0,
    'benchmark_ltv_cac_excelente': 5.0,
    'benchmark_ltv_cac_atencao': 3.0,
    'benchmark_ltv_cac_critico': 1.0,
    'benchmark_ltv_cac_suspeito': 10.0,
    
    'traducoes': {
        'Runway': 'Runway (Sobrevivência / Pista de Pouso)',
        'Burn Rate': 'Burn Rate (Taxa de Queima / Queima de Caixa)',
        'Churn': 'Churn (Cancelamento / Evasão)',
        'LTV': 'LTV (Valor Vitalício do Cliente)',
        'CAC': 'CAC (Custo de Aquisição)',
        'Payback': 'Payback (Tempo de Retorno)',
        'Margem Contrib': 'Margem de Contribuição',
        'MRR': 'MRR (Receita Recorrente Mensal)',
        'ARR': 'ARR (Receita Anual Recorrente)',
        'ARPU': 'ARPU (Receita Média por Usuário)',
    },

    # ========================================================================
    # 14. METAS DO NEGÓCIO
    # ========================================================================
    'meta_caixa_seguranca': 50000.0,
    'meta_caixa_ideal': 100000.0,
    'meta_runway_minimo_meses': 6,

    # ========================================================================
    # 15. DESIGN SYSTEM (CORES)
    # ========================================================================
    'cores': {
        'primary': '#0F172A',
        'secondary': '#64748B',
        'background': '#FFFFFF',
        'grid': '#F1F5F9',
        'receita': '#10B981',
        'despesa': '#EF4444',
        'lucro': '#3B82F6',
        'ebitda': '#6366F1',
        'caixa': '#8B5CF6',
        'success': '#10B981',
        'danger': '#EF4444',
        'warning': '#F59E0B',
        'info': '#3B82F6',
        'marketing_pago': '#3B82F6',
        'marketing_organico': '#10B981',
        'infra': '#64748B',
        'cogs': '#E05D44',
        'opex': '#2684FF'
    }
}

# ============================================================================
# VALIDAÇÃO E DIAGNÓSTICO
# ============================================================================
if __name__ == "__main__":
    print("="*80)
    print("✅ PREMISSAS V9.2 CARREGADAS (GROWTH PARAMETRIZADO)")
    print("="*80)
    
    print(f"\n💰 RESUMO FINANCEIRO:")
    print(f"   • Caixa Inicial:        R$ {PREMISSAS['caixa_inicial']:,.2f}")
    print(f"   • Aporte Mensal:        R$ {PREMISSAS['aporte_mensal']:,.2f}")
    print(f"   • Budget Mkt Fixo:      R$ {PREMISSAS['marketing_fixo_mensal']:,.2f}")
    
    print(f"\n📈 MODELO DE CRESCIMENTO (TIERS):")
    for tier in PREMISSAS['growth_tiers']:
        print(f"   • R$ {tier['budget_min']:>6} - R$ {tier['budget_max']:>6}: {tier['taxa']*100:>4.1f}%/mês ({tier['nome']})")
    
    print(f"\n🎯 AJUSTES APLICADOS:")
    print(f"   • Usuários Iniciais: 5 → 10")
    print(f"   • Tráfego Inicial: 250 → 400")
    print(f"   • Conversão Trial→Pago: 12% → 16%")
    print(f"   • Churn Maturidade: 6% → 5%")
    print(f"   • Fator Viral: 2.5 → 3.5")
    print(f"   • Taxa Upgrade: 2% → 3%")
    print(f"   • Marketing Fixo: R$ 1.750 → R$ 2.500")
    print(f"   • Marketing % Receita: 40% → 25%")
    print(f"   • Caixa Inicial: R$ 2.000 → R$ 5.000")
    print(f"   • Aporte Mensal: R$ 2.000 → R$ 3.000")
    
    print("\n⭐ PRONTO PARA EXECUÇÃO (MOTOR V13.2)")
    print("="*80)