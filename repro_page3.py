
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt

# Mock display to capture output
def mock_display(obj):
    if hasattr(obj, 'data'):
        print(f"\n--- DISPLAY OBJECT START ({type(obj).__name__}) ---")
        print(obj.data)
        print("--- DISPLAY OBJECT END ---\n")
    else:
        print(f"\n--- DISPLAY RAW START ---")
        print(str(obj))
        print("--- DISPLAY RAW END ---\n")

# Mock Markdown/HTML classes
class MockMarkdown:
    def __init__(self, data):
        self.data = data
    def _repr_markdown_(self):
        return self.data

class MockHTML:
    def __init__(self, data):
        self.data = data
    def _repr_html_(self):
        return self.data

# Inject into builtins
import builtins
builtins.display = mock_display
builtins.Markdown = MockMarkdown
builtins.HTML = MockHTML

# Setup path
sys.path.append(os.path.abspath("notebooks/ypynb/celulas"))

# Import module
try:
    from PAGINA_3_FINANCEIRO import gerar_viz_3_2_estrutura_custos
except ImportError:
    sys.path.append("e:/Projetos/sam_analise_financeira/notebooks/ypynb/celulas")
    from PAGINA_3_FINANCEIRO import gerar_viz_3_2_estrutura_custos

# Mock Data (matches user scenario)
data = {
    'receita_bruta': 1000.0,
    'receita_liquida': 900.0, # 90%
    'total_deducoes': 100.0,
    'total_cogs': 200.0,
    'total_opex': 500.0,
    'ebitda': 200.0,
    'margem_bruta': 700.0,
    'margem_bruta_pct': 70.0,
    'ebitda_margin': 20.0,
    
    # Details
    'custo_ia_total': 50.0,
    'custo_ia_lite': 10.0,
    'custo_ia_trader': 20.0,
    'custo_ia_pro': 20.0,
    'comissao_afiliados': 0.0,
    'custo_suporte_variavel': 0.0,
    
    'gasto_marketing': 100.0, # 10%
    'gasto_instagram': 50.0,
    'gasto_facebook': 50.0,
    'gasto_youtube': 0.0,
    'gasto_google': 0.0,
    
    'custo_pessoal': 30570.0, # 3057%
    'custo_infra_fixo': 515.0, # 51.5%
    'custo_escritorio': 0.0,
    'custo_contabilidade': 0.0,
    'despesas_viagens': 0.0,
    'despesas_freelancer': 0.0,
}

df_real = pd.DataFrame([data] * 36)
df_ideal = df_real.copy()
premissas = {}

print("--- STARTING TEST ---")
gerar_viz_3_2_estrutura_custos(df_real, df_ideal, premissas, report_mode=True)
print("--- END TEST ---")
