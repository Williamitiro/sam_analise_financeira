# ============================================================================
# HELPER NOTEBOOK - CARREGA TODOS OS DADOS PARA USO INTERATIVO (V1.0)
# ============================================================================
# OBJETIVO: Carregar todos os dados e variáveis para uso interativo no notebook.
# USO: No notebook, rode: %run helper_notebook.py
# ============================================================================

import os
import sys
import warnings

# Adiciona diretório 'celulas' ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
celulas_dir = os.path.join(current_dir, 'celulas')
if celulas_dir not in sys.path:
    sys.path.append(celulas_dir)

warnings.filterwarnings('ignore')

print("="*80)
print("🚀 HELPER NOTEBOOK - CARREGANDO DADOS")
print("="*80)

# 1. PREMISSAS
print("\n📦 1. Carregando PREMISSAS...")
from celula_2_premissas import PREMISSAS
print(f"   ✅ {len(PREMISSAS)} parâmetros carregados")

# 2. CONFIGURAÇÃO MONTE CARLO
print("\n🎲 2. Carregando Config Monte Carlo...")
_config_mc_path = os.path.join(celulas_dir, 'celula_2B_config_MC.py')
if os.path.exists(_config_mc_path):
    exec(open(_config_mc_path, encoding='utf-8').read())
    print("   ✅ Configuração Monte Carlo adicionada às PREMISSAS")
else:
    print("   ⚠️ Config Monte Carlo não encontrada")

# 3. CENÁRIO REAL
print("\n⚙️ 3. Executando Cenário Real (5A)...")
from celula_5A_bootstrap_real import executar_analise_real
df_real_m, df_real_a, df_real_s, df_real_d, met_real, alertas_real = executar_analise_real(PREMISSAS)
print(f"   ✅ df_real_m: {len(df_real_m)} meses")

# 4. CENÁRIO IDEAL
print("\n⚙️ 4. Executando Cenário Ideal (5B)...")
from celula_5B_cenario_ideal import executar_analise_ideal
df_ideal_m, df_ideal_a, df_ideal_s, df_ideal_d, met_ideal, alertas_ideal = executar_analise_ideal(PREMISSAS)
print(f"   ✅ df_ideal_m: {len(df_ideal_m)} meses")

# 5. MONTE CARLO
print("\n🎲 5. Executando Monte Carlo (5D)...")
from celula_5D_monte_carlo import executar_monte_carlo
try:
    output_data, mc_results = executar_monte_carlo(PREMISSAS)
    print(f"   ✅ mc_results: {len(mc_results)} simulações")
except Exception as e:
    print(f"   ⚠️ Monte Carlo falhou: {e}")
    mc_results = None
    output_data = None

# 6. IMPORTS DAS PÁGINAS
print("\n📄 6. Importando módulos de páginas...")
try:
    from PAGINA_1_COCKPIT_V4 import executar_pagina_1
    from PAGINA_2_GROWTH import executar_pagina_2_growth_machine
    from PAGINA_3_FINANCEIRO import executar_pagina_3_financeiro
    from PAGINA_4_UNIT_ECONOMICS import executar_pagina_4_unit_economics
    from PAGINA_5_RISCO import executar_pagina_5_risco
    print("   ✅ Todas as páginas importadas")
except ImportError as e:
    print(f"   ⚠️ Erro ao importar páginas: {e}")

print("\n" + "="*80)
print("✅ HELPER CARREGADO! Variáveis disponíveis:")
print("="*80)
print("""
📊 DADOS:
   • PREMISSAS      - Dicionário com todos os parâmetros (171 itens)
   • df_real_m      - DataFrame Real Mensal (36 meses)
   • df_ideal_m     - DataFrame Ideal Mensal (36 meses)
   • df_real_s      - DataFrame Real Semanal
   • df_ideal_s     - DataFrame Ideal Semanal
   • mc_results     - DataFrame Monte Carlo (simulações)

📄 PÁGINAS (rode com report_mode=False para notebook):
   • executar_pagina_1(df_real_m, df_ideal_m, met_real, met_ideal, report_mode=False)
   • executar_pagina_2_growth_machine(df_real_m, df_real_s, df_ideal_m, df_ideal_s, PREMISSAS, report_mode=False)
   • executar_pagina_3_financeiro(df_real_m, df_real_s, df_ideal_m, PREMISSAS, report_mode=False)
   • executar_pagina_4_unit_economics(df_real_m, df_real_s, df_ideal_m, PREMISSAS, report_mode=False)
   • executar_pagina_5_risco(df_real_m, df_ideal_m, mc_results, PREMISSAS, report_mode=False)
""")
print("="*80)
