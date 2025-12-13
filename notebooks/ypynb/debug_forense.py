
import sys
import os
import pandas as pd
sys.path.append(os.path.join(os.getcwd(), 'notebooks', 'ypynb', 'celulas'))

from celula_4_motor import executar_motor_fintech_v10_production_ready
from celula_2_premissas import PREMISSAS
from celula_0_utils import formata_moeda, formata_pct

print("🔍 INVESTIGAÇÃO FORENSE - MKT & OPEX")
print("-" * 50)

# 1. Executar Motor
df_mensal, _, _, _ = executar_motor_fintech_v10_production_ready(PREMISSAS, modo_debug=False)

# 2. Investigar Marketing (M1 a M6)
print("\n🟢 RASTREAMENTO DE MARKETING (M1-M12)")
cols_mkt = ['mes', 'receita_bruta', 'marketing_perc_receita', 'gasto_marketing', 'caixa', 'runway_meses']

for idx, row in df_mensal.head(12).iterrows():
    m = int(row['mes']) + 1
    rec = row['receita_bruta']
    mkt = row['gasto_marketing']
    caixa = row['caixa']
    
    print(f"M{m:02d} | Receita: {formata_moeda(rec):>12} | Mkt Real: {formata_moeda(mkt):>12} | Caixa: {formata_moeda(caixa):>12}")

# 3. Investigar OPEX (M1 a M12)
print("\n🔴 RASTREAMENTO DE OPEX (M1-M12)")

for idx, row in df_mensal.head(12).iterrows():
    m = int(row['mes']) + 1
    users = int(row['usuarios_ativos'])
    opex = row['total_opex']
    pessoal = row['custo_pessoal']
    headcount = int(row['headcount_total'])
    
    print(f"M{m:02d} | Users: {users:>4} | OPEX: {formata_moeda(opex):>12} | Pessoal: {formata_moeda(pessoal):>12} (HC={headcount})")

# 4. Investigar Formatação
print("\n🔵 TESTE DE FORMATAÇÃO")
val = 60360.00
print(f"Valor Original: {val}")
print(f"Formatado (formata_moeda): '{formata_moeda(val)}'")

# 5. Premissa Check
print("\n🟡 CHECK DE PREMISSAS")
print(f"Marketing % Receita: {PREMISSAS['marketing_perc_receita']} (Esperado: 0.40 -> 40%)")
print(f"Trigger Dev Senior: {PREMISSAS['trigger_dev']} usuarios")
print(f"Salario Dev Senior: {formata_moeda(PREMISSAS['salario_dev_senior'])}")
