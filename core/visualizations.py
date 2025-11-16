# DENTRO DE: core/visualizations.py
import plotly.graph_objects as go
import pandas as pd

def _formatar_moeda(valor): 
    if pd.isna(valor) or valor is None: return "N/A"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def criar_grafico_waterfall(mrr_inicio: float, mrr_novos: float, mrr_churn: float, mrr_expansao: float, mrr_contracao: float, mrr_fim: float, mes: int) -> go.Figure:
    """Cria um gráfico Plotly Waterfall para o movimento de MRR."""
    fig_waterfall = go.Figure(go.Waterfall(
        name="MRR Movement",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "relative", "total"],
        x=["MRR Início", "+ Novos Clientes", "- Churn", "+ Expansão", "- Contração", "MRR Fim"],
        textposition="outside",
        text=[_formatar_moeda(x) for x in [mrr_inicio, mrr_novos, mrr_churn, mrr_expansao, mrr_contracao, mrr_fim]],
        y=[mrr_inicio, mrr_novos, -mrr_churn, mrr_expansao, -mrr_contracao, mrr_fim],
        connector={"line": {"color": "#E5E7EB"}},
        increasing={"marker": {"color": "#10B981"}},
        decreasing={"marker": {"color": "#EF4444"}},
        totals={"marker": {"color": "#1E3A8A"}}
    ))
    
    fig_waterfall.update_layout(
        height=400,
        title=f"Decomposição do MRR - Mês {mes}",
        showlegend=False,
        template='plotly_white'
    )
    return fig_waterfall
