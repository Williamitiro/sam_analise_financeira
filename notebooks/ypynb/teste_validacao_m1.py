
import sys
import os
import pandas as pd
import numpy as np

# Adicionar caminho para importar módulos
sys.path.append(os.path.join(os.getcwd(), 'celulas'))

# Importar premissas e motor
try:
    from celula_2_premissas import PREMISSAS
    from celula_4_motor import executar_motor_fintech_v10_production_ready
except ImportError:
    # Se estiver rodando da raiz e não conseguir, tentar ajustar path
    sys.path.append('notebooks/ypynb/celulas')
    from celula_2_premissas import PREMISSAS
    from celula_4_motor import executar_motor_fintech_v10_production_ready

def analisar_simulacao(users_iniciais, label):
    print(f"\n{'='*60}")
    print(f"🧪 SIMULAÇÃO: {label} (Início: {users_iniciais} usuários)")
    print(f"{'='*60}")
    
    # Configurar
    p = PREMISSAS.copy()
    p['usuarios_pagos_iniciais'] = users_iniciais
    
    # Rodar Motor
    # Retorno: df_mensal, df_anual, metricas, alertas
    df_mensal, df_anual, metricas, alertas = executar_motor_fintech_v10_production_ready(p, modo_debug=False)
    
    # Extrair dados M1
    m1 = df_mensal.iloc[0]
    
    # Extrair dados M1
    usuarios_m1 = m1['usuarios_ativos']
    novos_m1 = m1['novos_pagantes_total']
    churn_users_m1 = m1['churn_usuarios']
    
    mrr_m1 = m1['mrr']
    caixa_m1 = m1['caixa']
    burn_m1 = m1['burn_rate']
    runway_m1 = m1['runway_meses']
    
    # Detalhes do Runway
    despesas_op = m1['total_cogs'] + m1['total_opex'] + abs(min(0, m1['fluxo_investimento']))
    caixa_proj = caixa_m1 + p['aporte_mensal'] # Lógica do código para M0
    runway_calc = caixa_proj / despesas_op if despesas_op > 0 else 999
    
    print(f"📊 RESULTADOS M1:")
    print(f"   • Usuários Ativos: {usuarios_m1:.1f}")
    print(f"     (Start {users_iniciais} + Novos {novos_m1:.2f} - Churn {churn_users_m1:.2f})")
    print(f"   • MRR: R$ {mrr_m1:,.2f}")
    print(f"   • Caixa Final: R$ {caixa_m1:,.2f}")
    print(f"   • Burn Rate (Tabela): R$ {burn_m1:,.2f}")
    print(f"   • Runway (Tabela): {runway_m1:.2f} meses")
    print("-" * 30)
    print(f"🕵️ INVESTIGAÇÃO RUNWAY:")
    print(f"   • Despesas Operacionais (Brutas): R$ {despesas_op:,.2f}")
    print(f"   • Aporte Mensal (Premissa): R$ {p['aporte_mensal']:,.2f}")
    print(f"   • Caixa Projetado (Caixa + Aporte): R$ {caixa_proj:,.2f}")
    print(f"   • Cálculo: {caixa_proj:.2f} / {despesas_op:.2f} = {runway_calc:.2f}")

# 1. Rodar com configuração atual (6 usuários)
analisar_simulacao(6, "CÓDIGO ATUAL")

# 2. Rodar com hipótese do relatório (10 usuários)
analisar_simulacao(10, "HIPÓTESE RELATÓRIO")
