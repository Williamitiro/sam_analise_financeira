# CÉLULA 05B — CENÁRIO IDEAL V9.4 (HERDA DO REAL)
# ============================================================================
# OBJETIVO: Simular cenário "execution perfect" herdadando e otimizando premissas
# ============================================================================

import copy
import time
import pandas as pd

try:
    from celula_4_motor import executar_motor_fintech_v10_production_ready
    from celula_4A_motor_granularidade import expandir_granularidade_completa
    from celula_2_premissas import PREMISSAS as premissas_real
except ImportError:
    pass

def obter_premissas_ideal(premissas_real):
    """Gera cenário Ideal com multiplicadores de otimismo"""
    ideal = copy.deepcopy(premissas_real)
    ideal['meta_version'] = '9.4-ideal-execution-perfect'
    ideal['meta_updated_at'] = '2025-12-15'
    
    # Multiplicadores de otimismo (15-30%)
    fatores = {
        'taxa_visitante_para_trial': 1.20,
        'taxa_trial_para_pagante': 1.20,
        'fator_visitas_organicas_por_pagante': 1.30,
        'marketing_fixo_mensal': 1.50,
        'marketing_perc_receita': 1.20,
        'churn_inicial': 0.90,
        'churn_maturidade': 0.80,
        'preco_lite': 1.10,
        'preco_trader': 1.10,
        'preco_pro': 1.10,
        'caixa_inicial': 2.0,  # Multiplicador
        'aporte_mensal': 1.5,
    }
    
    for k, mult in fatores.items():
        if k.startswith('preco_'):
            ideal[k] = round(ideal[k] * mult, 2)
        elif isinstance(ideal[k], (int, float)):
            ideal[k] *= mult
    
    # Remove campos deprecated
    ideal.pop('crescimento_trafego_mes_1_6', None)
    ideal.pop('crescimento_trafego_mes_7_12', None)
    ideal.pop('crescimento_trafego_mes_13_plus', None)
    
    return ideal

def executar_analise_ideal(premissas_real_arg=None):
    """Executa cenário Ideal V9.4"""
    print("\n" + "="*80)
    print("🚀 INICIANDO CENÁRIO IDEAL (V9.4 - EXECUTION PERFECT)")
    print("="*80)
    
    start_time = time.time()
    
    # 1. Gera premissas (herda do Real)
    # Se recebeu argumento (do loader), usa. Senão, usa o importado.
    base_real = premissas_real_arg if premissas_real_arg is not None else premissas_real
    premissas_ideal = obter_premissas_ideal(base_real)
    
    # 2. Executa motor
    df_ideal_m, df_ideal_a, met_ideal, alertas_ideal = executar_motor_fintech_v10_production_ready(
        premissas_ideal, seed=42, modo_debug=False
    )
    
    # 3. Granularidade
    df_ideal_s, df_ideal_d = expandir_granularidade_completa(
        df_ideal_m, premissas_ideal, meses_expandir=6, seed=42
    )
    
    print(f"\n✅ IDEAL CONCLUÍDO em {time.time() - start_time:.2f}s")
    return df_ideal_m, df_ideal_a, df_ideal_s, df_ideal_d, met_ideal, alertas_ideal

if __name__ == "__main__":
    executar_analise_ideal()