# Script de teste rápido para validar a Página 4 (Risco)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from notebooks.modelo4_v7 import executar_pagina_4_risco

# 1. MOCK DATA (Monte Carlo)
print("🧪 Criando dados mock para Página 4...")
n_sims = 200
n_meses = 36

# Gerar séries temporais simuladas
caixa_series = []
caixa_final = []
roi = []
quebrou = []

for _ in range(n_sims):
    # Random walk
    start = 5000
    steps = np.random.normal(100, 500, n_meses)
    path = start + np.cumsum(steps)
    
    # Verificar quebra
    quebra = any(path < 0)
    
    caixa_series.append(path.tolist())
    caixa_final.append(path[-1])
    roi.append((path[-1] - start)/start * 100)
    quebrou.append(quebra)

df_mc = pd.DataFrame({
    'sim': range(n_sims),
    'caixa_series': caixa_series, # Lista de listas
    'caixa_final': caixa_final,
    'roi_total_pct': roi,
    'quebrou': quebrou,
    'cac_medio': np.random.normal(200, 50, n_sims),
    'churn_medio': np.random.normal(0.05, 0.02, n_sims),
    'ltv_medio': np.random.normal(800, 100, n_sims),
    'margem_bruta_media': np.random.normal(80, 5, n_sims)
})

# DF Base (Determinístico)
df_real_m = pd.DataFrame({
    'mes': range(1, n_meses+1),
    'caixa': np.linspace(5000, 15000, n_meses) # Caminho suave
})

premissas = {}

# 2. EXECUTAR TESTE (Modo Notebook)
print("\n" + "="*50)
print("🧪 [TESTE 1] MODO NOTEBOOK INTERATIVO:")
executar_pagina_4_risco(df_mc, df_real_m, premissas, report_mode=False)

# 3. EXECUTAR TESTE (Modo PDF)
print("\n" + "="*50)
print("🧪 [TESTE 2] MODO RELATÓRIO PDF:")
executar_pagina_4_risco(df_mc, df_real_m, premissas, report_mode=True)

print("\n✅ SUCESSO! Se você viu os gráficos de leque e histograma, a Página 4 está funcional.")
