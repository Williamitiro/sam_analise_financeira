# Script de teste rápido para validar a Página 1 (Resumo Executivo)
# Executa a geração dos gráficos usando dados mockados ou reais
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from notebooks.modelo1_v7 import executar_pagina_1_resumo_executivo

# 1. MOCK DATA (Simulando o output do motor financeiro)
print("🧪 Criando dados mock para Página 1...")
meses = np.arange(1, 37)
receita = np.linspace(1000, 50000, 36) # Crescimento linear
custos = np.linspace(2000, 30000, 36)  # Custos crescem menos (Alavancagem)
ebitda = receita - custos
caixa = 10000 + np.cumsum(ebitda) # Caixa acumulado

df_mock = pd.DataFrame({
    'mes': meses,
    'caixa': caixa,
    'burn_rate': np.where(ebitda < 0, -ebitda, 0),
    'receita_liquida': receita,
    'ebitda': ebitda,
    'receita_lite': receita * 0.2,
    'receita_trader': receita * 0.5,
    'receita_pro': receita * 0.3,
    'total_opex': custos,
    'headcount_total': np.linspace(2, 10, 36)
})

# DataFrame Ideal (Meta +20%)
df_ideal = df_mock.copy()
df_ideal['caixa'] = df_ideal['caixa'] * 1.2

premissas = {}

# 2. EXECUTAR TESTE (Modo Notebook)
print("\n" + "="*50)
print("🧪 [TESTE 1] MODO NOTEBOOK INTERATIVO:")
executar_pagina_1_resumo_executivo(df_mock, df_ideal, premissas, report_mode=False)

# 3. EXECUTAR TESTE (Modo PDF)
print("\n" + "="*50)
print("🧪 [TESTE 2] MODO RELATÓRIO PDF:")
executar_pagina_1_resumo_executivo(df_mock, df_ideal, premissas, report_mode=True)

print("\n✅ SUCESSO! Se você viu os gráficos e mensagens acima, a Página 1 está funcional.")
