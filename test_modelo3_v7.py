# Script de teste rápido para validar a Página 3 (Financeiro Detalhado)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from notebooks.modelo3_v7 import executar_pagina_3_financeiro

# 1. MOCK DATA (Simulando o output do motor financeiro para 36 meses)
print("🧪 Criando dados mock para Página 3...")
meses = np.arange(1, 37)
receita = np.linspace(5000, 50000, 36)
cogs = receita * 0.20
mkt = receita * 0.25
pessoal = receita * 0.30
opex_outros = receita * 0.10
impostos = receita * 0.06

# Ajuste para simular lucro no final
pessoal[-12:] = pessoal[-12:] * 0.8 # Ganho de eficiência

ebitda = receita - cogs - mkt - pessoal - opex_outros
lucro_liq = ebitda - 500 - impostos # Depreciação fixa

df_mock = pd.DataFrame({
    'mes': meses,
    'receita_liquida': receita,
    'total_cogs': cogs,
    'gasto_marketing': mkt,
    'custo_pessoal': pessoal,
    'total_opex': mkt + pessoal + opex_outros,
    'impostos': impostos,
    'margem_bruta_pct': (receita-cogs)/receita*100,
    'ebitda': ebitda,
    'ebitda_margin': (ebitda/receita)*100,
    'margem_liquida': (lucro_liq/receita)*100,
    'arr': receita * 12,
    'headcount_total': np.linspace(2, 10, 36)
})

premissas = {}

# 2. EXECUTAR TESTE (Modo Notebook)
print("\n" + "="*50)
print("🧪 [TESTE 1] MODO NOTEBOOK INTERATIVO:")
executar_pagina_3_financeiro(df_mock, premissas, report_mode=False)

# 3. EXECUTAR TESTE (Modo PDF)
print("\n" + "="*50)
print("🧪 [TESTE 2] MODO RELATÓRIO PDF:")
executar_pagina_3_financeiro(df_mock, premissas, report_mode=True)

print("\n✅ SUCESSO! Se você viu os gráficos e mensagens acima, a Página 3 está funcional.")
