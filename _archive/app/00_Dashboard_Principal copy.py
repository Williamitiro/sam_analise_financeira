"""
app/00_Dashboard_Principal.py
SAM Financial Model - Aplicação Streamlit Principal (Pós-Refatoração UX)
Versão: 6.0 - Dashboard Interativo

Este arquivo agora é o centro de controle interativo para simulações rápidas.
A configuração detalhada e estrutural fica em `app/pages/99_Configuracoes.py`.
"""

import sys
from pathlib import Path
from io import BytesIO

# Configuração de path
RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.append(str(RAIZ))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Imports do core
try:
    from core.engine import MotorProjecaoFinanceira
    from core.glossary import obter_explicacao, listar_todos_termos
    from core.config import (
        criar_config_padrao,
        criar_config_com_contratacoes,
        criar_config_pessimista,
        criar_config_otimista
    )
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
    if not isinstance(valor, (int, float)):
        return "N/A"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def criar_metric_card(titulo: str, valor: str, explicacao: str = ""):
    st.metric(titulo, valor)
    if explicacao:
        with st.expander("ℹ️ O que significa?"):
            st.info(explicacao)

@st.cache_data
def converter_df_para_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode('utf-8')

@st.cache_data
def converter_df_para_excel(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Projecao', index=False)
    return output.getvalue()

# ============================================================================
# SIDEBAR - CONTROLES GLOBAIS
# ============================================================================

st.sidebar.title("Controles SAM")
st.sidebar.markdown("Use a página 'Configurações' para customizar o modelo em detalhes.")
st.sidebar.markdown("---")
executar_sidebar = st.sidebar.button("🚀 RODAR SIMULAÇÃO", type="primary", use_container_width=True)

# ============================================================================
# ÁREA PRINCIPAL
# ============================================================================

st.title("💰 SAM Financial Model")
st.markdown("### Simulador Financeiro Completo para SaaS")

# --- FLUXO DE EXECUÇÃO ---

executar_main = False
# 1. Se nenhuma simulação foi feita, mostra a tela de boas-vindas para o "caminho rápido"
if 'df_projecao' not in st.session_state:
    
    st.header("🏁 Comece por aqui: Gere sua primeira projeção")
    st.markdown("Selecione um cenário base, ajuste os parâmetros principais e gere sua projeção.")

    col1, col2 = st.columns([2, 1])
    with col1:
        cenario_base = st.selectbox(
            "Escolha o cenário inicial:",
            ["Padrão (Validação)", "Com Contratações", "Pessimista", "Otimista"],
            key="cenario_selecionado_main"
        )
    
    # Carrega a configuração inicial no estado da sessão se ainda não foi carregada ou se mudou
    if 'cenario_carregado' not in st.session_state or st.session_state.cenario_carregado != cenario_base:
        if cenario_base == "Padrão (Validação)":
            config = criar_config_padrao()
        elif cenario_base == "Com Contratações":
            config = criar_config_com_contratacoes()
        elif cenario_base == "Pessimista":
            config = criar_config_pessimista()
        else: # Otimista
            config = criar_config_otimista()
        st.session_state.config = config
        st.session_state.cenario_carregado = cenario_base

    config = st.session_state.config

    with col2:
        st.write("")
        st.write("")
        executar_main = st.button("Gerar Projeção", type="primary", use_container_width=True)

    st.markdown("---")
    st.subheader("🔬 Ajuste Fino das Premissas do Cenário")

    col_param1, col_param2, col_param3 = st.columns(3)
    with col_param1:
        with st.expander("📈 Aquisição", expanded=True):
            config.taxa_crescimento_trafego_mensal = st.slider("Cresc. Tráfego Mensal (%)", 0, 100, int(config.taxa_crescimento_trafego_mensal * 100), help="Taxa de crescimento de novos visitantes ao seu site a cada mês.") / 100
            config.taxa_conversao_trial_pagante = st.slider("Conversão Trial → Pagante (%)", 0, 100, int(config.taxa_conversao_trial_pagante * 100), help="Percentual de usuários em período de teste que se tornam clientes pagantes.") / 100
    with col_param2:
        with st.expander("📉 Retenção", expanded=True):
            config.churn_mensal = st.slider("Churn Mensal (%)", 0, 20, int(config.churn_mensal * 100), help="Taxa de cancelamento de clientes a cada mês.") / 100
            config.cac_pago_meta = st.number_input("CAC Meta (R$)", value=config.cac_pago_meta, step=50.0, help="Custo de Aquisição de Cliente: quanto você gasta em marketing para adquirir um novo cliente.")
    with col_param3:
        with st.expander("💵 Monetização", expanded=True):
            config.arpu_medio_override = st.number_input("ARPU Médio (R$)", value=config.arpu_medio, step=5.0, key="arpu_override", help="Receita Média Por Usuário. Altere aqui para um ajuste rápido ou ajuste os preços dos planos na página de Configurações.")

    if hasattr(config, 'cargos_planejados') and config.cargos_planejados:
        with st.expander("👥 Regras de Contratação do Cenário"):
            for cargo in config.cargos_planejados:
                gatilho_str = ", ".join(str(g) for g in cargo.gatilhos_contratacao) if cargo.gatilhos_contratacao else f"no mês {cargo.mes_contratacao_manual}"
                st.text(f"- Contratar {cargo.cargo_funcao} (R$ {cargo.salario_base:,.0f}) quando: {gatilho_str}")
            st.caption("Para adicionar ou remover cargos, use a página 'Configurações'.")

# 2. Lógica de execução quando o botão é pressionado
if executar_main or executar_sidebar:
    if 'config' not in st.session_state:
        st.error("❌ Nenhuma configuração encontrada. Por favor, selecione um cenário base acima.")
        st.stop()

    with st.spinner("🔄 Executando simulação com as configurações atuais..."):
        try:
            config_atual = st.session_state.config
            if not hasattr(config_atual, 'meses_projecao'):
                config_atual.meses_projecao = 36

            motor = MotorProjecaoFinanceira(config_atual)
            df = motor.executar_projecao(meses=config_atual.meses_projecao)
            kpis = motor.calcular_kpis()
            
            st.session_state.df_projecao = df
            st.session_state.kpis = kpis
            
            st.success("✅ Simulação concluída com sucesso!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Erro na simulação: {str(e)}")
            st.exception(e)

# 3. Se a simulação já foi feita, mostra os dashboards
if 'df_projecao' in st.session_state and 'kpis' in st.session_state:
    df = st.session_state.df_projecao
    kpis = st.session_state.kpis

    st.markdown("---")
    # Filtro de período global
    max_mes = len(df)
    periodo_selecionado = st.slider(
        "Selecione o Período de Análise (Meses)",
        1, max_mes, (1, max_mes)
    )
    df_filtrado = df[(df['mes'] >= periodo_selecionado[0]) & (df['mes'] <= periodo_selecionado[1])]

    tab_dashboard, tab_tabelas, tab_kpis, tab_cenarios, tab_glossario = st.tabs([
        "📊 Dashboard", "📋 Tabelas Detalhadas", "🎯 KPIs e Métricas",
        "🔄 Análise de Cenários", "📚 Glossário"
    ])

    with tab_dashboard:
        st.header("📊 Dashboard Executivo")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            mrr_final = df_filtrado['MRR'].iloc[-1]
            criar_metric_card("💰 MRR (Final do Período)", formatar_moeda(mrr_final), obter_explicacao("MRR", "layman"))
        with col2:
            usuarios_final = df_filtrado['Usuarios_Finais'].iloc[-1]
            criar_metric_card("👥 Usuários (Final do Período)", f"{int(usuarios_final):,}", "Número total de clientes pagantes ativos")
        with col3:
            caixa_final = df_filtrado['Saldo_Caixa'].iloc[-1]
            criar_metric_card("💵 Caixa (Final do Período)", formatar_moeda(caixa_final), obter_explicacao("Caixa", "layman"))
        with col4:
            ltv_cac = kpis.get('LTV_CAC_Ratio_Final', 0)
            criar_metric_card("🎯 LTV/CAC (Geral)", f"{ltv_cac:.2f}x", obter_explicacao("LTV_CAC_Ratio", "layman"))
        
        st.markdown("---")
        col_grafico1, col_grafico2 = st.columns(2)
        with col_grafico1:
            st.subheader("📈 Evolução do MRR")
            fig_mrr = px.area(df_filtrado, x='mes', y='MRR', title="Receita Recorrente Mensal")
            st.plotly_chart(fig_mrr, use_container_width=True)
        with col_grafico2:
            st.subheader("💰 Saldo de Caixa")
            fig_caixa = go.Figure(go.Scatter(x=df_filtrado['mes'], y=df_filtrado['Saldo_Caixa'], fill='tozeroy'))
            fig_caixa.add_hline(y=0, line_dash="dash", line_color="red")
            st.plotly_chart(fig_caixa, use_container_width=True)

    with tab_tabelas:
        st.header("📋 Tabelas Detalhadas")
        st.markdown("Analise os números detalhados por área de negócio.")
        
        tabela_funil, tabela_saas, tabela_caixa = st.tabs(["Funil de Aquisição", "Métricas SaaS", "Fluxo de Caixa"])
        
        with tabela_funil:
            cols_funil = ['mes', 'Visitantes', 'Trials', 'Novos_Pagantes', 'Taxa_Conversao_Geral']
            st.dataframe(df_filtrado[cols_funil], use_container_width=True)
            
        with tabela_saas:
            cols_saas = ['mes', 'Usuarios_Iniciais', 'Novos_Pagantes', 'Churn_Absoluto', 'Usuarios_Finais', 'MRR', 'ARPU']
            st.dataframe(df_filtrado[cols_saas], use_container_width=True)
            
        with tabela_caixa:
            cols_caixa = ['mes', 'Receita_Total', 'COGS_Total', 'OPEX_Total', 'Resultado_Operacional', 'Aportes', 'Saldo_Caixa']
            st.dataframe(df_filtrado[cols_caixa], use_container_width=True)

    with tab_kpis:
        st.header("🎯 KPIs e Métricas-Chave")
        st.subheader("💎 Unit Economics")
        col1, col2, col3 = st.columns(3)
        with col1:
            ltv = kpis.get('LTV_Final', 0)
            st.metric("LTV (Lifetime Value)", formatar_moeda(ltv))
        with col2:
            cac = kpis.get('CAC_Medio_Periodo', 0)
            st.metric("CAC (Custo de Aquisição)", formatar_moeda(cac))
        with col3:
            payback = kpis.get('CAC_Payback_Meses_Config', 0)
            st.metric("CAC Payback", f"{payback:.1f} meses")
        
        st.markdown("---")
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

    with tab_cenarios:
        st.header("🔄 Análise de Cenários")
        st.info("🚧 Em desenvolvimento")

    with tab_glossario:
        st.header("📚 Glossário Financeiro")
        termos = listar_todos_termos()
        termo_selecionado = st.selectbox("Escolha um termo:", termos)
        if termo_selecionado:
            st.info(obter_explicacao(termo_selecionado, "layman"))

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>SAM Financial Model v6.0</div>", unsafe_allow_html=True)