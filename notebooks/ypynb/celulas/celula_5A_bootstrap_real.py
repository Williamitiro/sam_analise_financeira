# CÉLULA 05A - EXECUÇÃO DO CENÁRIO REAL (BOOTSTRAP R$ 2k) V2.0
# ============================================================================
# OBJETIVO: Simular a realidade atual com recursos limitados.
# VERSÃO: 2.1 - Modularizada
# ============================================================================

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
    # Fallback para execução interactive onde já podem estar carregados
    pass

def executar_analise_real(premissas, seed=None):
    """
    Executa a simulação do cenário Real (Bootstrap).
    Retorna tupla: (df_real_m, df_real_a, df_real_s, df_real_d, met_real, alertas_real)
    """
    print("="*80)
    print("🚀 INICIANDO SIMULAÇÃO DO CENÁRIO REAL (BOOTSTRAP)")
    print("="*80)
    print(f"📅 Período: {premissas['meses_projecao']} meses ({premissas['meses_projecao']//12} anos)")
    print(f"💰 Budget Marketing: R$ {premissas['marketing_fixo_mensal']:,.2f}/mês")
    print(f"👥 Base Inicial: {premissas['usuarios_pagos_iniciais']} usuários pagantes")
    print("-" * 80)

    start_time = time.time()

    # 1. MOTOR MENSAL
    df_real_m, df_real_a, met_real, alertas_real = executar_motor_fintech_v10_production_ready(
        premissas,
        seed=seed, 
        variacao_params=None,
        modo_debug=False
    )

    # 2. GRANULARIDADE
    print("\n📐 Gerando granularidades semanal e diária...")
    try:
        df_real_s, df_real_d = expandir_granularidade_completa(
            df_real_m, 
            premissas, 
            meses_expandir=12,
            seed=premissas.get('seed_fixa', 42)
        )
        print(f"   ✅ df_real_s: {len(df_real_s)} semanas geradas")
        print(f"   ✅ df_real_d: {len(df_real_d)} dias gerados")
    except Exception as e:
        print(f"   ⚠️ Impossível gerar granularidade: {e}")
        df_real_s = pd.DataFrame()
        df_real_d = pd.DataFrame()
    
    tempo_exec = time.time() - start_time
    
    print("\n" + "="*80)
    print(f"✅ SIMULAÇÃO REAL CONCLUÍDA em {tempo_exec:.2f}s")
    print("="*80)
    
    return df_real_m, df_real_a, df_real_s, df_real_d, met_real, alertas_real

if __name__ == "__main__":
    # Teste isolado
    if 'PREMISSAS' in globals():
        p = PREMISSAS
    else:
        # Tenta importar se não estiver no namespace
        try:
            from celula_2_premissas import PREMISSAS as p
        except:
            p = {} # Should fail or mock
            
    executar_analise_real(p)