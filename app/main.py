"""
app/main.py
SAM Financial Model - Aplicação Streamlit Completa
Versão: 3.0 Final - Corrigida e Funcional

Substitua completamente o arquivo app/main.py pelo código abaixo.
"""

import sys
import os
from pathlib import Path
from io import BytesIO
from typing import Dict, Any, Optional

# Configuração de path
RAIZ = Path(__file__).parent.parent.absolute()
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Imports do core
try:
    from core.config import (
        ConfigFinanceira,
        criar_config_padrao,
        criar_config_com_contratacoes,
        criar_config_pessimista,
        criar_config_otimista
    )
    from core.engine import MotorProjecaoFinanceira
    from core.glossary import obter_explicacao, listar_todos_termos
    from core.visualizations import DashboardFinanceiro
except ImportError as e:
    st.error(f"❌ Erro ao importar módulos do core: {e}")
    st.stop()

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="SAM Financial Model",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def formatar_moeda(valor: float) -> str:
    """Formata valor como moeda brasileira."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_percentual(valor: float) -> str:
    """Formata valor como percentual."""
    return f"{valor*100:.1f}%"

def criar_metric_card(titulo: str, valor: str, explicacao: str = ""):
    """Cria um card de métrica com explicação."""
    st.metric(titulo, valor)
    if explicacao:
        with st.expander("ℹ️ O que significa?"):
            st.info(explicacao)

@st.cache_data
def converter_df_para_csv(df: pd.DataFrame) -> bytes:
    """Converte DataFrame para CSV."""
    return df.to_csv(index=False).encode('utf-8')

@st.cache_data
def converter_df_para_excel(df: pd.DataFrame) -> bytes:
    """Converte DataFrame para Excel."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Projecao', index=False)
    return output.getvalue()

# ============================================================================
# SIDEBAR - CONFIGURAÇÕES
# ============================================================================

st.sidebar.title("⚙️ Configurações SAM")
st.sidebar.markdown("---")

# Seleção de cenário base
st.sidebar.subheader("📋 Cenário Base")
cenario_base = st.sidebar.selectbox(
    "Escolha o cenário inicial:",
    ["Padrão (Validação)", "Com Contratações", "Pessimista", "Otimista", "Personalizado"]
)

# Carrega configuração baseada no cenário
if cenario_base == "Padrão (Validação)":
    config = criar_config_padrao()
elif cenario_base == "Com Contratações":
    config = criar_config_com_contratacoes()
elif cenario_base == "Pessimista":
    config = criar_config_pessimista()
elif cenario_base == "Otimista":
    config = criar_config_otimista()
else:  # Personalizado
    config = criar_config_padrao()

st.sidebar.markdown("---")

# ============================================================================
# PARÂMETROS PRINCIPAIS
# ============================================================================

st.sidebar.subheader("🎯 Parâmetros de Simulação")

# Horizonte
config.meses_projecao = st.sidebar.slider(
    "Meses de projeção",
    min_value=12,
    max_value=60,
    value=36,
    step=6
)

# Capital
with st.sidebar.expander("💰 Capital e Financiamento"):
    config.capital_inicial_caixa = st.number_input(
        "Capital Inicial (CAPEX)",
        value=float(config.capital_inicial_caixa),
        step=1000.0,
        format="%.2f"
    )
    config.aporte_mensal_fixo = st.number_input(
        "Aporte Mensal",
        value=float(config.aporte_mensal_fixo),
        step=100.0,
        format="%.2f"
    )
    config.meses_aporte_fixo = st.number_input(
        "Meses de Aporte",
        value=config.meses_aporte_fixo,
        step=1
    )

# Funil de Aquisição
with st.sidebar.expander("📊 Funil de Aquisição"):
    config.visitantes_mes_1 = st.number_input(
        "Visitantes Mês 1",
        value=config.visitantes_mes_1,
        step=100
    )
    config.taxa_crescimento_trafego_mensal = st.slider(
        "Crescimento Tráfego (%/mês)",
        0, 100, int(config.taxa_crescimento_trafego_mensal * 100)
    ) / 100
    config.taxa_conversao_visitante_trial = st.slider(
        "Conversão Visitante→Trial (%)",
        0, 50, int(config.taxa_conversao_visitante_trial * 100)
    ) / 100
    config.taxa_conversao_trial_pagante = st.slider(
        "Conversão Trial→Pagante (%)",
        0, 50, int(config.taxa_conversao_trial_pagante * 100)
    ) / 100
    config.churn_mensal = st.slider(
        "Churn Mensal (%)",
        0, 30, int(config.churn_mensal * 100)
    ) / 100

# Receita
with st.sidebar.expander("💵 Modelo de Receita"):
    config.preco_plano_lite = st.number_input(
        "Preço Plano Lite (R$)",
        value=float(config.preco_plano_lite),
        step=5.0
    )
    config.preco_plano_trader = st.number_input(
        "Preço Plano Trader (R$)",
        value=float(config.preco_plano_trader),
        step=5.0
    )
    config.preco_plano_pro = st.number_input(
        "Preço Plano Pro (R$)",
        value=float(config.preco_plano_pro),
        step=5.0
    )
    
    st.write("**Mix de Planos** (deve somar 100%)")
    config.mix_plano_lite = st.slider("Lite (%)", 0, 100, int(config.mix_plano_lite * 100)) / 100
    config.mix_plano_trader = st.slider("Trader (%)", 0, 100, int(config.mix_plano_trader * 100)) / 100
    config.mix_plano_pro = st.slider("Pro (%)", 0, 100, int(config.mix_plano_pro * 100)) / 100
    
    mix_total = config.mix_plano_lite + config.mix_plano_trader + config.mix_plano_pro
    if abs(mix_total - 1.0) > 0.01:
        st.warning(f"⚠️ Mix de planos soma {mix_total*100:.0f}% (deveria ser 100%)")

# Custos
with st.sidebar.expander("💸 Custos Operacionais"):
    config.custo_ia_por_usuario = st.number_input(
        "Custo IA por Usuário (R$)",
        value=float(config.custo_ia_por_usuario),
        step=0.5
    )
    config.aliquota_impostos = st.slider(
        "Alíquota Impostos (%)",
        0, 30, int(config.aliquota_impostos * 100)
    ) / 100
    config.taxa_pagamento_percentual = st.slider(
        "Taxa Pagamento (%)",
        0, 10, int(config.taxa_pagamento_percentual * 100)
    ) / 100

# Marketing
with st.sidebar.expander("📢 Marketing"):
    config.marketing_fase1_custo_fixo = st.number_input(
        "Marketing Fase 1 (R$/mês)",
        value=float(config.marketing_fase1_custo_fixo),
        step=100.0
    )
    config.marketing_fase1_duracao_meses = st.number_input(
        "Duração Fase 1 (meses)",
        value=config.marketing_fase1_duracao_meses,
        step=1
    )
    config.marketing_fase2_perc_lucro_bruto = st.slider(
        "Marketing Fase 2 (% Lucro Bruto)",
        0, 50, int(config.marketing_fase2_perc_lucro_bruto * 100)
    ) / 100

st.sidebar.markdown("---")

# Botão de execução
executar = st.sidebar.button("🚀 RODAR SIMULAÇÃO", type="primary", use_container_width=True)

# ============================================================================
# ÁREA PRINCIPAL
# ============================================================================

st.title("💰 SAM Financial Model")
st.markdown("### Simulador Financeiro Completo para SaaS")

# Tabs principais
tab_dashboard, tab_tabelas, tab_kpis, tab_cenarios, tab_glossario = st.tabs([
    "📊 Dashboard",
    "📋 Tabelas Detalhadas",
    "🎯 KPIs e Métricas",
    "🔄 Análise de Cenários",
    "📚 Glossário"
])

# ============================================================================
# EXECUÇÃO DA SIMULAÇÃO
# ============================================================================

if executar or 'df_projecao' not in st.session_state:
    with st.spinner("🔄 Executando simulação..."):
        try:
            # Executa motor
            motor = MotorProjecaoFinanceira(config)
            df = motor.executar_projecao(meses=config.meses_projecao)
            kpis = motor.calcular_kpis()
            
            # Salva no session_state
            st.session_state.df_projecao = df
            st.session_state.kpis = kpis
            st.session_state.config = config
            
            st.success("✅ Simulação concluída com sucesso!")
            
        except Exception as e:
            st.error(f"❌ Erro na simulação: {str(e)}")
            st.exception(e)
            st.stop()

# Recupera dados
if 'df_projecao' in st.session_state:
    df = st.session_state.df_projecao
    kpis = st.session_state.kpis
    config = st.session_state.config
else:
    st.info("👈 Configure os parâmetros na barra lateral e clique em 'RODAR SIMULAÇÃO'")
    st.stop()

# ============================================================================
# TAB 1: DASHBOARD
# ============================================================================

with tab_dashboard:
    st.header("📊 Dashboard Executivo")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        mrr_final = df['MRR'].iloc[-1]
        criar_metric_card(
            "💰 MRR Final",
            formatar_moeda(mrr_final),
            obter_explicacao("MRR", "layman")
        )
    
    with col2:
        usuarios_final = df['Usuarios_Finais'].iloc[-1]
        criar_metric_card(
            "👥 Usuários",
            f"{int(usuarios_final):,}",
            "Número total de clientes pagantes ativos no último mês"
        )
    
    with col3:
        caixa_final = df['Saldo_Caixa'].iloc[-1]
        criar_metric_card(
            "💵 Caixa Final",
            formatar_moeda(caixa_final),
            obter_explicacao("Caixa", "layman")
        )
    
    with col4:
        ltv_cac = kpis.get('LTV_CAC_Ratio_Final', 0)
        criar_metric_card(
            "🎯 LTV/CAC",
            f"{ltv_cac:.2f}x",
            obter_explicacao("LTV_CAC_Ratio", "layman")
        )
    
    st.markdown("---")
    
    # Gráficos principais
    col_grafico1, col_grafico2 = st.columns(2)
    
    with col_grafico1:
        st.subheader("📈 Evolução do MRR")
        fig_mrr = px.area(
            df,
            x='mes',
            y='MRR',
            title="Receita Recorrente Mensal",
            labels={'mes': 'Mês', 'MRR': 'MRR (R$)'}
        )
        fig_mrr.update_traces(line_color='#2E86AB')
        st.plotly_chart(fig_mrr, use_container_width=True)
    
    with col_grafico2:
        st.subheader("💰 Saldo de Caixa")
        fig_caixa = go.Figure()
        fig_caixa.add_trace(go.Scatter(
            x=df['mes'],
            y=df['Saldo_Caixa'],
            fill='tozeroy',
            name='Caixa',
            line_color='#06A77D'
        ))
        fig_caixa.add_hline(y=0, line_dash="dash", line_color="red")
        fig_caixa.update_layout(
            title="Evolução do Saldo de Caixa",
            xaxis_title="Mês",
            yaxis_title="R$"
        )
        st.plotly_chart(fig_caixa, use_container_width=True)
    
    st.markdown("---")
    
    # Gráfico de composição de custos
    st.subheader("💸 Composição de Custos (OPEX)")
    
    custos_cols = ['Custo_Infra', 'Custo_Marketing', 'Custo_Pessoal_CLT', 
                   'Custo_Pessoal_PJ', 'Custo_Ferramentas']
    custos_disponiveis = [c for c in custos_cols if c in df.columns]
    
    if custos_disponiveis:
        fig_custos = px.area(
            df,
            x='mes',
            y=custos_disponiveis,
            title="Principais Componentes de OPEX",
            labels={'value': 'R$', 'variable': 'Categoria'}
        )
        st.plotly_chart(fig_custos, use_container_width=True)
    
    # Gráfico de usuários
    st.subheader("👥 Crescimento de Usuários")
    fig_usuarios = go.Figure()
    fig_usuarios.add_trace(go.Bar(
        x=df['mes'],
        y=df['Novos_Pagantes'],
        name='Novos Pagantes'
    ))
    fig_usuarios.add_trace(go.Scatter(
        x=df['mes'],
        y=df['Usuarios_Finais'],
        name='Total Acumulado',
        yaxis='y2'
    ))
    fig_usuarios.update_layout(
        title="Aquisição e Base Total de Usuários",
        xaxis_title="Mês",
        yaxis_title="Novos Pagantes",
        yaxis2=dict(title="Total Acumulado", overlaying='y', side='right')
    )
    st.plotly_chart(fig_usuarios, use_container_width=True)

# ============================================================================
# TAB 2: TABELAS DETALHADAS
# ============================================================================

with tab_tabelas:
    st.header("📋 Tabelas Detalhadas")
    
    # Filtros
    col_filtro1, col_filtro2 = st.columns(2)
    with col_filtro1:
        mes_inicio = st.slider("Mês Início", 1, len(df), 1)
    with col_filtro2:
        mes_fim = st.slider("Mês Fim", mes_inicio, len(df), len(df))
    
    df_filtrado = df[(df['mes'] >= mes_inicio) & (df['mes'] <= mes_fim)]
    
    # Tabela de Projeção Completa
    st.subheader("📊 Projeção Mensal Completa")
    st.dataframe(df_filtrado, use_container_width=True)
    
    # Downloads
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        csv = converter_df_para_csv(df)
        st.download_button(
            "📥 Baixar CSV",
            csv,
            "projecao_sam.csv",
            "text/csv",
            use_container_width=True
        )
    with col_dl2:
        excel = converter_df_para_excel(df)
        st.download_button(
            "📥 Baixar Excel",
            excel,
            "projecao_sam.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    st.markdown("---")
    
    # DRE Simplificado
    st.subheader("📑 DRE Simplificado")
    dre = df[['mes', 'MRR', 'COGS_Total', 'Lucro_Bruto', 
              'OPEX_Total', 'Resultado_Operacional']].copy()
    dre.columns = ['Mês', 'Receita', 'COGS', 'Lucro Bruto', 'OPEX', 'Resultado']
    st.dataframe(dre, use_container_width=True)

# ============================================================================
# TAB 3: KPIs E MÉTRICAS
# ============================================================================

with tab_kpis:
    st.header("🎯 KPIs e Métricas-Chave")
    
    # Unit Economics
    st.subheader("💎 Unit Economics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ltv = kpis.get('LTV_Final', 0)
        st.metric("LTV (Lifetime Value)", formatar_moeda(ltv))
        with st.expander("ℹ️ Explicação"):
            st.info(obter_explicacao("LTV", "executive"))
    
    with col2:
        cac = kpis.get('CAC_Medio_Periodo', 0)
        st.metric("CAC (Custo de Aquisição)", formatar_moeda(cac))
        with st.expander("ℹ️ Explicação"):
            st.info(obter_explicacao("CAC", "executive"))
    
    with col3:
        payback = kpis.get('CAC_Payback_Meses_Config', 0)
        st.metric("CAC Payback", f"{payback:.1f} meses")
        with st.expander("ℹ️ Explicação"):
            st.info(obter_explicacao("CAC_Payback", "executive"))
    
    st.markdown("---")
    
    # Viabilidade
    st.subheader("💼 Viabilidade Financeira")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        be_mes = kpis.get('Break_Even_Mes', 'N/A')
        st.metric("Break-Even", f"Mês {be_mes}" if be_mes != 'N/A' else "N/A")
    
    with col2:
        vale = kpis.get('Vale_da_Morte_Minimo_Caixa', 0)
        st.metric("Vale da Morte", formatar_moeda(vale))
    
    with col3:
        runway = kpis.get('Runway_Meses', 0)
        st.metric("Runway", f"{runway} meses" if isinstance(runway, int) else str(runway))
    
    st.markdown("---")
    
    # Snapshots Anuais
    st.subheader("📸 Snapshots Anuais")
    
    anos_data = []
    for ano in [1, 2, 3]:
        mrr_key = f'MRR_Ano{ano}'
        users_key = f'Usuarios_Ano{ano}'
        if mrr_key in kpis:
            anos_data.append({
                'Ano': ano,
                'MRR': formatar_moeda(kpis[mrr_key]),
                'Usuários': int(kpis.get(users_key, 0))
            })
    
    if anos_data:
        df_anos = pd.DataFrame(anos_data)
        st.table(df_anos)

# ============================================================================
# TAB 4: ANÁLISE DE CENÁRIOS
# ============================================================================

with tab_cenarios:
    st.header("🔄 Análise de Cenários")
    st.info("🚧 Funcionalidade de comparação de múltiplos cenários em desenvolvimento")
    
    st.markdown("""
    Esta seção permitirá:
    - Comparar cenários Base, Otimista e Pessimista lado a lado
    - Análise de sensibilidade (variação de parâmetros)
    - Monte Carlo com 500+ simulações
    - Fan charts de incerteza
    """)

# ============================================================================
# TAB 5: GLOSSÁRIO
# ============================================================================

with tab_glossario:
    st.header("📚 Glossário Financeiro")
    
    termos = listar_todos_termos()
    termo_selecionado = st.selectbox(
        "Escolha um termo para ver a explicação:",
        termos
    )
    
    if termo_selecionado:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 Explicação para Leigos")
            st.info(obter_explicacao(termo_selecionado, "layman"))
        
        with col2:
            st.subheader("💼 Explicação Executiva")
            st.info(obter_explicacao(termo_selecionado, "executive"))
        
        st.subheader("📊 Explicação para Investidores")
        st.success(obter_explicacao(termo_selecionado, "investor"))

# ============================================================================
# RODAPÉ
# ============================================================================

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "SAM Financial Model v3.0 | Powered by Streamlit + Claude"
    "</div>",
    unsafe_allow_html=True
)