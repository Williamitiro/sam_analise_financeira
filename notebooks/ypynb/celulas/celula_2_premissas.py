# CÉLULA 02 - PREMISSAS V9.0 - PAINEL DE CONTROLE MASTER (HUMAN READABLE)
# ============================================================================
# DOCUMENTAÇÃO E ESTRATÉGIA
# ============================================================================
# CENÁRIO: BOOTSTRAPPING (Validação com Recursos Próprios)
#
# 4. CAPEX: R$ 0,00 (Hardware/PC assumido na Pessoa Física)
#
# REGRAS DE GROWTH:
# 1. Metas são definidas MENSALMENTE.
# 2. A taxa SEMANAL é calculada matematicamente no final desta célula.
# ============================================================================

PREMISSAS = {
    # ========================================================================
    # 1. METADADOS & CONTROLE DE TEMPO
    # ========================================================================
    'meta_version': '9.0-full-documented',
    'meta_updated_at': '2025-12-01',
    
    'data_inicio': '2026-06-01',
    'meses_projecao': 36,       # 3 anos de visão
    'seed_fixa': 42,            # Para reprodutibilidade (Monte Carlo)
    
    # Convenções de Tempo
    'semanas_por_mes': 4.33,
    'meses_por_ano': 12,

    # ========================================================================
    # 2. SAZONALIDADE DO MERCADO (CALENDÁRIO B3)
    # ========================================================================
    # Fator multiplicador sobre o tráfego base.
    # Jan (1.30) é forte (começo de ano), Dez (0.75) é fraco (festas).
    'sazonalidade_trafego': {
        1: 1.30,  2: 1.10,  3: 1.15, 
        4: 1.00,  5: 1.05,  6: 1.00,
        7: 0.85,  8: 1.00,  9: 1.00, 
        10: 1.05, 11: 1.10, 12: 0.75
    },

    # ========================================================================
    # 3. AQUISIÇÃO, GROWTH & METAS
    # ========================================================================
    'usuarios_pagos_iniciais': 5,  # Começamos pequenos
    'trafego_inicial': 500,        # Visitas no site/app
    
    # --- METAS DE CRESCIMENTO MENSAL (DRIVERS) ---
    # A meta semanal será calculada baseada nestes números no final do script.
    'crescimento_trafego_mes_1_6': 0.05,      # 25% ao mês (Fase Validação)
    'crescimento_trafego_mes_7_12': 0.07,     # 7% ao mês (Fase Consolidação)
    'crescimento_trafego_mes_13_plus': 0.04,  # 4% ao mês (Fase Escala)

    # Parâmetros de Mercado
    'mercado_potencial_traders': 150000,        # [usuários] TAM para curva S viral
    
    # Configuração da Validação Semanal
    'semanas_validacao_m0_m6': 26,            # Duração da fase crítica (6 meses)

    # --- FUNIL DE VENDAS ---
    'taxa_visitante_para_trial': 0.05,        # 5% dos visitantes testam
    'taxa_trial_para_pagante': 0.12,          # 12% dos testers pagam
    
    # Eficiência do Time (Ramp-up)
    'ramp_up_inicial': 0.50,                  # Começamos com 50% de eficiência
    'ramp_up_incremento': 0.06,               # Melhora 6% ao mês até 100%
    
    # --- CRESCIMENTO ORGÂNICO (SEO/INDICAÇÃO) ---
    'fator_visitas_organicas_por_pagante': 2.5, # Cada cliente atrai 2.5 visitantes
    'taxa_crescimento_organico_base': 0.02,     # SEO melhora 2% ao mês
    'elasticidade_organico': 0.60,              # Fator de viralidade
    'alerta_dependencia_organica_pct': 50.0,    # Alerta se depender <50% de orgânico

    # ========================================================================
    # 4. CHURN & RETENÇÃO (CANCELAMENTO)
    # ========================================================================
    # Traders trocam muito de plataforma no início.
    'churn_inicial': 0.12,                    # 12% ao mês (Mês 1)
    'churn_maturidade': 0.06,                 # 6% ao mês (Meta Longo Prazo)
    'churn_base': 0.07,                       # Média para cálculos simples
    'churn_decaimento_mensal': 0.0015,        # Melhora 0.15% a cada mês
    'taxa_reativacao_base_cancelada': 0.01,   # 1% dos cancelados voltam

    # ========================================================================
    # 5. PRICING & MIX DE PRODUTOS
    # ========================================================================
    # Preços das Assinaturas
    'preco_lite': 69.90, 
    'preco_trader': 99.90, 
    'preco_pro': 169.90,
    
    # Distribuição dos Clientes (Mix)
    'mix_lite': 0.50,                         # 50% no plano básico
    'mix_trader': 0.35,                       # 35% no intermediário
    'mix_pro': 0.15,                          # 15% no avançado
    'taxa_upgrade_lite_trader': 0.02,         # 2% sobem de plano/mês
    
    # --- MEIOS DE PAGAMENTO ---
    'mix_pagamento_cartao': 0.55, 
    'mix_pagamento_pix': 0.40, 
    'mix_pagamento_boleto': 0.05,
    
    # Custos Financeiros (Taxas)
    'taxa_processamento_cartao': 0.045,       # 4.5%
    'taxa_processamento_pix': 0.01,           # 1.0%
    'taxa_processamento_boleto': 0.035,       # 3.5%
    'taxa_chargeback': 0.005,                 # 0.5% fraude/estorno
    
    # Inadimplência Realista
    'taxa_inadimplencia_cartao': 0.04,
    'taxa_inadimplencia_pix': 0.08,           # Pix agendado que não paga
    'taxa_inadimplencia_boleto': 0.02,
    
    # Regime Tributário
    'imposto_simples_inicial': 0.06,          # 6% (Anexo III)
    'imposto_lucro_presumido': 0.1633,        # 16.33% (Se estourar o teto)
    'threshold_regime_tributario': 4800000.00,# Teto Simples Nacional

    # ========================================================================
    # 6. INFRAESTRUTURA & CUSTOS VARIÁVEIS (TIERS)
    # ========================================================================
    # Custo Variável por Usuário (IA Tokens + Server Load)
    'custo_ia_lite': 3.00, 
    'custo_ia_trader': 5.00, 
    'custo_ia_pro': 13.00,
    
    'custo_ferramentas_base': 1.00,         # Ferramentas fixas (Jira, etc), já está nos custos de ferramentas do tier 1!!!
    'custo_suporte_por_1000_users': 1.00,   # Zendesk variável - não tem agoagora eu o fundador vou dar suporte e vou automatizar!!!
    
    # Limites para Mudança de Tier (Escalabilidade)
    'infra_tier_1_limite': 500,
    'infra_tier_2_limite': 1500,
    'infra_tier_3_limite': 5000,
    'infra_tier_4_limite': 10000,

    # --- TIER 1: VALIDAÇÃO (0 - 500 usuários) ---
    't1_vps_app_api': 120.00, 
    't1_vps_windows_mt5': 180.00, 
    't1_database_managed': 80.00,
    't1_storage_s3': 20.00, 
    't1_ferramentas_dev': 300.00, 
    't1_observability': 0.00,
    't1_scraping_news': 100.00, 
    't1_dominio_dns': 10.00, 
    't1_email_transacional': 50.00,
    
    # --- TIER 2: GROWTH (501 - 1500 usuários) ---
    't2_api_dados_b3': 5000.00, 
    't2_compute_app': 450.00, 
    't2_database_primary': 350.00,
    't2_cache_redis': 120.00, 
    't2_storage_s3': 100.00, 
    't2_security_waf': 120.00,
    't2_ferramentas_dev': 600.00, 
    't2_observability': 250.00, 
    't2_suporte_ticket': 300.00,
    
    # --- TIER 3: SCALE (1501 - 5000 usuários) ---
    't3_api_dados_b3_pro': 7000.00, 
    't3_load_balancer': 200.00, 
    't3_compute_cluster': 1500.00,
    't3_db_primary_replica': 1200.00, 
    't3_cache_cluster': 400.00, 
    't3_data_warehouse': 500.00,
    't3_security_advanced': 500.00, 
    't3_ci_cd_pipeline': 300.00, 
    't3_observability_pro': 1000.00,
    
    # --- TIER 4: ENTERPRISE (5001+ usuários) ---
    't4_api_dados_institutional': 10000.00, 
    't4_k8s_cluster': 4500.00,
    't4_db_aurora_serverless': 3000.00, 
    't4_data_lake_engineering': 2000.00,
    't4_security_soc': 2500.00, 
    't4_support_enterprise': 1500.00, 
    't4_multi_region_backup': 1000.00,

    # ========================================================================
    # 7. MARKETING (REALIDADE BOOTSTRAPPING)
    # ========================================================================
    # R$ 2.000 é o teto máximo.
    # O script de validação vai checar se isso paga o CAC.
    'marketing_fixo_mensal': 1500.00,
    'marketing_perc_receita': 0.40,           # Reinveste 40% da receita em ads
    'marketing_teto': 25000.00,               # Teto futuro

    # Parâmetros de Growth
    'marketing_budget_ref_brand_lift': 3000.0,  # [R$] Budget onde Brand Lift atinge 50%
    'limite_inventario_mensal': 50000,          # [visitas] Máximo de visitas pagas (saturação)
    
    # Mix de Canais (Onde gastamos o dinheiro)
    'canal_instagram_pct': 0.35, 'cpc_instagram': 0.60, 'conv_instagram': 0.03,
    'canal_facebook_pct': 0.20,  'cpc_facebook': 0.80,  'conv_facebook': 0.02,
    'canal_youtube_pct': 0.35,   'cpc_youtube': 3.00,   'conv_youtube': 0.09,
    'canal_google_pct': 0.10,    'cpc_google': 6.00,    'conv_google': 0.12,

    # ========================================================================
    # 8. PROGRAMA DE AFILIADOS
    # ========================================================================
    'modelo_afiliado_habilitado': False,
    'pct_usuarios_via_afiliado': 0.15,        # 15% das vendas vêm daqui
    'comissao_afiliado_tipo': 'primeira_mensalidade', # Paga só a 1ª
    'comissao_afiliado_fixo': 50.00, 
    'comissao_afiliado_pct': 0.20, 
    'comissao_afiliado_meses': 12,

    # ========================================================================
    # 9. RH & EQUIPE (GATILHOS DE CONTRATAÇÃO)
    # ========================================================================
    # Só contrata se atingir gatilhos de Receita ou Usuários
    'salario_fundador': 5000.00,    'trigger_fundador': 25000.00, # MRR > 25k
    'salario_dev_senior': 10000.00, 'trigger_dev': 750,           # Users > 750
    'salario_cs': 4500.00,          'trigger_cs': 1000,           # Users > 1000
    'encargos_trabalhistas': 0.70,  # CLT + Benefícios

    # ========================================================================
    # 10. GOVERNANÇA, ADMIN & B2B
    # ========================================================================
    'custo_escritorio_base': 3500.00, 
    'trigger_escritorio': 150000.00,           # Só aluga sala se faturar 150k
    
    'custo_contabilidade_adv': 1000.00,       # Contador
    'custo_juridico_compliance': 100.00,
    'trigger_contabilidade': 85000.00,      #adicionado agora, precisa corrigir motor e outras celular
    
    'verba_viagens_base': 1.00, 
    'verba_viagens_pct_receita': 0.02,
    'trigger_viagens_receita': 45000.00,
    
    'conselho_jeton': 3000.00, 
    'trigger_conselho_mrr': 120000.00,
    
    'freelancers_trimestral': 1000.00,
    'trigger_freelancer_receita': 30000.00,
    
    'beneficios_executivos': 5000.00, 
    'trigger_beneficios_lucro': 100000.00, 
    
    # B2B (Venda para Escolas/Mesas)
    'b2b_probabilidade_anual': 0.10, 
    'b2b_setup_fee': 15000.00,
    'b2b_custo_implantacao': 5000.00,


  
    # ========================================================================
    # 11. CAPITAL & CONTABILIDADE (REALIDADE DO CLIENTE)
    # ========================================================================
    'caixa_inicial': 4000.00,       # Dinheiro na conta hoje
    'aporte_mensal': 2000.00,       # Quanto entra por mês
    'meses_aporte': 10,             # Garantia de aporte por 6 meses, não mexe nisso!!!

    # --- NOVAS VARIÁVEIS OBRIGATÓRIAS (V12.0) ---
    # Parâmetros de Segurança
    'threshold_caixa_quebra': -3000.0,          # [R$] Nível de caixa que define falência técnica
    'caixa_reserva_operacional': 500.0,        # [R$] Mínimo de caixa antes de cortar MKT
    
    'capex_inicial': 1.00,          # PC comprado na PF (Zero custo empresa)
    'capex_recorrente_24m': 12000.00,     
    'tempo_depreciacao_equipamento_meses': 24,

    # ========================================================================
    # 12. DISTRIBUIÇÃO DE LUCROS
    # ========================================================================
    'percentual_distribuicao': 0.00, # 0% - Reinvestimento total na fase inicial
    'split_fundador': 0.50,
    'split_investidor': 0.50,

    # ========================================================================
    # 13. BENCHMARKS & TRADUÇÕES (OBRIGATÓRIOS)
    # ========================================================================
    # Benchmarks Fintech B2C (Validação M0-M6)
    'benchmark_cac_m0': 500.0,
    'benchmark_cac_m6': 250.0,
    'benchmark_cac_m12': 250.0,
    'benchmark_cac_m36': 200.0,
    
    'benchmark_churn_m0': 0.12,
    'benchmark_churn_m6': 0.075,
    
    'benchmark_ltv_cac_m0': 2.0,
    'benchmark_ltv_cac_m6': 4.0,

    # Benchmarks para Validação Final (Status Report)
    'benchmark_churn_atencao_pct': 5.0,
    'benchmark_churn_critico_pct': 7.0,
    'benchmark_margem_alvo_pct': 80.0,
    'benchmark_margem_critica_pct': 70.0,
    'benchmark_ltv_cac_excelente': 5.0,
    'benchmark_ltv_cac_atencao': 3.0,
    'benchmark_ltv_cac_critico': 1.0,
    'benchmark_ltv_cac_suspeito': 10.0,
    
    # Traduções Obrigatórias (Zero Jargão)
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
    # 14. METAS DO NEGÓCIO (OBJETIVOS)
    # ========================================================================
    'meta_caixa_seguranca': 50000.0,
    'meta_caixa_ideal': 100000.0,
    'meta_runway_minimo_meses': 6,

    # ========================================================================
    # 15. MONTE CARLO (SIMULAÇÃO DE RISCO)
    # ========================================================================
    #'mc_n_simulacoes': 1,
    #'mc_prob_atraso_aporte': 0.20,
    #'mc_std_churn': 0.30,
    #'mc_std_vis_trial': 0.30,
    #'mc_std_trial_pag': 0.30,
    #'mc_std_cresc_traf': 0.35,
    #'mc_std_marketing': 0.15,
    #'mc_std_infra': 0.15,
    #'mc_std_taxa_pag': 0.005,
    #'mc_std_mix_lite': 0.10,
    #'mc_var_ia_otimista': 0.80,
    #'mc_var_ia_pessimista': 1.50,
    
    # ========================================================================
    # 16. DESIGN SYSTEM (CORES COMPLETAS)
    # ========================================================================
    'cores': {
        'primary': '#0F172A',    # Navy Blue (Principal)
        'secondary': '#64748B',  # Slate (Secundário)
        'background': '#FFFFFF', # Branco (Fundo)
        'grid': '#F1F5F9',       # Cinza Claro (Linhas)
        
        # Cores Semânticas
        'receita': '#10B981',    # Verde (Entrada)
        'despesa': '#EF4444',    # Vermelho (Saída)
        'lucro': '#3B82F6',      # Azul (Resultado)
        'ebitda': '#6366F1',     # Indigo (Operacional)
        'caixa': '#8B5CF6',      # Roxo (Acumulado)
        
        # Status
        'success': '#10B981',    # Sucesso
        'danger': '#EF4444',     # Perigo
        'warning': '#F59E0B',    # Atenção
        'info': '#3B82F6',       # Informativo
        
        # Categorias
        'marketing_pago': '#3B82F6',
        'marketing_organico': '#10B981',
        'infra': '#64748B',
        'cogs': '#E05D44',
        'opex': '#2684FF'

    }
}

# ============================================================================
# CONFIGURAÇÃO DO MONTE CARLO (CÉLULA 05C)
# ============================================================================
#PREMISSAS['mc_n_simulacoes'] = 1  # Quantidade de cenários

#PREMISSAS['mc_variaveis'] = {
    # VARIÁVEIS DE GROWTH
#    'marketing_fixo_mensal': {'dist': 'normal', 'std': 0.15, 'min': 500}, # Pode variar +/- 15%
#    'cpc_instagram':         {'dist': 'scale',  'std': 0.20, 'min': 0.10, 'max': 3.0}, # CPC flutua
#    'taxa_visitante_para_trial': {'dist': 'normal', 'std': 0.10, 'min': 0.01, 'max': 0.15},
#    'taxa_trial_para_pagante':   {'dist': 'normal', 'std': 0.15, 'min': 0.05, 'max': 0.20},
    
    # VARIÁVEIS DE RETENÇÃO
#    'churn_base':            {'dist': 'normal', 'std': 0.20, 'min': 0.03, 'max': 0.15},
    
    # VARIÁVEIS FINANCEIRAS
#    'b2b_probabilidade_anual': {'dist': 'uniform', 'min': 0.10, 'max': 0.50}, # Incerteza alta no B2B
#    'aporte_mensal':         {'dist': 'normal', 'std': 0.05, 'min': 1500}, # Risco baixo no aporte
    
    # VARIÁVEIS MACRO
#    'crescimento_trafego_mes_1_6': {'dist': 'normal', 'std': 0.20, 'min': 0.05, 'max': 0.30},
#}



# ============================================================================
# CÁLCULOS AUTOMÁTICOS (PÓS-CONFIGURAÇÃO)
# ============================================================================
# Aqui transformamos a meta mensal em meta semanal matematicamente.
# Não há "outra meta", é a MESMA meta, convertida.

taxa_mensal_meta = PREMISSAS['crescimento_trafego_mes_1_6']
semanas_no_mes = PREMISSAS['semanas_por_mes']

# Fórmula de juros compostos: (1 + Mensal) = (1 + Semanal) ^ Semanas
# Logo: Semanal = (1 + Mensal)^(1/Semanas) - 1
taxa_semanal_calc = (1 + taxa_mensal_meta) ** (1 / semanas_no_mes) - 1

# Atualiza no dicionário
PREMISSAS['taxa_crescimento_semanal_m0_m6'] = taxa_semanal_calc

if __name__ == "__main__":
    print("="*80)
    print("✅ PREMISSAS V9.0 CARREGADAS E CALCULADAS")
    print("="*80)
    
    print(f"💰 RESUMO FINANCEIRO:")
    print(f"   • Caixa Inicial:        R$ {PREMISSAS['caixa_inicial']:,.2f}")
    print(f"   • Aporte Mensal:        R$ {PREMISSAS['aporte_mensal']:,.2f}")
    print(f"   • Budget Mkt Mensal:    R$ {PREMISSAS['marketing_fixo_mensal']:,.2f}")

    print(f"\n📈 METAS TRAFEGO CONVERTIDAS:")
    print(f"   • Meta Mensal Definida: {taxa_mensal_meta*100:.1f}%")
    print(f"   • Meta Semanal Calc.:   {taxa_semanal_calc*100:.2f}% (Matematicamente equivalente)")

    print(f"\n🎨 CORES CARREGADAS: {len(PREMISSAS['cores'])} definições.")
    print("⭐ PRONTO PARA EXECUÇÃO.")