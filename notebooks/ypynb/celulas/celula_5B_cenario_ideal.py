# CÉLULA 05B — CENÁRIO IDEAL (BENCHMARK-DRIVEN) V2.0
# ============================================================================
# OBJETIVO: Simular cenário otimista com premissas de benchmark.
# VERSÃO: 2.1 - Modularizada
# ============================================================================

import copy
import traceback
import time
import pandas as pd
import sys
import os

# Adiciona diretório atual para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from celula_4_motor import executar_motor_fintech_v10_production_ready
    from celula_4A_motor_granularidade import expandir_granularidade_completa
    from celula_2_premissas import PREMISSAS
except ImportError:
    pass

def executar_analise_ideal(premissas):
    """
    Executa a simulação do cenário Ideal.
    Retorna tupla: (df_mensal_ideal, df_anual_ideal, df_semanal_ideal, df_diario_ideal, metricas_ideal, alertas_ideal)
    """
    print("\n" + "="*88)
    print("🚀 INICIANDO CENÁRIO 05B — IDEAL (BENCHMARK-DRIVEN) — VERSÃO CORRIGIDA")
    print("="*88)
    
    start_time = time.time()
    
    # ----------------------------------------------------------------------------
    # 1) Preparar variacao_params
    # ----------------------------------------------------------------------------
    variacao_params = {}
    
    # Crescimento
    if 'growth_m1_6_otimista' in premissas:
        variacao_params['crescimento_trafego_mes_1_6'] = premissas['growth_m1_6_otimista']
    if 'growth_m7_12_otimista' in premissas:
        variacao_params['crescimento_trafego_mes_7_12'] = premissas['growth_m7_12_otimista']
    if 'growth_m13_36_otimista' in premissas:
        variacao_params['crescimento_trafego_mes_13_plus'] = premissas['growth_m13_36_otimista']
    
    # Funil e retenção
    if 'benchmark_trial_excelente' in premissas:
        variacao_params['taxa_trial_para_pagante'] = premissas['benchmark_trial_excelente']
    if 'benchmark_churn_bom' in premissas:
        variacao_params['churn_maturidade'] = premissas['benchmark_churn_bom']
    
    # Marketing Ideal
    variacao_params['marketing_fixo_mensal'] = 10000.0
    
    # Viralidade
    variacao_params['fator_visitas_organicas_por_pagante'] = premissas.get('fator_visitas_organicas_por_pagante', 5.0)
    
    # Triggers
    if 'trigger_dev' in premissas:
        variacao_params['trigger_dev'] = max(1, int(premissas.get('trigger_dev') * 0.6))
    else:
        variacao_params['trigger_dev'] = 500
        
    if 'trigger_cs' in premissas:
        variacao_params['trigger_cs'] = max(1, int(premissas.get('trigger_cs') * 0.8))
    else:
        variacao_params['trigger_cs'] = 800
        
    if 'trigger_fundador' in premissas:
        variacao_params['trigger_fundador'] = int(premissas.get('trigger_fundador') * 0.8)
    else:
        variacao_params['trigger_fundador'] = 10000
        
    # Afiliados
    if 'pct_usuarios_via_afiliado' in premissas:
        variacao_params['pct_usuarios_via_afiliado'] = premissas['pct_usuarios_via_afiliado']
    if 'modelo_afiliado' in premissas:
        variacao_params['modelo_afiliado_habilitado'] = True
        variacao_params['comissao_afiliado_tipo'] = premissas.get('modelo_afiliado', 'primeira_mensalidade')
    
    # Taxas Pagamento
    if 'taxa_pagamento' in premissas:
         if 'taxa_processamento_cartao' in premissas:
            variacao_params['taxa_processamento_cartao'] = premissas['taxa_processamento_cartao']
         else:
            variacao_params['taxa_processamento_cartao'] = premissas.get('taxa_pagamento', 0.035)

    # Limpeza
    for k, v in list(variacao_params.items()):
        if v is None:
            variacao_params.pop(k)
            
    print("\n🔧 Variáveis de cenário (variacao_params) preparadas.")

    # ----------------------------------------------------------------------------
    # 2) Executar Motor
    # ----------------------------------------------------------------------------
    try:
        print("\n⏱️ Rodando o motor financeiro com overrides do cenário ideal...")
        df_mensal_ideal, df_anual_ideal, metricas_ideal, alertas_ideal = executar_motor_fintech_v10_production_ready(
            premissas,
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
    # 3) Expansão de Granularidade
    # ----------------------------------------------------------------------------
    print("\n📐 Gerando granularidades semanal e diária para cenário IDEAL...")
    try:
        df_semanal_ideal, df_diario_ideal = expandir_granularidade_completa(
            df_mensal_ideal, 
            premissas, 
            meses_expandir=6,
            seed=premissas.get('seed_fixa', 42) + 500
        )
        print(f"   ✅ df_ideal_s: {len(df_semanal_ideal)} semanas geradas")
        print(f"   ✅ df_ideal_d: {len(df_diario_ideal)} dias gerados")
    except Exception as e:
        print(f"   ⚠️ Impossível gerar granularidade: {e}")
        df_semanal_ideal = pd.DataFrame()
        df_diario_ideal = pd.DataFrame()

    tempo_total = time.time() - start_time
    
    print("\n" + "="*88)
    print(f"✅ CENÁRIO IDEAL CONCLUÍDO em {tempo_total:.2f}s")
    print("="*88)
    
    return df_mensal_ideal, df_anual_ideal, df_semanal_ideal, df_diario_ideal, metricas_ideal, alertas_ideal

if __name__ == "__main__":
    if 'PREMISSAS' in globals():
        p = PREMISSAS
    else:
        try:
            from celula_2_premissas import PREMISSAS as p
        except:
            p = {}
            
    executar_analise_ideal(p)
