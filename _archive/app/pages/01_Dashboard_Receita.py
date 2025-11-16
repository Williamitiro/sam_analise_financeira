"""
app/pages/01_Dashboard_Receita.py
Dashboard de Receita - Análise Completa do Motor de Crescimento
PADRÃO: Top da Indústria (Stripe, ChartMogul, Baremetrics)
Versão: 2.0 - UI/UX Profissional
"""

import sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent.parent
if str(RAIZ) not in sys.path: sys.path.append(str(RAIZ))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# ============================================================================
# IMPORTS DO CORE (COM TRY/EXCEPT PARA FALLBACK)
# ============================================================================
from core.config import ConfigFinanceira

# Tentar importar builders (não quebra se não existirem)
try:
    from core.builders.revenue_builder import RevenueBuilder, Plano
    HAS_REVENUE_BUILDER = True
except ImportError:
    HAS_REVENUE_BUILDER = False
    Plano = None

try:
    from core.builders.channels_builder import ChannelsBuilder, CanalAquisicao, TipoCanal
    HAS_CHANNELS_BUILDER = True
except ImportError:
    HAS_CHANNELS_BUILDER = False
    CanalAquisicao = None
    TipoCanal = None

try:
    from core.builders.capital_builder import CapitalBuilder, Aporte
    HAS_CAPITAL_BUILDER = True
except ImportError:
    HAS_CAPITAL_BUILDER = False
    Aporte = None

try:
    from core.builders.marketing_builder import MarketingBuilder
    HAS_MARKETING_BUILDER = True
except ImportError:
    HAS_MARKETING_BUILDER = False

# ============================================================================
# CONFIGURAÇÃO DE TEMA (DETECTA OU CRIA)
# ============================================================================
# Tenta detectar config.toml, senão usa tema padrão profissional
st.set_page_config(
    page_title="Dashboard de Receita - SAM",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Dashboard de Receita SAM - Análise Financeira Profissional"
    }
)

# Tema profissional (sobrescreve cores agressivas)
st.markdown("""
<style>
/* ===== SISTEMA DE DESIGN TOKENS ===== */
:root {
    --primary-color: #1E3A8A;      /* Azul profundo (confiança) */
    --secondary-color: #10B981;    /* Verde suave (crescimento) */
    --accent-color: #F59E0B;       /* Âmbar (atenção) */
    --danger-color: #EF4444;       /* Vermelho (churn) */
    --bg-primary: #FFFFFF;
    --bg-secondary: #F9FAFB;
    --bg-tertiary: #F3F4F6;
    --text-primary: #111827;
    --text-secondary: #6B7280;
    --border-color: #E5E7EB;
}

/* ===== TIPOGRAFIA E LAYOUT ===== */
.main-header {
    font-size: 2rem;
    font-weight: 600;
    color: var(--primary-color);
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.5px;
}

.section-container {
    background: var(--bg-primary);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1.5rem 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border: 1px solid var(--border-color);
}

.section-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.section-title::before {
    content: "📊";
    font-size: 1.5rem;
}

/* ===== CARDS DE MÉTRICAS (KPI) ===== */
.kpi-card {
    background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    border-left: 4px solid var(--primary-color);
    transition: all 0.2s ease;
    height: 100%;
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.kpi-label {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
}

.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
    line-height: 1;
}

.kpi-delta {
    font-size: 0.875rem;
    font-weight: 600;
    margin-top: 0.5rem;
}

.delta-positive { color: var(--secondary-color); }
.delta-negative { color: var(--danger-color); }
.delta-neutral { color: var(--text-secondary); }

/* ===== SPARKLINES MINIMALISTAS ===== */
.sparkline-container {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--bg-tertiary);
}

.sparkline {
    height: 40px;
    margin: 0;
}

/* ===== FILTROS E CONTROLES ===== */
.filter-container {
    background: var(--bg-secondary);
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1.5rem;
}

.filter-title {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
}

/* ===== GRÁFICOS ===== */
.chart-container {
    background: var(--bg-primary);
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border: 1px solid var(--border-color);
}

.chart-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 1rem;
}

/* ===== INSIGHTS ===== */
.insight-box {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border-left: 4px solid var(--primary-color);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
}

.insight-title {
    font-weight: 600;
    color: var(--primary-color);
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.insight-value {
    font-size: 1.125rem;
    font-weight: 700;
    color: var(--text-primary);
}

/* ===== MILESTONES ===== */
.milestone-progress {
    background: var(--bg-tertiary);
    border-radius: 20px;
    height: 8px;
    overflow: hidden;
    margin: 0.5rem 0;
}

.milestone-bar {
    height: 100%;
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    border-radius: 20px;
    transition: width 0.3s ease;
}

.milestone-text {
    font-size: 0.75rem;
    color: var(--text-secondary);
    text-align: right;
    margin-top: 0.25rem;
}

/* ===== ALERTAS ===== */
.alert-warning {
    background: #FFFBEB;
    border: 1px solid var(--accent-color);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
}

.alert-info {
    background: #EFF6FF;
    border: 1px solid var(--primary-color);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
}

/* ===== RESPONSIVIDADE ===== */
@media (max-width: 768px) {
    .kpi-value { font-size: 1.5rem; }
    .section-title { font-size: 1.125rem; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNÇÕES AUXILIARES (MANTIDAS - NÃO QUEBRAR LÓGICA)
# ============================================================================
def formatar_moeda(valor): 
    if pd.isna(valor) or valor is None: return "N/A"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_percentual(valor): 
    if pd.isna(valor) or valor is None: return "N/A"
    return f"{valor:.1f}%"

def calcular_growth_rate(df, coluna='MRR'): 
    return df[coluna].pct_change() * 100

# ============================================================================
# VERIFICAÇÃO INICIAL (MANTIDA)
# ============================================================================
if 'df_projecao' not in st.session_state or st.session_state.df_projecao is None:
    st.error("⚠️ **Nenhuma projeção encontrada**")
    st.info("Execute uma projeção no Dashboard Principal primeiro")
    st.stop()

df = st.session_state.df_projecao.copy()
config = st.session_state.get('config', ConfigFinanceira())

# ============================================================================
# DETECÇÃO INTELIGENTE DE COLUNAS (MELHORADA)
# ============================================================================
colunas_existentes = set(df.columns.tolist())

# Verifica quais features estão disponíveis
FEATURES_DISPONIVEIS = {
    'breakdown_planos': {'MRR_Lite', 'MRR_Trader', 'MRR_Pro'}.issubset(colunas_existentes),
    'waterfall': {'MRR_Novos_Clientes', 'MRR_Churn'}.issubset(colunas_existentes),
    'cohorts': {'Novos_Pagantes', 'Churn_Absoluto'}.issubset(colunas_existentes),
    'funil': {'Visitantes', 'Trials', 'Conversao_Rate'}.issubset(colunas_existentes),
    'capital': HAS_CAPITAL_BUILDER,
}

# Mensagens de debug (só aparecem quando faltam dados)
debug_messages = []
if not FEATURES_DISPONIVEIS['breakdown_planos']:
    debug_messages.append("💡 **Dica**: Ative RevenueBuilder para ver breakdown por plano")
if not FEATURES_DISPONIVEIS['waterfall']:
    debug_messages.append("💡 **Dica**: Ative RevenueBuilder com MRR Movement para waterfall real")
if not FEATURES_DISPONIVEIS['funil']:
    debug_messages.append("💡 **Dica**: Ative ChannelsBuilder para ver funil de conversão")

# ============================================================================
# SIDEBAR REESTRUTURADA (FILTROS LÓGICOS)
# ============================================================================
with st.sidebar:
    st.markdown('<div class="filter-title">📊 Período de Análise</div>', unsafe_allow_html=True)
    
    max_mes = len(df)
    periodo = st.slider(
        "Selecione o período",
        min_value=1,
        max_value=max_mes,
        value=(max(1, max_mes-11), max_mes),  # Últimos 12 meses por padrão
        help="Filtro global para todas as seções"
    )
    
    st.markdown("---")
    
    st.markdown('<div class="filter-title">🎨 Opções de Visualização</div>', unsafe_allow_html=True)
    
    # Opções que SEMPRE funcionam
    mostrar_sparklines = st.checkbox("Mini gráficos nos KPIs", value=True, help="Mostra sparklines abaixo dos cards")
    
    # Opções condicionais (só aparecem se os dados existirem)
    mostrar_projecoes = st.checkbox("Projeções de milestones", value=True, help="Mostra quando atingirá metas")
    
    # Checkboxes para features específicas (só aparecem se disponíveis)
    if FEATURES_DISPONIVEIS['breakdown_planos']:
        st.session_state['show_planos'] = st.checkbox("Breakdown por plano", value=True)
    
    if FEATURES_DISPONIVEIS['cohorts']:
        st.session_state['show_cohorts'] = st.checkbox("Análise de cohorts", value=True)
    
    if FEATURES_DISPONIVEIS['funil']:
        st.session_state['show_funnel'] = st.checkbox("Funil de conversão", value=True)
    
    st.markdown("---")
    
    # Métricas de comparação (sempre disponíveis)
    st.markdown('<div class="filter-title">📈 Comparar com</div>', unsafe_allow_html=True)
    comparador = st.selectbox(
        "Período de referência",
        ["Mês Anterior", "Trimestre Anterior", "Média 3M", "Meta Configurada"],
        help="Define a base de comparação para deltas"
    )
    
    # Meta de MRR (interativa)
    st.markdown('<div class="filter-title">🎯 Milestone Alvo</div>', unsafe_allow_html=True)
    meta_mrr = st.number_input(
        "Meta MRR (R$)",
        min_value=10000,
        max_value=10000000,
        value=100000,
        step=10000,
        help="Usado para projeções na seção de milestones"
    )

# Aplica filtro de período
df_filtrado = df[(df['mes'] >= periodo[0]) & (df['mes'] <= periodo[1])].copy()

# ============================================================================
# HEADER PROFISSIONAL
# ============================================================================
st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
    <div>
        <h1 class="main-header">💰 Dashboard de Receita</h1>
        <p style="color: var(--text-secondary); margin: 0;">
            Análise Completa do Motor de Crescimento | 
            Período: Mês {periodo[0]} a {periodo[1]}
        </p>
    </div>
    <div style="text-align: right;">
        <p style="color: var(--text-secondary); font-size: 0.875rem; margin: 0;">Última atualização</p>
        <p style="font-weight: 600; margin: 0;">{datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Mostrar dicas se features estiverem desativadas
if debug_messages:
    with st.expander("🔍 Dicas para melhorar seu dashboard"):
        for msg in debug_messages:
            st.info(msg)

# ============================================================================
# SEÇÃO 1: KPIs COM NOVO LAYOUT DE CARDS
# ============================================================================
st.markdown('<div class="section-title">🎯 Visão Geral</div>', unsafe_allow_html=True)

# Container para KPIs
kpi_container = st.container()

with kpi_container:
    # Calcula métricas
    current = df_filtrado.iloc[-1]
    previous = df_filtrado.iloc[-2] if len(df_filtrado) > 1 else current
    
    # Função para calcular delta baseado no comparador
    def calcular_delta(atual, anterior, tipo='moeda'):
        if tipo == 'moeda':
            valor = atual - anterior
            pct = (valor / max(1, anterior)) * 100
            return formatar_moeda(valor), f"{pct:+.1f}%"
        elif tipo == 'percentual':
            delta = atual - anterior
            return f"{delta:+.1f}pp", f"{delta:+.1f}%"
        else:
            valor = atual - anterior
            pct = (valor / max(1, anterior)) * 100
            return f"{valor:+,}".replace(",", "."), f"{pct:+.1f}%"
    
    # Prepara dados dos KPIs
    kpis = [
        {
            'titulo': 'MRR Atual',
            'icone': '💰',
            'valor': formatar_moeda(current['MRR']),
            'delta': calcular_delta(current['MRR'], previous['MRR']),
            'cor_delta': 'positive' if current['MRR'] >= previous['MRR'] else 'negative',
            'sparkline': df_filtrado['MRR'],
            'help': 'Monthly Recurring Revenue'
        },
        {
            'titulo': 'ARR',
            'icone': '📅',
            'valor': formatar_moeda(current['MRR'] * 12),
            'delta': calcular_delta(current['MRR'] * 12, previous['MRR'] * 12),
            'cor_delta': 'positive' if current['MRR'] >= previous['MRR'] else 'negative',
            'sparkline': df_filtrado['MRR'] * 12,
            'help': 'Annual Recurring Revenue'
        },
        {
            'titulo': 'ARPU',
            'icone': '👤',
            'valor': formatar_moeda(current['ARPU']),
            'delta': calcular_delta(current['ARPU'], previous['ARPU']),
            'cor_delta': 'positive' if current['ARPU'] >= previous['ARPU'] else 'negative',
            'sparkline': df_filtrado['ARPU'],
            'help': 'Average Revenue Per User'
        },
        {
            'titulo': 'Usuários',
            'icone': '👥',
            'valor': f"{int(current['Usuarios_Finais']):,}".replace(",", "."),
            'delta': calcular_delta(current['Usuarios_Finais'], previous['Usuarios_Finais'], 'int'),
            'cor_delta': 'positive' if current['Usuarios_Finais'] >= previous['Usuarios_Finais'] else 'negative',
            'sparkline': df_filtrado['Usuarios_Finais'],
            'help': 'Total de usuários pagantes'
        },
        {
            'titulo': 'Churn Rate',
            'icone': '📉',
            'valor': f"{current.get('Churn_Rate', config.churn_mensal) * 100:.1f}%",
            'delta': None,  # Churn não tem delta claro no modelo atual
            'cor_delta': 'neutral',
            'sparkline': None,
            'help': 'Taxa de churn mensal'
        },
    ]
    
    # Renderiza KPIs em grid responsivo
    cols = st.columns(5)
    for i, kpi in enumerate(kpis):
        with cols[i]:
            # Card principal
            st.markdown(f"""
            <div class="kpi-card" title="{kpi['help']}">
                <div class="kpi-label">{kpi['icone']} {kpi['titulo']}</div>
                <div class="kpi-value">{kpi['valor']}</div>
                {f'<div class="kpi-delta delta-{kpi["cor_delta"]}">{kpi["delta"][1]}</div>' if kpi['delta'] else ''}
            </div>
            """, unsafe_allow_html=True)
    
    # Sparklines em linha separada (se ativado)
    if mostrar_sparklines:
        st.markdown('<div class="sparkline-container"></div>', unsafe_allow_html=True)
        spark_cols = st.columns(4)  # Churn não tem sparkline
        
        for i, kpi in enumerate(kpis[:-1]):  # Exclui churn
            if kpi['sparkline'] is not None:
                with spark_cols[i]:
                    fig_spark = go.Figure(go.Scatter(
                        y=kpi['sparkline'].tail(12),
                        mode='lines',
                        line=dict(color='#1E3A8A', width=2),
                        fill='tozeroy',
                        fillcolor='rgba(30, 58, 138, 0.1)'
                    ))
                    fig_spark.update_layout(
                        height=40,
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(visible=False),
                        yaxis=dict(visible=False),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_spark, use_container_width=True, config={'displayModeBar': False})

# ============================================================================
# SEÇÃO 2: CRESCIMENTO DE MRR (COM FILTROS DE VISUALIZAÇÃO)
# ============================================================================
st.markdown('<div class="section-title">📈 Crescimento de MRR</div>', unsafe_allow_html=True)

# Filtros específicos para esta seção
col_filtros1, col_filtros2 = st.columns(2)
with col_filtros1:
    show_growth_rate = st.checkbox("Mostrar taxa de crescimento", value=True, key="show_growth")
with col_filtros2:
    show_mrr_line = st.checkbox("Mostrar linha de MRR", value=True, key="show_mrr")

# Calcula growth rate
df_filtrado['MRR_Growth_Rate'] = calcular_growth_rate(df_filtrado, 'MRR')

# Gráfico interativo
fig_crescimento = make_subplots(
    rows=2, cols=1,
    row_heights=[0.6, 0.4],
    subplot_titles=("MRR ao Longo do Tempo", "Taxa de Crescimento Mensal"),
    vertical_spacing=0.12,
    specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
)

# Linha MRR (pode ser desligada)
if show_mrr_line:
    fig_crescimento.add_trace(
        go.Scatter(
            x=df_filtrado['mes'],
            y=df_filtrado['MRR'],
            name='MRR',
            line=dict(color='#1E3A8A', width=3, shape='spline'),
            fill='tozeroy',
            fillcolor='rgba(30, 58, 138, 0.1)',
            hovertemplate='<b>Mês %{x}</b><br>MRR: R$ %{y:,.2f}<extra></extra>'
        ),
        row=1, col=1
    )

# Barras Growth Rate (pode ser desligada)
if show_growth_rate:
    cores_growth = [
        '#10B981' if x >= 10 else '#F59E0B' if x >= 5 else '#EF4444' 
        for x in df_filtrado['MRR_Growth_Rate']
    ]
    
    fig_crescimento.add_trace(
        go.Bar(
            x=df_filtrado['mes'],
            y=df_filtrado['MRR_Growth_Rate'],
            name='Growth Rate',
            marker_color=cores_growth,
            showlegend=False,
            hovertemplate='<b>Mês %{x}</b><br>Growth: %{y:.1f}%<extra></extra>'
        ),
        row=2, col=1
    )

# Layout
fig_crescimento.update_xaxes(title_text="Mês", row=2, col=1)
fig_crescimento.update_yaxes(title_text="R$", row=1, col=1, tickformat='.2s')
fig_crescimento.update_yaxes(title_text="%", row=2, col=1)

fig_crescimento.update_layout(
    height=500,
    hovermode='x unified',
    template='plotly_white',
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_crescimento, use_container_width=True, config={'displayModeBar': False})

# Insights de crescimento (cards ao invés de HTML bruto)
col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    growth_medio = df_filtrado['MRR_Growth_Rate'].mean()
    status_growth = "✅ Acima da meta" if growth_medio >= 10 else "⚠️ Abaixo da meta"
    
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">📊 Crescimento Médio</div>
        <div class="insight-value">{growth_medio:.1f}%/mês</div>
        <div style="color: var(--text-secondary); font-size: 0.875rem; margin-top: 0.25rem;">
            {status_growth} (meta: 10%/mês)
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_insight2:
    growth_recente = df_filtrado['MRR_Growth_Rate'].tail(3).mean()
    growth_anterior = df_filtrado['MRR_Growth_Rate'].iloc[-6:-3].mean() if len(df_filtrado) >= 6 else growth_medio
    
    if growth_recente > growth_anterior * 1.15:
        status = "🚀 Acelerando"
        cor = "#10B981"
    elif growth_recente < growth_anterior * 0.85:
        status = "⚠️ Desacelerando"
        cor = "#EF4444"
    else:
        status = "➡️ Estável"
        cor = "#6B7280"
    
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title" style="color: {cor};">{status}</div>
        <div class="insight-value" style="color: {cor};">{growth_recente:.1f}% (últimos 3m)</div>
        <div style="color: var(--text-secondary); font-size: 0.875rem; margin-top: 0.25rem;">
            vs {growth_anterior:.1f}% (3m anteriores)
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SEÇÃO 3: BREAKDOWN POR PLANO (SOMENTE SE DISPONÍVEL)
# ============================================================================
if FEATURES_DISPONIVEIS['breakdown_planos'] and st.session_state.get('show_planos', True):
    st.markdown('<div class="section-title">🎨 Composição de Receita por Plano</div>', unsafe_allow_html=True)
    
    planos_info = [
        {'nome': 'Lite', 'cor': '#3B82F6'},
        {'nome': 'Trader', 'cor': '#10B981'},
        {'nome': 'Pro', 'cor': '#8B5CF6'}
    ]
    
    # Gráfico stacked area
    fig_planos = go.Figure()
    
    for plano in planos_info:
        col_mrr = f"MRR_{plano['nome']}"
        if col_mrr in df_filtrado.columns:
            fig_planos.add_trace(go.Scatter(
                x=df_filtrado['mes'],
                y=df_filtrado[col_mrr],
                mode='lines',
                stackgroup='one',
                name=plano['nome'],
                line=dict(color=plano['cor'], width=0),
                fillcolor=plano['cor'],
                hovertemplate=f"<b>{plano['nome']}</b><br>Mês %{{x}}<br>MRR: R$ %{{y:,.2f}}<extra></extra>"
            ))
    
    fig_planos.update_layout(
        height=400,
        xaxis_title="Mês",
        yaxis_title="R$",
        hovermode='x unified',
        template='plotly_white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_planos, use_container_width=True, config={'displayModeBar': False})
    
    # Tabela de mix atual (com formatação melhorada)
    st.markdown("#### Mix Atual de Planos")
    
    mrr_total = df_filtrado.iloc[-1]['MRR']
    mix_data = []
    
    for plano in planos_info:
        col_mrr = f"MRR_{plano['nome']}"
        col_arpu = f"ARPU_{plano['nome']}"
        
        if col_mrr in df_filtrado.columns:
            mrr_plano = df_filtrado.iloc[-1][col_mrr]
            pct = (mrr_plano / mrr_total * 100) if mrr_total > 0 else 0
            arpu_plano = df_filtrado.iloc[-1].get(col_arpu, df_filtrado.iloc[-1]['ARPU'])
            usuarios_plano = int(mrr_plano / max(1, arpu_plano))
            
            mix_data.append({
                'Plano': plano['nome'],
                'MRR': formatar_moeda(mrr_plano),
                'Mix': f"{pct:.1f}%",
                'ARPU': formatar_moeda(arpu_plano),
                'Clientes': f"{usuarios_plano:,}".replace(",", ".")
            })
    
    if mix_data:
        df_mix = pd.DataFrame(mix_data)
        st.dataframe(
            df_mix,
            use_container_width=True,
            hide_index=True,
            column_config={
                'Plano': st.column_config.TextColumn(width='small'),
                'MRR': st.column_config.TextColumn(width='medium'),
                'Mix': st.column_config.TextColumn(width='small'),
                'ARPU': st.column_config.TextColumn(width='medium'),
                'Clientes': st.column_config.TextColumn(width='medium'),
            }
        )
    else:
        st.info("ℹ️ Aguardando dados de planos...")

# ============================================================================
# SEÇÃO 4: WATERFALL DE RECEITA (COM DETECÇÃO INTELIGENTE)
# ============================================================================
st.markdown('<div class="section-title">💧 Waterfall de Receita</div>', unsafe_allow_html=True)

# Verifica se tem dados completos de waterfall
if FEATURES_DISPONIVEIS['waterfall'] and len(df_filtrado) >= 2:
    mes_atual = df_filtrado.iloc[-1]
    mes_anterior = df_filtrado.iloc[-2]
    
    # Valores reais do DataFrame
    mrr_inicio = mes_anterior['MRR']
    mrr_fim = mes_atual['MRR']
    mrr_novos = mes_atual['MRR_Novos_Clientes']
    mrr_churn = mes_atual['MRR_Churn']
    mrr_expansao = mes_atual.get('MRR_Expansao', 0)
    mrr_contracao = mes_atual.get('MRR_Contracao', 0)
    
    # Validação do waterfall
    mrr_calculado = mrr_inicio + mrr_novos - mrr_churn + mrr_expansao - mrr_contracao
    discrepancia = abs(mrr_calculado - mrr_fim)
    
    if discrepancia > 10:  # Mais de R$10 de diferença
        st.warning(f"⚠️ Divergência no waterfall: R$ {discrepancia:,.2f}")
    
    # Gráfico waterfall
    fig_waterfall = go.Figure(go.Waterfall(
        name="MRR Movement",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "relative", "total"],
        x=["MRR Início", "+ Novos Clientes", "- Churn", "+ Expansão", "- Contração", "MRR Fim"],
        textposition="outside",
        text=[formatar_moeda(x) for x in [mrr_inicio, mrr_novos, mrr_churn, mrr_expansao, mrr_contracao, mrr_fim]],
        y=[mrr_inicio, mrr_novos, -mrr_churn, mrr_expansao, -mrr_contracao, mrr_fim],
        connector={"line": {"color": "#E5E7EB"}},
        increasing={"marker": {"color": "#10B981"}},
        decreasing={"marker": {"color": "#EF4444"}},
        totals={"marker": {"color": "#1E3A8A"}}
    ))
    
    fig_waterfall.update_layout(
        height=400,
        title=f"Decomposição do MRR - Mês {int(mes_atual['mes'])}",
        showlegend=False,
        template='plotly_white'
    )
    
    st.plotly_chart(fig_waterfall, use_container_width=True, config={'displayModeBar': False})
    
    # Métricas de retenção (cards)
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        nrr = ((mrr_fim - mrr_novos) / max(1, mrr_inicio)) * 100
        st.metric(
            "Net Revenue Retention",
            f"{nrr:.1f}%",
            help="Receita retida dos clientes existentes (exclui novos)"
        )
    
    with col_m2:
        gross_churn = (mrr_churn / max(1, mrr_inicio)) * 100
        st.metric(
            "Gross Churn",
            f"{gross_churn:.1f}%",
            help="Receita perdida por churn bruto",
            delta_color="inverse"
        )
    
    with col_m3:
        exp_rate = (mrr_expansao / max(1, mrr_inicio)) * 100
        st.metric(
            "Expansion Rate",
            f"{exp_rate:.1f}%",
            help="Receita ganha por expansão (upsell)"
        )

else:
    # Fallback simplificado (não quebra o dashboard)
    st.info("ℹ️ **Waterfall simplificado** - Dados detalhados não disponíveis")
    
    if len(df_filtrado) >= 2:
        mes_atual = df_filtrado.iloc[-1]
        mes_anterior = df_filtrado.iloc[-2]
        
        mrr_inicio = mes_anterior['MRR']
        mrr_fim = mes_atual['MRR']
        
        # Estima novos clientes por variação de usuários
        delta_usuarios = mes_atual['Usuarios_Finais'] - mes_anterior['Usuarios_Finais']
        churn_estimado = mes_anterior['Usuarios_Finais'] * config.churn_mensal
        novos_estimados = max(0, delta_usuarios + churn_estimado)
        
        mrr_novos = novos_estimados * mes_atual['ARPU']
        mrr_churn = churn_estimado * mes_anterior['ARPU']
        
        fig_fallback = go.Figure(go.Waterfall(
            orientation="v",
            measure=["absolute", "relative", "relative", "total"],
            x=["MRR Início", "+ Novos Estimados", "- Churn Estimado", "MRR Fim"],
            y=[mrr_inicio, mrr_novos, -mrr_churn, mrr_fim],
            connector={"line": {"color": "#E5E7EB"}},
            increasing={"marker": {"color": "#10B981"}},
            decreasing={"marker": {"color": "#EF4444"}},
            totals={"marker": {"color": "#6B7280"}}
        ))
        
        fig_fallback.update_layout(
            height=350,
            title="Waterfall (Estimado)",
            showlegend=False,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_fallback, use_container_width=True, config={'displayModeBar': False})

# ============================================================================
# SEÇÃO 5: FUNIL DE CONVERSÃO (SE DISPONÍVEL)
# ============================================================================
if FEATURES_DISPONIVEIS['funil'] and st.session_state.get('show_funnel', True):
    st.markdown('<div class="section-title">🔄 Funil de Conversão</div>', unsafe_allow_html=True)
    
    # Selecionar canal específico ou todos
    if hasattr(config, 'canais_aquisicao') and config.canais_aquisicao:
        canais_nomes = ["Todos os Canais"] + [c.nome for c in config.canais_aquisicao]
        canal_selecionado = st.selectbox("Visualizar canal", canais_nomes, key="canal_funil")
    else:
        canal_selecionado = "Todos os Canais"
    
    mes_atual = df_filtrado.iloc[-1]
    
    # Dados do funil
    if canal_selecionado == "Todos os Canais":
        visitantes = int(mes_atual.get('Visitantes', 0))
        trials = int(mes_atual.get('Trials', 0))
        pagantes = int(mes_atual.get('Novos_Pagantes', 0))
        cac = mes_atual.get('CAC', mes_atual.get('Custo_Marketing', 0) / max(1, pagantes))
    else:
        # Filtra por canal específico (se dados existirem)
        # Note: Isso requer que o DataFrame tenha colunas por canal
        visitantes = int(mes_atual.get(f'Visitantes_{canal_selecionado}', 0))
        trials = int(mes_atual.get(f'Trials_{canal_selecionado}', 0))
        pagantes = int(mes_atual.get(f'Pagantes_{canal_selecionado}', 0))
        cac = mes_atual.get(f'CAC_{canal_selecionado}', 0)
    
    if visitantes > 0:
        # Gráfico funil
        fig_funnel = go.Figure(go.Funnel(
            y=["Visitantes", "Trials", "Pagantes"],
            x=[visitantes, trials, pagantes],
            textinfo="value+percent initial",
            marker=dict(
                color=["#6B7280", "#F59E0B", "#10B981"],
                line=dict(color="rgba(255,255,255,0.5)", width=2)
            ),
            textfont=dict(size=12),
            hovertemplate="<b>%{label}</b><br>Valor: %{value:,}<br>Taxa: %{percentInitial}%<extra></extra>"
        ))
        
        fig_funnel.update_layout(
            height=400,
            title=f"Funil de Conversão - {canal_selecionado}",
            template='plotly_white',
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        st.plotly_chart(fig_funnel, use_container_width=True, config={'displayModeBar': False})
        
        # Métricas do funil
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        
        with col_f1:
            taxa_trial = trials / visitantes * 100 if visitantes > 0 else 0
            st.metric("Trial Rate", f"{taxa_trial:.1f}%")
        
        with col_f2:
            taxa_conv = pagantes / trials * 100 if trials > 0 else 0
            st.metric("Conversão Trial→Pagante", f"{taxa_conv:.1f}%")
        
        with col_f3:
            st.metric("CAC", formatar_moeda(cac))
        
        with col_f4:
            if hasattr(config, 'arpu_medio') and config.arpu_medio > 0:
                payback = cac / config.arpu_medio
                st.metric("Payback (meses)", f"{payback:.1f}")

# ============================================================================
# SEÇÃO 6: COHORTS (SE DISPONÍVEL)
# ============================================================================
if FEATURES_DISPONIVEIS['cohorts'] and st.session_state.get('show_cohorts', True):
    st.markdown('<div class="section-title">👥 Análise de Retenção (Cohorts)</div>', unsafe_allow_html=True)
    
    @st.cache_data
    def gerar_cohort_matrix(df):
        """Gera matriz de cohorts (otimizada)"""
        try:
            meses = df['mes'].unique()[:12]
            cohort_data = []
            
            for i, mes_cohort in enumerate(meses):
                linha = {'Cohort': f"Mês {mes_cohort}"}
                usuarios_cohort = df[df['mes'] == mes_cohort]['Novos_Pagantes'].iloc[0]
                
                if usuarios_cohort <= 0:
                    continue
                
                for idade in range(0, min(12, len(meses) - i)):
                    mes_futuro = mes_cohort + idade
                    if mes_futuro in df['mes'].values:
                        try:
                            # Busca o cohort específico (aproximação)
                            df_cohort = df[df['mes'] == mes_futuro]
                            if not df_cohort.empty:
                                # Aproximação: assume que os usuários remanescentes incluem o cohort
                                total_remanescente = df_cohort['Usuarios_Finais'].iloc[0]
                                cohort_original = sum(df[(df['mes'] == mes_cohort)]['Novos_Pagantes'])
                                
                                if cohort_original > 0:
                                    retencao = min(100, (total_remanescente / cohort_original) * 100)
                                    linha[f"M{idade}"] = retencao
                                else:
                                    linha[f"M{idade}"] = None
                            else:
                                linha[f"M{idade}"] = None
                        except:
                            linha[f"M{idade}"] = None
                    else:
                        linha[f"M{idade}"] = None
                
                cohort_data.append(linha)
            
            return pd.DataFrame(cohort_data) if cohort_data else None
        except Exception as e:
            st.error(f"Erro ao gerar cohorts: {e}")
            return None
    
    cohort_df = gerar_cohort_matrix(df_filtrado)
    
    if cohort_df is not None and not cohort_df.empty:
        # Seletor de visualização
        viz_cohort = st.radio("Visualização", ["Heatmap", "Linhas"], horizontal=True, key="viz_cohort")
        
        if viz_cohort == "Heatmap":
            # Heatmap
            fig_cohort = go.Figure(data=go.Heatmap(
                z=cohort_df.iloc[:, 1:].values,
                x=cohort_df.columns[1:],
                y=cohort_df['Cohort'],
                colorscale='RdYlGn',
                text=cohort_df.iloc[:, 1:].values,
                texttemplate="%{text:.1f}%",
                textfont={"size": 10},
                hoverongaps=False,
                hovertemplate="Cohort: %{y}<br>Mês: %{x}<br>Retenção: %{z:.1f}%<extra></extra>"
            ))
            
            fig_cohort.update_layout(
                height=500,
                title="Taxa de Retenção por Cohort (%)",
                template='plotly_white',
                xaxis_title="Idade do Cohort (meses)",
                yaxis_title="Cohort (mês de aquisição)"
            )
            
            st.plotly_chart(fig_cohort, use_container_width=True, config={'displayModeBar': False})
        
        else:
            # Linhas
            fig_cohort_lines = go.Figure()
            
            for i, row in cohort_df.iterrows():
                meses = list(range(len(row[1:])))
                valores = row[1:].values
                
                fig_cohort_lines.add_trace(go.Scatter(
                    x=meses,
                    y=valores,
                    mode='lines+markers',
                    name=row['Cohort'],
                    line=dict(width=2),
                    hovertemplate="%{fullData.name}<br>Mês %{x}: %{y:.1f}%<extra></extra>"
                ))
            
            fig_cohort_lines.update_layout(
                height=500,
                title="Curvas de Retenção por Cohort",
                template='plotly_white',
                xaxis_title="Idade do Cohort (meses)",
                yaxis_title="Retenção (%)",
                legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
            )
            
            st.plotly_chart(fig_cohort_lines, use_container_width=True, config={'displayModeBar': False})
        
        # Métricas de churn
        st.markdown("#### Métricas de Churn")
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            churn_mensal_medio = (df_filtrado['Churn_Absoluto'] / df_filtrado['Usuarios_Iniciais'] * 100).mean()
            st.metric("Churn Médio", f"{churn_mensal_medio:.1f}%")
        
        with col_c2:
            if len(cohort_df.columns) > 2:
                retencao_m1 = cohort_df['M1'].mean()
                st.metric("Retenção Mês 1", f"{retencao_m1:.1f}%")

# ============================================================================
# SEÇÃO 7: ARPU EVOLUTION
# ============================================================================
st.markdown('<div class="section-title">💎 Evolução do ARPU</div>', unsafe_allow_html=True)

# Filtros de ARPU
col_arpu1, col_arpu2 = st.columns(2)
with col_arpu1:
    show_arpu_geral = st.checkbox("ARPU Geral", value=True, key="arpu_geral")
with col_arpu2:
    show_arpu_planos = False
    if FEATURES_DISPONIVEIS['breakdown_planos']:
        show_arpu_planos = st.checkbox("ARPU por Plano", value=True, key="arpu_planos")

# Gráfico
fig_arpu = go.Figure()

# ARPU Geral
if show_arpu_geral:
    fig_arpu.add_trace(go.Scatter(
        x=df_filtrado['mes'],
        y=df_filtrado['ARPU'],
        mode='lines+markers',
        name='ARPU Geral',
        line=dict(color='#1E3A8A', width=3),
        hovertemplate='<b>ARPU Geral</b><br>Mês %{x}<br>Valor: R$ %{y:,.2f}<extra></extra>'
    ))

# ARPU por plano
if show_arpu_planos and FEATURES_DISPONIVEIS['breakdown_planos']:
    for plano in ['Lite', 'Trader', 'Pro']:
        col_arpu = f'ARPU_{plano}'
        if col_arpu in df_filtrado.columns:
            fig_arpu.add_trace(go.Scatter(
                x=df_filtrado['mes'],
                y=df_filtrado[col_arpu],
                mode='lines',
                name=f'ARPU {plano}',
                hovertemplate=f'<b>ARPU {plano}</b><br>Mês %{{x}}<br>Valor: R$ %{{y:,.2f}}<extra></extra>'
            ))

fig_arpu.update_layout(
    height=400,
    title="Evolução do ARPU ao Longo do Tempo",
    xaxis_title="Mês",
    yaxis_title="R$",
    template='plotly_white',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_arpu, use_container_width=True, config={'displayModeBar': False})

# ============================================================================
# SEÇÃO 8: MILESTONES & PROJEÇÕES
# ============================================================================
if mostrar_projecoes:
    st.markdown('<div class="section-title">🚀 Milestones & Projeções</div>', unsafe_allow_html=True)
    
    # Container para milestones
    milestone_container = st.container()
    
    with milestone_container:
        # Calcula projeção
        mes_atual = int(df_filtrado.iloc[-1]['mes'])
        mrr_atual = df_filtrado.iloc[-1]['MRR']
        growth_rate = df_filtrado['MRR_Growth_Rate'].tail(3).mean() / 100
        
        # Métricas de milestones
        milestones = [
            {'nome': 'R$ 50k MRR', 'valor': 50000, 'cor': '#6B7280'},
            {'nome': 'R$ 100k MRR', 'valor': meta_mrr, 'cor': '#1E3A8A'},
            {'nome': 'R$ 1M ARR', 'valor': 1000000/12, 'cor': '#8B5CF6'},
        ]
        
        cols_milestone = st.columns(len(milestones))
        
        for i, milestone in enumerate(milestones):
            with cols_milestone[i]:
                progresso = min(100, (mrr_atual / milestone['valor']) * 100)
                
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 1rem;">
                    <div style="font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 0.5rem;">
                        {milestone['nome']}
                    </div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: {milestone['cor']};">
                        {progresso:.0f}%
                    </div>
                </div>
                <div class="milestone-progress">
                    <div class="milestone-bar" style="width: {progresso}%; background: {milestone['cor']};"></div>
                </div>
                """, unsafe_allow_html=True)
                
                if progresso < 100 and growth_rate > 0:
                    meses_faltando = np.log(milestone['valor'] / mrr_atual) / np.log(1 + growth_rate)
                    data_estimada = datetime.now() + timedelta(days=30 * meses_faltando)
                    st.markdown(f'<div class="milestone-text">~{int(meses_faltando)} meses</div>', unsafe_allow_html=True)
                elif progresso >= 100:
                    st.markdown('<div class="milestone-text" style="color: #10B981;">✅ Alcançado!</div>', unsafe_allow_html=True)
        
        # Trajetória visual
        if growth_rate > 0:
            st.markdown("#### Trajetória Projetada")
            
            meses_proj = list(range(mes_atual, mes_atual + 24))  # Próximos 24 meses
            mrr_proj = [mrr_atual * (1 + growth_rate) ** (i - mes_atual) for i in meses_proj]
            
            fig_proj = go.Figure()
            
            # Histórico
            fig_proj.add_trace(go.Scatter(
                x=df_filtrado['mes'],
                y=df_filtrado['MRR'],
                mode='lines',
                name='Histórico',
                line=dict(color='#1E3A8A', width=3),
                hovertemplate='<b>Histórico</b><br>Mês %{x}<br>MRR: R$ %{y:,.2f}<extra></extra>'
            ))
            
            # Projeção
            fig_proj.add_trace(go.Scatter(
                x=meses_proj,
                y=mrr_proj,
                mode='lines',
                name='Projeção',
                line=dict(color='#10B981', width=2, dash='dot'),
                hovertemplate='<b>Projeção</b><br>Mês %{x}<br>MRR: R$ %{y:,.2f}<extra></extra>'
            ))
            
            # Linhas de milestone
            for milestone in milestones:
                fig_proj.add_hline(
                    y=milestone['valor'],
                    line_dash="dash",
                    line_color=milestone['cor'],
                    annotation_text=milestone['nome'],
                    annotation_position="top right"
                )
            
            fig_proj.update_layout(
                height=400,
                title="Trajetória até os Próximos Milestones",
                xaxis_title="Mês",
                yaxis_title="MRR (R$)",
                template='plotly_white',
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_proj, use_container_width=True, config={'displayModeBar': False})
        else:
            st.warning("⚠️ Crescimento negativo ou zero - não é possível projetar milestones")

# ============================================================================
# RODAPÉ COM DIAGNÓSTICO
# ============================================================================
st.markdown("---")

with st.expander("📊 Diagnóstico do Dashboard", expanded=False):
    col_diag1, col_diag2 = st.columns(2)
    
    with col_diag1:
        st.markdown("**Builders Detectados:**")
        builders_status = {
            'RevenueBuilder': HAS_REVENUE_BUILDER,
            'MarketingBuilder': HAS_MARKETING_BUILDER,
            'ChannelsBuilder': HAS_CHANNELS_BUILDER,
            'CapitalBuilder': HAS_CAPITAL_BUILDER,
        }
        
        for nome, ativo in builders_status.items():
            status = "✅ Ativo" if ativo else "❌ Inativo"
            st.markdown(f"- {nome}: {status}")
    
    with col_diag2:
        st.markdown("**Features Disponíveis:**")
        for feature, disponivel in FEATURES_DISPONIVEIS.items():
            status = "✅ Sim" if disponivel else "❌ Não"
            st.markdown(f"- {feature.replace('_', ' ').title()}: {status}")
    
    # Preview de dados
    st.markdown("**Amostra do DataFrame:**")
    st.dataframe(df.head(3), use_container_width=True)

# Botão para recarregar
st.markdown('<div style="text-align: center; margin-top: 2rem;">', unsafe_allow_html=True)
if st.button("🔄 Recarregar Dados", type="secondary"):
    st.cache_data.clear()
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)