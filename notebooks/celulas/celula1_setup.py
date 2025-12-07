# CELULA 01
# ============================================================================
# SETUP & IMPORTS 
# ============================================================================

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configuração de exibição do Pandas
pd.options.display.float_format = '{:,.2f}'.format

def formatar_moeda(valor):
    if isinstance(valor, (int, float)):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return valor

def formatar_pct(valor):
    return f"{valor:.1f}%"

print("✅ Ambiente configurado")
print("📦 Bibliotecas: pandas, numpy, plotly, scipy")
print("🎨 Cores: Movidas para PREMISSAS (Célula 02)")