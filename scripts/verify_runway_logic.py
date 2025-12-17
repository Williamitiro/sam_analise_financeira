
import sys
import os
import pandas as pd
import numpy as np

# Setup paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'notebooks', 'ypynb')))

try:
    from celulas import celula_2_premissas as p2
    from celulas import celula_4_motor as motor
except ImportError:
    # Fallback if running from different cwd
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'notebooks', 'ypynb', 'celulas')))
    import celula_2_premissas as p2
    import celula_4_motor as motor

def verify_runway():
    print("--- FORENSIC VERIFICATION: RUNWAY LOGIC ---")
    
    # 1. Generate Data (Source of Truth)
    print("1. Running Motor Financeiro (V13)...")
    premissas = p2.PREMISSAS
    df_real_m, df_real_s, metricas, debug_info = motor.executar_motor_fintech_v10_production_ready(premissas)
    
    # 2. Extract Vectors
    caixa = df_real_m['caixa'].values
    receita = df_real_m['receita_liquida'].values
    custos = df_real_m['total_custos'].values if 'total_custos' in df_real_m.columns else (df_real_m['total_cogs'] + df_real_m['total_opex']).values
    burn = custos - receita
    burn = np.maximum(burn, 0) # Burn cannot be negative for runway calc usually
    
    # 3. Calculate Method A: Zero Revenue (Caixa / Custos)
    runway_zero_rev = np.zeros(len(caixa))
    for i in range(len(caixa)):
        if custos[i] > 0:
            runway_zero_rev[i] = caixa[i] / custos[i]
        else:
            runway_zero_rev[i] = 36
            
    min_a = runway_zero_rev.min()
    idx_a = np.argmin(runway_zero_rev) + 1
    
    # 4. Calculate Method B: Standard Burn (Caixa / Burn)
    runway_burn = np.zeros(len(caixa))
    for i in range(len(caixa)):
        if burn[i] > 0:
            runway_burn[i] = caixa[i] / burn[i]
        else:
            runway_burn[i] = 36 # Infinite if profitable
            
    min_b = runway_burn.min()
    idx_b = np.argmin(runway_burn) + 1
    
    # 5. Report
    print(f"\n[DATA DUMP M1]: Caixa={caixa[0]:.2f}, Custos={custos[0]:.2f}, Burn={burn[0]:.2f}")
    
    print("\n[METHOD A: Zero Revenue (Caixa / Custos)]")
    print(f"Min Runway: {min_a:.2f} months")
    print(f"Critical Month: M{idx_a}")
    print(f"Calculation M1: {caixa[0]} / {custos[0]} = {caixa[0]/custos[0]:.2f}")
    
    print("\n[METHOD B: Standard Burn (Caixa / Burn)]")
    print(f"Min Runway: {min_b:.2f} months")
    print(f"Critical Month: M{idx_b}")
    print(f"Calculation M1: {caixa[0]} / {burn[0] if burn[0]>0 else 1} = {caixa[0]/burn[0] if burn[0]>0 else 'inf'}")

    print("\n[COMPARISON WITH REPORT TEXT]")
    print("Report says: '1.2 meses no mês M1'")
    if abs(min_a - 1.2) < 0.1:
        print("MATCH: Report uses Method A (Zero Revenue).")
    elif abs(min_b - 1.2) < 0.1:
        print("MATCH: Report uses Method B (Standard Burn).")
    else:
        print("MISMATCH: Report value matches neither method perfectly. Check premissas or rounding.")

if __name__ == "__main__":
    verify_runway()
