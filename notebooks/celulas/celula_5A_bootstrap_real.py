# CÉLULA 05A - EXECUÇÃO DO CENÁRIO REAL (BOOTSTRAP R$ 2k) V2.0
# ============================================================================
# OBJETIVO: Simular a realidade atual com recursos limitados.
# VERSÃO: 2.0 - Agora gera granularidades MENSAL, SEMANAL e DIÁRIA
# TEMPO DE EXECUÇÃO: ~10 segundos
# ============================================================================
# OUTPUTS GERADOS:
#   - df_real_m : DataFrame mensal (36 meses) [PRINCIPAL]
#   - df_real_a : DataFrame anual (3 anos) [AGREGADO]
#   - df_real_s : DataFrame semanal (26 semanas = M1-M6) [NOVO]
#   - df_real_d : DataFrame diário (180 dias = M1-M6) [NOVO]
#   - met_real  : Métricas consolidadas
#   - alertas_real : Lista de alertas gerados
# ============================================================================

import time

# Importa o motor de granularidade (se não estiver carregado)
try:
    from motor_granularidade import expandir_granularidade_completa
except ImportError:
    # Se executado no notebook, o motor já deve estar no namespace
    pass

print("="*80)
print("🚀 INICIANDO SIMULAÇÃO DO CENÁRIO REAL (BOOTSTRAP)")
print("="*80)
print(f"📅 Período: {PREMISSAS['meses_projecao']} meses ({PREMISSAS['meses_projecao']//12} anos)")
print(f"💰 Budget Marketing: R$ {PREMISSAS['marketing_fixo_mensal']:,.2f}/mês")
print(f"👥 Base Inicial: {PREMISSAS['usuarios_pagos_iniciais']} usuários pagantes")
print(f"🎯 Estratégia: Bootstrapping (Crescimento Orgânico + Ads Mínimo)")
print("-"*80)

start_time = time.time()

# ----------------------------------------------------------------------------
# EXECUÇÃO DO MOTOR COM PREMISSAS ATUAIS (SEM VARIAÇÕES)
# ----------------------------------------------------------------------------
df_real_m, df_real_a, met_real, alertas_real = executar_motor_fintech_v10_production_ready(
    PREMISSAS,
    seed=None,  # Usa seed padrão (42)
    variacao_params=None,  # Sem alterações
    modo_debug=False
)

tempo_exec_motor = time.time() - start_time

# ----------------------------------------------------------------------------
# EXPANSÃO DE GRANULARIDADE (SEMANAL + DIÁRIO) - V2.0
# ----------------------------------------------------------------------------
print("\n📐 Gerando granularidades semanal e diária...")

try:
    # Tenta usar a função do módulo importado
    df_real_s, df_real_d = expandir_granularidade_completa(
        df_real_m, 
        PREMISSAS, 
        meses_expandir=6,  # Expande os primeiros 6 meses
        seed=PREMISSAS.get('seed_fixa', 42)
    )
    print(f"   ✅ df_real_s: {len(df_real_s)} semanas geradas")
    print(f"   ✅ df_real_d: {len(df_real_d)} dias gerados")
except NameError:
    # Se a função não está disponível, cria DataFrames vazios com aviso
    import pandas as pd
    df_real_s = pd.DataFrame()
    df_real_d = pd.DataFrame()
    print("   ⚠️ Motor de granularidade não carregado. Execute celulas/motor_granularidade.py primeiro.")
    alertas_real.append({
        'tipo': 'granularidade_indisponivel',
        'mensagem': 'DataFrames semanal e diário não gerados. Carregue o motor_granularidade.py.'
    })

tempo_exec = time.time() - start_time

# ----------------------------------------------------------------------------
# EXTRAÇÃO DE MÉTRICAS CHAVE PARA ANÁLISE
# ----------------------------------------------------------------------------
# Snapshots temporais para análise de evolução
metricas_m6 = {
    'mrr': df_real_m.loc[5, 'mrr'],  # Mês 6 (índice 5)
    'usuarios': df_real_m.loc[5, 'usuarios_ativos'],
    'caixa': df_real_m.loc[5, 'caixa'],
    'cac': df_real_m.loc[5, 'cac_blended'],
    'ltv_cac': df_real_m.loc[5, 'ltv_cac'],
    'churn': df_real_m.loc[5, 'churn_rate'],
}

metricas_m12 = {
    'mrr': df_real_m.loc[11, 'mrr'],  # Mês 12 (índice 11)
    'usuarios': df_real_m.loc[11, 'usuarios_ativos'],
    'caixa': df_real_m.loc[11, 'caixa'],
    'cac': df_real_m.loc[11, 'cac_blended'],
    'ltv_cac': df_real_m.loc[11, 'ltv_cac'],
    'churn': df_real_m.loc[11, 'churn_rate'],
}

metricas_m36 = {
    'mrr': df_real_m.loc[35, 'mrr'],  # Mês 36 (índice 35)
    'usuarios': df_real_m.loc[35, 'usuarios_ativos'],
    'caixa': df_real_m.loc[35, 'caixa'],
    'cac': df_real_m.loc[35, 'cac_blended'],
    'ltv_cac': df_real_m.loc[35, 'ltv_cac'],
    'churn': df_real_m.loc[35, 'churn_rate'],
}

# Cálculos agregados
caixa_minimo = df_real_m['caixa'].min()
mes_caixa_minimo = df_real_m['caixa'].idxmin() + 1
break_even_mes = (df_real_m['lucro_liquido'] > 0).idxmax() + 1 if (df_real_m['lucro_liquido'] > 0).any() else None

# ----------------------------------------------------------------------------
# RELATÓRIO EXECUTIVO
# ----------------------------------------------------------------------------
print("\n" + "="*80)
print("✅ SIMULAÇÃO CONCLUÍDA - CENÁRIO REAL")
print("="*80)
print(f"⏱️  Tempo de Execução: {tempo_exec:.2f} segundos")
print()

print("📊 RESUMO FINANCEIRO - MARCOS TEMPORAIS")
print("-"*80)
print(f"{'Métrica':<25} {'Mês 6':<15} {'Mês 12':<15} {'Mês 36':<15}")
print("-"*80)
print(f"{'MRR':<25} R$ {metricas_m6['mrr']:>10,.2f}  R$ {metricas_m12['mrr']:>10,.2f}  R$ {metricas_m36['mrr']:>10,.2f}")
print(f"{'Usuários Ativos':<25} {metricas_m6['usuarios']:>13,.0f}  {metricas_m12['usuarios']:>13,.0f}  {metricas_m36['usuarios']:>13,.0f}")
print(f"{'Caixa':<25} R$ {metricas_m6['caixa']:>10,.2f}  R$ {metricas_m12['caixa']:>10,.2f}  R$ {metricas_m36['caixa']:>10,.2f}")
print(f"{'CAC':<25} R$ {metricas_m6['cac']:>10,.2f}  R$ {metricas_m12['cac']:>10,.2f}  R$ {metricas_m36['cac']:>10,.2f}")
print(f"{'LTV/CAC':<25} {metricas_m6['ltv_cac']:>13,.2f}  {metricas_m12['ltv_cac']:>13,.2f}  {metricas_m36['ltv_cac']:>13,.2f}")
print(f"{'Churn Rate':<25} {metricas_m6['churn']*100:>12,.1f}%  {metricas_m12['churn']*100:>12,.1f}%  {metricas_m36['churn']*100:>12,.1f}%")
print("-"*80)

print()
print("🎯 MÉTRICAS DE SAÚDE DO NEGÓCIO")
print("-"*80)
print(f"💰 MRR Final (Mês 36):        R$ {met_real['mrr_final']:,.2f}")
print(f"📈 ARR Final (Mês 36):        R$ {met_real['arr_final']:,.2f}")
print(f"👥 Usuários Finais:           {met_real['usuarios_final']:,}")
print(f"💵 Caixa Final:               R$ {met_real['caixa_final']:,.2f}")
print(f"🔻 Caixa Mínimo:              R$ {caixa_minimo:,.2f} (Mês {mes_caixa_minimo})")
print(f"⚖️  Break-Even:               {'Mês ' + str(break_even_mes) if break_even_mes else 'Não atingido'}")
print()

print("📐 UNIT ECONOMICS (MÉDIAS)")
print("-"*80)
print(f"💳 CAC Médio:                 R$ {met_real['cac_medio']:,.2f}")
print(f"💎 LTV Médio:                 R$ {met_real['ltv_media']:,.2f}")
print(f"🎯 LTV/CAC Médio:             {met_real['ltv_media']/met_real['cac_medio']:.2f}x")
print(f"📊 Margem Bruta Média:        {met_real['margem_bruta_media']:.1f}%")
print(f"💰 Margem EBITDA Média:       {met_real['ebitda_margin_media']:.1f}%")
print(f"🔄 Churn Médio:               {met_real['churn_medio']:.1f}%")
print()

# ----------------------------------------------------------------------------
# VALIDAÇÃO CONTRA BENCHMARKS
# ----------------------------------------------------------------------------
print("✅ VALIDAÇÃO CONTRA BENCHMARKS DA INDÚSTRIA")
print("-"*80)

# LTV/CAC
ltv_cac_final = met_real['ltv_media'] / met_real['cac_medio']
if ltv_cac_final >= PREMISSAS['benchmark_ltv_cac_excelente']:
    status_ltv_cac = "🟢 EXCELENTE"
elif ltv_cac_final >= PREMISSAS['benchmark_ltv_cac_atencao']:
    status_ltv_cac = "🟡 BOM"
else:
    status_ltv_cac = "🔴 CRÍTICO"
print(f"LTV/CAC: {ltv_cac_final:.2f}x {status_ltv_cac}")

# Churn
churn_final_pct = metricas_m36['churn'] * 100
if churn_final_pct <= PREMISSAS['benchmark_churn_atencao_pct']:
    status_churn = "🟢 SAUDÁVEL"
elif churn_final_pct <= PREMISSAS['benchmark_churn_critico_pct']:
    status_churn = "🟡 ATENÇÃO"
else:
    status_churn = "🔴 ALTO"
print(f"Churn: {churn_final_pct:.1f}% {status_churn}")

# Margem Bruta
if met_real['margem_bruta_media'] >= PREMISSAS['benchmark_margem_alvo_pct']:
    status_margem = "🟢 FORTE"
elif met_real['margem_bruta_media'] >= PREMISSAS['benchmark_margem_critica_pct']:
    status_margem = "🟡 ACEITÁVEL"
else:
    status_margem = "🔴 FRACA"
print(f"Margem Bruta: {met_real['margem_bruta_media']:.1f}% {status_margem}")

print()
print("="*80)
print("📁 DADOS GERADOS (CENÁRIO REAL - BOOTSTRAP):")
print("-"*80)
print("   • df_real_m : DataFrame MENSAL (36 meses, 107 colunas)")
print("   • df_real_a : DataFrame ANUAL (3 anos, agregado)")
print("   • df_real_s : DataFrame SEMANAL (26 semanas = M1-M6) [NOVO V2.0]")
print("   • df_real_d : DataFrame DIÁRIO (180 dias = M1-M6) [NOVO V2.0]")
print("   • met_real  : Métricas consolidadas (dict)")
print("   • alertas_real : Lista de alertas gerados")
print("-"*80)
print("⭐ PRONTO PARA ANÁLISE E COMPARAÇÃO COM CENÁRIO IDEAL")
print("="*80)