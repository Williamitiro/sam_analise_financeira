# CÉLULA 06 — OTIMIZADOR FINANCEIRO V1.0 (GOAL SEEKING)
# ============================================================================
# OBJETIVO: Encontrar parâmetros "ótimos" (Caixa Inicial, Marketing) para metas
# (Sobrevivência, Valuation Máximo) dado um orçamento limitado.
# ============================================================================

import copy
import time
import pandas as pd
import numpy as np
from itertools import product

try:
    from celula_4_motor import executar_motor_fintech_v10_production_ready
    from celula_2_premissas import PREMISSAS
except ImportError:
    pass

def otimizar_caixa_sobrevivencia(premissas_base, margem_seguranca=1000):
    """
    MODO 1: SOBREVIVÊNCIA
    Pergunta: 'Qual o MÍNIMO de caixa inicial para não quebrar (saldo > 0 sempre)?'
    Método: Busca Binária
    """
    print("\n" + "="*80)
    print("🤖 MODO 1: BUSCANDO PONTO DE EQUILÍBRIO (BREAKEVEN DE CAIXA)") 
    print("="*80)
    
    # Intervalo de busca (R$ 0 a R$ 200k)
    low = 0
    high = 200000
    best_caixa = high
    iterations = 0
    
    p_sim = copy.deepcopy(premissas_base)
    
    # Desativa debug do motor
    modo_debug_motor = False
    
    while low <= high and iterations < 20:
        mid = (low + high) // 2
        p_sim['caixa_inicial'] = mid
        
        # Roda motor
        df_m, _, metricas, _ = executar_motor_fintech_v10_production_ready(p_sim, modo_debug=modo_debug_motor)
        
        # Verifica se quebrou
        # Quebra = Saldo final < 0 OU algum mês negativo? 
        # Risco zero = NENHUM mês negativo.
        saldo_minimo = df_m['caixa'].min() if len(df_m) > 0 else -1
        
        if saldo_minimo >= margem_seguranca:
            # Sobreviveu com folga: Tenta diminuir caixa
            best_caixa = mid
            high = mid - 100 # step
            status = "🟢 OK"
        else:
            # Quebrou: Precisa de mais caixa
            low = mid + 100
            status = "🔴 Quebra"
            
        print(f"   Iter {iterations+1}: Testando R$ {mid:,.0f} -> Mínimo: R$ {saldo_minimo:,.0f} ({status})")
        iterations += 1
        
    print("-" * 50)
    print(f"🎯 RESULTADO: Caixa Mínimo Necessário = R$ {best_caixa:,.2f}")
    if best_caixa > 150000:
        print("⚠️ ALERTA: O modelo exige muito capital. Revise custos fixos ou aumente eficiência.")
        
    return best_caixa

def otimizar_budget_marketing(premissas_base, teto_gasto_total_3anos=50000):
    """
    MODO 2: MAXIMIZAR VALUATION (LTV TOTAL) NO TETO DE GASTOS
    Pergunta: 'Como dividir meu dinheiro entre Caixa Inicial e Mkt para crescer o máximo possível?'
    Constraint: Caixa Inicial + (Aporte Mensal * Meses) <= Teto
    Ou: Soma de Cash Burn <= Teto (Mais complexo, vamos simplificar pelo investimento)
    """
    print("\n" + "="*80)
    print(f"🤖 MODO 2: ALOCAÇÃO ÓTIMA (TETO DE INVESTIMENTO: R$ {teto_gasto_total_3anos:,.0f})")
    print("="*80)
    
    # Grid Search Simplificado
    # Variável 1: Mix de Investimento (Low vs High Risk)
    # Variável 2: Agressividade no Growth (Tiers)
    
    resultados = []
    
    # Definir cenários de caixa inicial (segurança) vs mkt (agressividade)
    # Se tenho 50k:
    # Cenário A (Conservador): 20k no caixa, 30k no mkt ao longo do tempo
    # Cenário B (Agressivo): 5k no caixa, 45k no mkt (risco de quebra alto)
    
    steps_caixa = [5000, 10000, 15000, 20000, 30000]
    steps_mkt_fixo = [1000, 2000, 3000, 4000, 5000]
    
    best_valuation = 0
    best_config = None
    
    count = 0
    total_combs = len(steps_caixa) * len(steps_mkt_fixo)
    
    for cx in steps_caixa:
        for mkt in steps_mkt_fixo:
            # Estima custo total simplificado (Caixa + 12 meses de mkt fixo "garantido")
            # Isso é uma heurística pro usuário não setar algo impossível
            investimento_estimado = cx + (mkt * 12)
            
            if investimento_estimado > teto_gasto_total_3anos * 1.2: # Aceita estouro de 20%
                continue
                
            p_sim = copy.deepcopy(premissas_base)
            p_sim['caixa_inicial'] = cx
            p_sim['marketing_fixo_mensal'] = mkt
            
            # Roda
            try:
                df_m, _, metricas, _ = executar_motor_fintech_v10_production_ready(p_sim, modo_debug=False)
                
                # Check de Quebra
                quebrou = df_m['caixa'].min() < 0
                
                # Score: Valuation (ARR x 6) se não quebrar. Se quebrar, Score = 0.
                if quebrou:
                    score = 0
                    status = "💀 Quebrou"
                else:
                    arr_final = df_m['arr'].iloc[-1]
                    score = arr_final * 6 # Valuation Proxy
                    status = f"💎 Val: {score/1000:.0f}k"
                
                resultados.append({
                    'caixa': cx,
                    'mkt': mkt,
                    'score': score,
                    'quebrou': quebrou
                })
                
                if score > best_valuation:
                    best_valuation = score
                    best_config = {'caixa': cx, 'mkt': mkt, 'arr': arr_final}
                    
                print(f"   Comb {count+1}/{total_combs}: Cx={cx/1000:.0f}k Mkt={mkt} -> {status}")
                
            except:
                pass
            count += 1
            
    if best_config:
        print("-" * 50)
        print(f"🏆 MELHOR CONFIGURAÇÃO ENCONTRADA:")
        print(f"   • Caixa Inicial Sugerido: R$ {best_config['caixa']:,.2f}")
        print(f"   • Marketing Mensal Fixo:  R$ {best_config['mkt']:,.2f}")
        print(f"   • Resultado (ARR Final):  R$ {best_config['arr']:,.2f}")
        print(f"   • Valuation Potencial:    R$ {best_valuation:,.2f}")
        
    return best_config

if __name__ == "__main__":
    # Teste rápido se rodar direto
    if 'PREMISSAS' in locals() or 'PREMISSAS' in globals():
        otimizar_caixa_sobrevivencia(PREMISSAS)
    else:
        # Fallback para teste isolado (mock)
        print("Rodando em modo standalone (sem premissas carregadas)...")
