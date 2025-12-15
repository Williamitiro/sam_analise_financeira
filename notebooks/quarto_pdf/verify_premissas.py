import sys
import os
import pandas as pd
from IPython.display import display, Markdown

# Setup Paths to mimic QMD environment
# Assuming script is run from notebooks/quarto_pdf/
# Root is ../../
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, 'notebooks/ypynb/'))
sys.path.append(os.path.join(root_dir, 'notebooks/ypynb/celulas/'))

try:
    from celula_2_premissas import PREMISSAS
    from celula_3_config_cenario_ideal import obter_premissas_ideal
    from celula_2B_config_MC import PREMISSAS as MC_CONFIG # Just to ensure MC is loaded if needed
    
    # Ensure Monte Carlo data is in PREMISSAS as QMD expects
    if 'monte_carlo' not in PREMISSAS:
         # Manually load if not present (celula_2B usually patches PREMISSAS global)
         # In standalone script, we might need to update it manually if imports behave differently
         if 'monte_carlo' in MC_CONFIG:
             PREMISSAS['monte_carlo'] = MC_CONFIG['monte_carlo']

    PREMISSAS_IDEAL = obter_premissas_ideal()
    
    print("DEBUG: Libraries loaded successfully.")
    
    # --- LOGIC COPIED FROM QMD ---
    # 2. Helpers de Formatação
    def fmt_pct(val): 
        try:
            return f"{val*100:.1f}%" if isinstance(val, (int, float)) else str(val)
        except: return str(val)

    def fmt_money(val): 
        try:
            return f"R$ {val:,.2f}" if isinstance(val, (int, float)) else str(val)
        except: return str(val)

    def fmt_int(val): 
        try:
            return f"{int(val)}" if isinstance(val, (int, float)) else str(val)
        except: return str(val)

    # 3. Construção das Tabelas

    # --- TABELA 1: GROWTH & AQUISIÇÃO ---
    # Extrair dados Real vs Ideal vs Monte Carlo (Pessimista)
    mc_pessimista = PREMISSAS.get('monte_carlo', {}).get('cenarios', {}).get('pessimista', {}).get('multiplicadores', {})

    data_growth = [
        ["Tráfego Inicial (Visitas)", 
         fmt_int(PREMISSAS.get('trafego_inicial', 0)), 
         fmt_int(PREMISSAS_IDEAL.get('trafego_inicial', '-')), 
         "N/A"],
        
        ["Conv. Visitante -> Trial", 
         fmt_pct(PREMISSAS.get('taxa_visitante_para_trial', 0)), 
         fmt_pct(PREMISSAS_IDEAL.get('taxa_visitante_para_trial', '-')), 
         f"x{mc_pessimista.get('taxa_visitante_para_trial', 1.0):.2f}"],
         
        ["Conv. Trial -> Pago", 
         fmt_pct(PREMISSAS.get('taxa_trial_para_pagante', 0)), 
         fmt_pct(PREMISSAS_IDEAL.get('taxa_trial_para_pagante', '-')), 
         f"x{mc_pessimista.get('taxa_trial_para_pagante', 1.0):.2f}"],
         
        ["Marketing Fixo Mensal", 
         fmt_money(PREMISSAS.get('marketing_fixo_mensal', 0)), 
         fmt_money(PREMISSAS_IDEAL.get('marketing_fixo_mensal', '-')), 
         f"x{mc_pessimista.get('marketing_fixo_mensal', 1.0):.2f}"],
         
        ["Fator Viral (K-Factor)", 
         f"{PREMISSAS.get('fator_visitas_organicas_por_pagante', 0)}x", 
         f"{PREMISSAS_IDEAL.get('fator_visitas_organicas_por_pagante', '-')}", 
         "N/A"]
    ]

    df_growth = pd.DataFrame(data_growth, columns=["Parâmetro", "Real (Conservador)", "Ideal (Benchmark)", "Estresse (Fator)"])

    # --- TABELA 2: RETENÇÃO & ECONOMICS ---
    data_retention = [
        ["Churn Inicial", 
         fmt_pct(PREMISSAS.get('churn_inicial', 0)), 
         fmt_pct(PREMISSAS_IDEAL.get('churn_inicial', '-')), 
         f"x{mc_pessimista.get('churn_inicial', 1.0):.2f}"],
         
        ["Churn Maturidade (M36)", 
         fmt_pct(PREMISSAS.get('churn_maturidade', 0)), 
         fmt_pct(PREMISSAS_IDEAL.get('churn_maturidade', '-')), 
         "-"],
         
        ["Preço 'Trader' (Plano Médio)", 
         fmt_money(PREMISSAS.get('preco_trader', 0)), 
         fmt_money(PREMISSAS_IDEAL.get('preco_trader', '-')), 
         "-"],
         
        ["Taxa Inadimplência (Cartão)", 
         fmt_pct(PREMISSAS.get('taxa_inadimplencia_cartao', 0)), 
         fmt_pct(PREMISSAS_IDEAL.get('taxa_inadimplencia_cartao', '-')), 
         "-"]
    ]
    df_retention = pd.DataFrame(data_retention, columns=["Parâmetro", "Real (Conservador)", "Ideal (Benchmark)", "Estresse (Fator)"])

    # --- TABELA 3: ESTRUTURA & OPEX ---
    data_struct = [
        ["Caixa Inicial", 
         fmt_money(PREMISSAS.get('caixa_inicial', 0)), 
         fmt_money(PREMISSAS_IDEAL.get('caixa_inicial', '-')), 
         "-"],
        
        ["Aporte Mensal", 
         fmt_money(PREMISSAS.get('aporte_mensal', 0)), 
         fmt_money(PREMISSAS_IDEAL.get('aporte_mensal', '-')), 
         "-"],
        
        ["Salário Fundador", 
         fmt_money(PREMISSAS.get('salario_fundador', 0)), 
         fmt_money(PREMISSAS_IDEAL.get('salario_fundador', '-')), 
         "-"],
        
        ["Gatilho Salário Fundador (MRR)", 
         fmt_money(PREMISSAS.get('trigger_fundador', 0)), 
         fmt_money(PREMISSAS_IDEAL.get('trigger_fundador', '-')), 
         "-"]
    ]
    df_struct = pd.DataFrame(data_struct, columns=["Parâmetro", "Real (Conservador)", "Ideal (Benchmark)", "Estresse (Fator)"])

    print("\n--- TABLE 1: GROWTH ---")
    print(df_growth.to_markdown(index=False))
    print("\n--- TABLE 2: RETENTION ---")
    print(df_retention.to_markdown(index=False))
    print("\n--- TABLE 3: STRUCTURE ---")
    print(df_struct.to_markdown(index=False))

    # --- TABELA 4: MONTE CARLO ---
    if 'monte_carlo' in PREMISSAS:
        mc = PREMISSAS['monte_carlo']
        
        # Top Variáveis Variáveis
        vars_mc = mc.get('variaveis', {})
        data_vars = []
        # Pegar as 5 primeiras chaves se existirem
        for k in list(vars_mc.keys())[:5]: 
            v = vars_mc[k]
            data_vars.append([k, f"±{v.get('std',0)*100:.0f}%", v.get('dist', '-')])
            
        df_vars = pd.DataFrame(data_vars, columns=["Variável Estocástica", "Volatilidade (Std)", "Distribuição"])
        print("\n--- TABLE 4: MONTE CARLO ---")
        print(f"Simulations: {mc.get('n_simulacoes')}")
        print(df_vars.to_markdown(index=False))

except Exception as e:
    import traceback
    traceback.print_exc()
