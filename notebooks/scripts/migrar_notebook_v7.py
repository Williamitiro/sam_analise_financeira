import json
import os
import copy

# CAMINHOS
INPUT_NB = "notebooks/real_vs_ideal.ipynb"
OUTPUT_NB = "notebooks/real_vs_ideal_v7_GOLD.ipynb"

# CÓDIGO DE INTEGRAÇÃO (O "Snippet Mágico" - Agora Completo com Pg 4)
CODE_INTEGRATION = """# ==============================================================================
# 🚀 INTEGRAÇÃO FINAL V7.0 (GOLD STANDARD)
# ==============================================================================
# Data: 06/12/2025
# Módulos Carregados: Resumo (Pg1), Growth (Pg2), Financeiro (Pg3), Risco (Pg4)

import sys
import os

# Adicionar raiz ao path se necessário
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

# 1. Importar os Novos Módulos
from notebooks import modelo1_v7, modelo2_v7, modelo3_v7, modelo4_v7
from notebooks.celulas import motor_granularidade

print("✅ Módulos V7 carregados com sucesso.")

# 2. Expandir Granularidade (Mensal -> Semanal/Diário)
print("🔄 Expandindo granularidade dos dados (Motor V7)...")
df_real_s, df_real_d = motor_granularidade.expandir_granularidade_temporal(
    df_mensal=df_real_m, 
    premissas=PREMISSAS, 
    modo='real'
)
df_ideal_s, df_ideal_d = motor_granularidade.expandir_granularidade_temporal(
    df_mensal=df_ideal, 
    premissas=PREMISSAS, 
    modo='ideal'
)

# 3. Executar Relatório Completo (Modo Interativo para Notebook)
# Nota: report_mode=False habilita HTML colorido e gráficos grandes.

# --- PÁGINA 1: RESUMO EXECUTIVO ---
modelo1_v7.executar_pagina_1_resumo_executivo(df_real_m, df_ideal, PREMISSAS, report_mode=False)

# --- PÁGINA 2: GROWTH MACHINE ---
modelo2_v7.executar_pagina_2_growth_machine(df_real_m, df_real_s, df_ideal, df_ideal_s, PREMISSAS, report_mode=False)

# --- PÁGINA 3: FINANCEIRO DETALHADO ---
modelo3_v7.executar_pagina_3_financeiro(df_real_m, PREMISSAS, report_mode=False)

# --- PÁGINA 4: RISCO & CENÁRIOS ---
# Verifica se Monte Carlo rodou (mc_results existe)
if 'mc_results' in globals():
    modelo4_v7.executar_pagina_4_risco(mc_results, df_real_m, PREMISSAS, report_mode=False)
else:
    print("⚠️ 'mc_results' não encontrado. Pulando Página 4 (Risco). Rode a célula de Monte Carlo antes.")
"""

def migrar_notebook():
    print(f"📖 Lendo notebook original: {INPUT_NB}")
    with open(INPUT_NB, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    cells = nb['cells']
    new_cells = []
    
    print(f"📊 Total de células originais: {len(cells)}")
    
    # ESTRATÉGIA: Manter células de setup e motor
    keep_mode = True
    count_kept = 0
    
    for cell in cells:
        source_text = "".join(cell['source']).upper()
        
        # Sinais de parada (Começo da parte visual antiga)
        if "VISUALIZAÇÃO" in source_text or "PLOTLY" in source_text or "DASHBOARD" in source_text or "RESUMO EXECUTIVO" in source_text:
            if count_kept > 5: 
                keep_mode = False
        
        # Sinais de que ainda é motor
        if "PREMISSAS" in source_text or "BOOTSTRAP" in source_text or "MONTE CARLO" in source_text or "MOTOR" in source_text:
            keep_mode = True 
            
        if keep_mode:
            new_cells.append(cell)
            count_kept += 1
            
    print(f"✂️  Células mantidas: {count_kept}")
    
    # Adicionar Célula Markdown de Transição
    md_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# 🛑 FIM DO MOTOR DE CÁLCULO / INÍCIO DO RELATÓRIO V7\n",
            "---\n",
            "**Atenção:** A partir deste ponto, utilizamos a nova arquitetura modular `V7 (Gold Standard)`.\n",
            "As visualizações antigas foram removidas em favor dos módulos `modelo1_v7`, `modelo2_v7`, `modelo3_v7` e `modelo4_v7`.\n",
            "\n",
            "Se precisar gerar PDF, use o arquivo `.qmd` correspondente."
        ]
    }
    new_cells.append(md_cell)
    
    # Adicionar Célula de Código V7
    code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [l + "\n" for l in CODE_INTEGRATION.split("\n")]
    }
    new_cells.append(code_cell)
    
    # Atualizar Notebook
    nb['cells'] = new_cells
    
    print(f"💾 Salvando novo notebook: {OUTPUT_NB}")
    with open(OUTPUT_NB, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        
    print("✅ Migração concluída com sucesso!")

if __name__ == "__main__":
    migrar_notebook()