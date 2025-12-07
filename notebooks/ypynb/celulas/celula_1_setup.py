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
import sys
import os

# Adiciona o diretório atual ao path para permitir imports locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from celula_0_utils import formata_moeda, formata_pct
except ImportError:
    # Fallback se rodar fora do contexto
    def formata_moeda(v): return f"R$ {v}"
    def formata_pct(v): return f"{v}%"

def configurar_ambiente():
    warnings.filterwarnings('ignore')
    # Configuração de exibição do Pandas
    pd.options.display.float_format = '{:,.2f}'.format

if __name__ == "__main__":
    configurar_ambiente()
    print("✅ Ambiente configurado")
    print("📦 Bibliotecas: pandas, numpy, plotly, scipy")
    print("🎨 Cores: Movidas para PREMISSAS (Célula 02)")