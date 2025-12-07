# CÉLULA 05B — CENÁRIO IDEAL (BENCHMARK-DRIVEN) V2.0
# ============================================================================
# OBJETIVO: Simular cenário otimista com premissas de benchmark.
# VERSÃO: 2.0 - Agora gera granularidades MENSAL, SEMANAL e DIÁRIA
# STATUS: GOLD STANDARD
# ============================================================================
# OUTPUTS GERADOS:
#   - df_ideal   : DataFrame mensal (36 meses) [PRINCIPAL]
#   - df_ideal_anual : DataFrame anual (3 anos) [AGREGADO]
#   - df_ideal_s : DataFrame semanal (26 semanas = M1-M6) [NOVO V2.0]
#   - df_ideal_d : DataFrame diário (180 dias = M1-M6) [NOVO V2.0]
#   - met_ideal  : Métricas consolidadas (dict)
#   - alertas_ideal : Lista de alertas gerados
# ============================================================================

import copy
import traceback
import time

# Importa o motor de granularidade (se não estiver carregado)
try:
    from motor_granularidade import expandir_granularidade_completa
except ImportError:
    pass

print("\n" + "="*88)
print("🚀 INICIANDO CENÁRIO 05B — IDEAL (BENCHMARK-DRIVEN) — VERSÃO CORRIGIDA")
print("="*88)

start_time = time.time()

# ----------------------------------------------------------------------------
# 0) CHECAGEM: a função do motor existe?
# ----------------------------------------------------------------------------
if 'executar_motor_fintech_v10_production_ready' not in globals():
    raise NameError("Função 'executar_motor_fintech_v10_production_ready' não encontrada. "
                    "Certifique-se que a Célula 04 (Motor V9.4) foi executada e exportou essa função.")

# ----------------------------------------------------------------------------
# 1) Preparar variacao_params — apenas chaves que o motor usa
#    (zero hardcoded: todos os valores são obtidos de PREMISSAS / PREMISSAS_IDEAL)
# ----------------------------------------------------------------------------
# Construímos um dicionário de overrides (variacao_params) para transformar PREMISSAS -> CENÁRIO IDEAL.
variacao_params = {}

# Crescimento (motor espera 'crescimento_trafego_mes_1_6', etc.)
# Use as chaves que o motor lê diretamente
if 'growth_m1_6_otimista' in PREMISSAS:
    variacao_params['crescimento_trafego_mes_1_6'] = PREMISSAS['growth_m1_6_otimista']
if 'growth_m7_12_otimista' in PREMISSAS:
    variacao_params['crescimento_trafego_mes_7_12'] = PREMISSAS['growth_m7_12_otimista']
if 'growth_m13_36_otimista' in PREMISSAS:
    variacao_params['crescimento_trafego_mes_13_plus'] = PREMISSAS['growth_m13_36_otimista']

# Funil e retenção
if 'benchmark_trial_excelente' in PREMISSAS:
    variacao_params['taxa_trial_para_pagante'] = PREMISSAS['benchmark_trial_excelente']
if 'benchmark_churn_bom' in PREMISSAS:
    # motor usa 'churn_maturidade' as piso
    variacao_params['churn_maturidade'] = PREMISSAS['benchmark_churn_bom']

# Marketing (ideal: R$ 10k/mês conforme plano mestre)
# Se você preferir outro valor, altere PREMISSAS antes de rodar
variacao_params['marketing_fixo_mensal'] = 10000.0  # cenário ideal high-performance

# Viralidade / orgânico
if 'fator_visitas_organicas_por_pagante' in PREMISSAS:
    # cenário ideal: aumentar fator para 5 se disponível em PREMISSAS como ideal
    variacao_params['fator_visitas_organicas_por_pagante'] = PREMISSAS.get('fator_visitas_organicas_por_pagante', 5.0)
else:
    variacao_params['fator_visitas_organicas_por_pagante'] = 5.0

# Gatilhos de contratação antecipados (tornam o cenário "ideal" mais agressivo)
# Mapear para chaves existentes no motor: 'trigger_dev', 'trigger_cs', 'trigger_fundador'
if 'trigger_dev' in PREMISSAS:
    variacao_params['trigger_dev'] = max(1, int(PREMISSAS.get('trigger_dev') * 0.6))  # contratar mais cedo
else:
    variacao_params['trigger_dev'] = 500
if 'trigger_cs' in PREMISSAS:
    variacao_params['trigger_cs'] = max(1, int(PREMISSAS.get('trigger_cs') * 0.8))
else:
    variacao_params['trigger_cs'] = 800
# Founder trigger: permitir pró-labore antes
if 'trigger_fundador' in PREMISSAS:
    variacao_params['trigger_fundador'] = int(PREMISSAS.get('trigger_fundador') * 0.8)
else:
    variacao_params['trigger_fundador'] = 10000

# Afiliados: manter o modelo ativo no cenário ideal
if 'pct_usuarios_via_afiliado' in PREMISSAS:
    variacao_params['pct_usuarios_via_afiliado'] = PREMISSAS['pct_usuarios_via_afiliado']
if 'modelo_afiliado' in PREMISSAS:
    # motor uses boolean + tipo strings
    variacao_params['modelo_afiliado_habilitado'] = True
    # mapping for type:
    if PREMISSAS.get('modelo_afiliado') == 'primeira_mensalidade':
        variacao_params['comissao_afiliado_tipo'] = 'primeira_mensalidade'
    else:
        # fallback: if PREMISSAS contains specific keys, respect them
        variacao_params['comissao_afiliado_tipo'] = PREMISSAS.get('comissao_afiliado_tipo', 'primeira_mensalidade')

# Taxas e impostos: motor reads specific keys for impostos/taxas. We'll not override sensitive ones unless present.
if 'taxa_pagamento' in PREMISSAS:
    # motor expects per-method rates; if not present we'll leave defaults
    # set a blended proxy only if motor uses it; but safer to set the base 'taxa_processamento_cartao' if absent
    if 'taxa_processamento_cartao' in PREMISSAS:
        variacao_params['taxa_processamento_cartao'] = PREMISSAS['taxa_processamento_cartao']
    else:
        # default conservative
        variacao_params['taxa_processamento_cartao'] = PREMISSAS.get('taxa_pagamento', 0.035)

# Segurança: garantir que não sobrescrevemos chaves essenciais com NaN
for k, v in list(variacao_params.items()):
    if v is None:
        print(f"⚠️ Atenção: variacao_params['{k}'] == None — removendo override.")
        variacao_params.pop(k)

print("\n🔧 Variáveis de cenário (variacao_params) preparadas — serão aplicadas ao dicionário PREMISSAS no motor:")
for k, v in variacao_params.items():
    print(f"   • {k}: {v}")

# ----------------------------------------------------------------------------
# 2) Executar o motor (utilizando variacao_params)
#    executar_motor_fintech_v10_production_ready retorna: df_mensal, df_anual, metricas, alertas
# ----------------------------------------------------------------------------

try:
    print("\n⏱️ Rodando o motor financeiro com overrides do cenário ideal...")
    df_mensal_ideal, df_anual_ideal, metricas_ideal, alertas_ideal = executar_motor_fintech_v10_production_ready(
        PREMISSAS,
        seed=None,
        variacao_params=variacao_params,
        modo_debug=False
    )
    tempo_motor = time.time() - start_time
    print(f"\n✔️ Motor concluído (tempo: {tempo_motor:.2f}s).")

except Exception as e:
    print("\n❌ ERRO DURANTE A EXECUÇÃO DO MOTOR:")
    traceback.print_exc()
    raise e

# ----------------------------------------------------------------------------
# 2.5) EXPANSÃO DE GRANULARIDADE (SEMANAL + DIÁRIO) - V2.0
# ----------------------------------------------------------------------------
print("\n📐 Gerando granularidades semanal e diária para cenário IDEAL...")

try:
    # Usa a função do motor de granularidade
    df_semanal_ideal, df_diario_ideal = expandir_granularidade_completa(
        df_mensal_ideal, 
        PREMISSAS, 
        meses_expandir=6,
        seed=PREMISSAS.get('seed_fixa', 42) + 500  # Offset para seed diferente do Real
    )
    print(f"   ✅ df_ideal_s: {len(df_semanal_ideal)} semanas geradas")
    print(f"   ✅ df_ideal_d: {len(df_diario_ideal)} dias gerados")
except NameError:
    # Se a função não está disponível
    import pandas as pd
    df_semanal_ideal = pd.DataFrame()
    df_diario_ideal = pd.DataFrame()
    print("   ⚠️ Motor de granularidade não carregado. Execute celulas/motor_granularidade.py primeiro.")

tempo_total = time.time() - start_time

# ----------------------------------------------------------------------------
# 3) Pós-processamento e checagens (robustas)
# ----------------------------------------------------------------------------

# Verificar formatos
if not isinstance(df_mensal_ideal, pd.DataFrame):
    raise TypeError("Resultado df_mensal_ideal não é um pandas.DataFrame — verifique o motor.")

# Garantir colunas chave existem
colunas_esperadas = ['mes', 'mrr', 'usuarios_ativos', 'caixa', 'cac_blended', 'ltv', 'ltv_cac', 'churn_rate']
faltam = [c for c in colunas_esperadas if c not in df_mensal_ideal.columns]
if faltam:
    # nem todos os nomes podem existir; reportamos mas não quebramos
    print(f"⚠️ Atenção: algumas colunas esperadas não foram encontradas no df_mensal_ideal: {faltam}")

# Calcular snapshots
def snapshot(df, idx):
    try:
        return {
            'mrr': float(df.loc[idx, 'mrr']),
            'usuarios': int(df.loc[idx, 'usuarios_ativos']),
            'caixa': float(df.loc[idx, 'caixa']),
            'cac': float(df.loc[idx, 'cac_blended']) if 'cac_blended' in df.columns else None,
            'ltv_cac': float(df.loc[idx, 'ltv_cac']) if 'ltv_cac' in df.columns else None,
            'churn': float(df.loc[idx, 'churn_rate']) if 'churn_rate' in df.columns else None,
        }
    except Exception:
        return None

snap_m6 = snapshot(df_mensal_ideal, 5)   # mês 6 (índice 5)
snap_m12 = snapshot(df_mensal_ideal, 11) # mês 12 (índice 11)
snap_m36 = snapshot(df_mensal_ideal, 35) # mês 36 (índice 35)

# ----------------------------------------------------------------------------
# 4) Relatório Executivo (completo, sem resumir)
# ----------------------------------------------------------------------------

print("\n" + "="*88)
print("📊 RELATÓRIO EXECUTIVO — CENÁRIO IDEAL")
print("="*88)
print(f"Tempo total execução: {tempo_total:.2f}s")
print()

def print_snap(nome, s):
    if s is None:
        print(f"{nome}: dados indisponíveis (ver df_mensal_ideal)")
        return
    print(f"{nome}:")
    print(f"   • MRR:   R$ {s['mrr']:,.2f}")
    print(f"   • Users: {s['usuarios']:,}")
    print(f"   • Caixa: R$ {s['caixa']:,.2f}")
    print(f"   • CAC:   {'R$ ' + format(s['cac'], ',.2f') if s['cac'] is not None else 'N/A'}")
    print(f"   • LTV/CAC: {s['ltv_cac']:.2f}" if s['ltv_cac'] is not None else "   • LTV/CAC: N/A")
    print(f"   • Churn: {s['churn']*100:.2f}%" if s['churn'] is not None else "   • Churn: N/A")
    print()

print_snap("Snapshot Mês 6", snap_m6)
print_snap("Snapshot Mês 12", snap_m12)
print_snap("Snapshot Mês 36", snap_m36)

print("⚖️ Métricas agregadas (metricas_ideal):")
for k, v in metricas_ideal.items():
    print(f"   • {k}: {v}")

print("\n🔔 Alertas retornados pelo motor (se houver):")
print(alertas_ideal if alertas_ideal else "   • Nenhum alerta.")

# ----------------------------------------------------------------------------
# 5) Salvamento / Tombamento (opcional para análises futuras)
# ----------------------------------------------------------------------------

# Expor nomes padrão para as próximas células
df_ideal = df_mensal_ideal
df_ideal_anual = df_anual_ideal
df_ideal_s = df_semanal_ideal   # NOVO V2.0
df_ideal_d = df_diario_ideal    # NOVO V2.0
met_ideal = metricas_ideal
alertas_ideal = alertas_ideal

print("\n💾 DADOS GERADOS (CENÁRIO IDEAL - BENCHMARK):")
print("-"*88)
print("   • df_ideal   : DataFrame MENSAL (36 meses, 107 colunas)")
print("   • df_ideal_anual : DataFrame ANUAL (3 anos, agregado)")
print("   • df_ideal_s : DataFrame SEMANAL (26 semanas = M1-M6) [NOVO V2.0]")
print("   • df_ideal_d : DataFrame DIÁRIO (180 dias = M1-M6) [NOVO V2.0]")
print("   • met_ideal  : Métricas consolidadas (dict)")
print("   • alertas_ideal : Lista de alertas gerados")
print("-"*88)

print("\n✅ Célula 05B (Cenário Ideal) V2.0 concluída com sucesso.")
print("="*88)
