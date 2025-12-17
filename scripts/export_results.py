
import os
import sys
import pandas as pd
from datetime import datetime

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTEBOOKS_DIR = os.path.join(BASE_DIR, 'notebooks', 'ypynb', 'celulas')
OUTPUTS_DIR = os.path.join(BASE_DIR, 'notebooks', 'outputs', 'csv_export')

sys.path.append(NOTEBOOKS_DIR)

# Ensure output dir exists
os.makedirs(OUTPUTS_DIR, exist_ok=True)

print("="*80)
print("📥 EXPORTADOR DE RESULTADOS COMPLETO (CSV)")
print("="*80)

try:
    from celula_2_premissas import PREMISSAS
    from celula_5A_bootstrap_real import executar_analise_real
    from celula_5B_cenario_ideal import executar_analise_ideal
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    sys.exit(1)

# 1. Executar Cenário Real
print("\n🔹 Gerando Dados: Cenário Real (Conservador)...")
df_real_m, df_real_a, df_real_s, df_real_d, _, _ = executar_analise_real(PREMISSAS)

# 2. Executar Cenário Ideal
print("\n🔹 Gerando Dados: Cenário Ideal (Benchmark)...")
df_ideal_m, df_ideal_a, df_ideal_s, df_ideal_d, _, _ = executar_analise_ideal(PREMISSAS)

# 3. Exportar
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

files_to_save = {
    'real_mensal': df_real_m,
    'real_anual': df_real_a,
    'real_semanal': df_real_s,
    'real_diario': df_real_d,
    'ideal_mensal': df_ideal_m,
    'ideal_anual': df_ideal_a,
    'ideal_semanal': df_ideal_s
}

print("\n💾 Salvando arquivos em:", OUTPUTS_DIR)

for name, df in files_to_save.items():
    if df is not None and not df.empty:
        filename = f"{name}_{timestamp}.csv"
        path = os.path.join(OUTPUTS_DIR, filename)
        df.to_csv(path, index=False, sep=';', decimal=',') # Format excel-friendly for BR
        print(f"   ✅ {filename} ({len(df)} linhas)")
    else:
        print(f"   ⚠️ {name}: Sem dados ou vazio")

print("\n🏁 Exportação concluída com sucesso!")
print("="*80)
