import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto ao sys.path
RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.append(str(RAIZ))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Importações do projeto
from core.config import (
    ConfigFinanceira,
    criar_config_padrao,
    criar_config_com_contratacoes,
    criar_config_pessimista,
    criar_config_otimista
)
from core.engine import MotorProjecaoFinanceira
from core.analytics.insights_engine import InsightsEngine, AlertLevel
from core.builders.revenue_builder import criar_estrategia_sam_revenue
from core.builders.channels_builder import criar_estrategia_sam_canais
from core.builders.capital_builder import criar_estrategia_sam_capital
from core.builders.team_builder import criar_equipe_sam

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="SAM Financial Model",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Customizado para UI profissional
st.markdown("""
<style>
    /* Header Principal */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    
    /* Cards de Alerta */
    .alert-critical {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #ffaa00 0%, #ff8800 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .alert-success {
        background: linear-gradient(135deg, #00c851 0%, #007e33 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Métric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def formatar_moeda(valor):
    """Formata valor em reais"""
    if pd.isna(valor):
        return "N/A"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_percentual(valor):
    """Formata valor como percentual"""
    if pd.isna(valor):
        return "N/A"
    return f"{valor:.1f}%"

def calcular_delta(atual, anterior):
    """Calcula variação percentual"""
    if anterior == 0 or pd.isna(anterior) or pd.isna(atual):
        return None
    return ((atual - anterior) / anterior) * 100

def criar_sparkline(valores):
    """Cria mini gráfico de linha"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=valores,
        mode='lines',
        line=dict(color='#1f77b4', width=2),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.1)'
    ))
    fig.update_layout(
        height=80,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def renderizar_alerta(alerta):
    """Renderiza um card de alerta"""
    if alerta.level == AlertLevel.CRITICAL:
        css_class = "alert-critical"
        icon = "🔴"
    elif alerta.level == AlertLevel.WARNING:
        css_class = "alert-warning"
        icon = "🟡"
    elif alerta.level == AlertLevel.SUCCESS:
        css_class = "alert-success"
        icon = "🟢"
    else:
        css_class = "alert-info"
        icon = "🔵"
    
    html = f"""
    <div class="{css_class}">
        <div style="display: flex; align-items: center;">
            <div style="font-size: 2rem; margin-right: 1rem;">{icon}</div>
            <div style="flex: 1;">
                <div style="font-size: 1.2rem; font-weight: 600;">{alerta.title}</div>
                <div style="margin: 0.5rem 0;">{alerta.description}</div>
                {f'<div style="font-size: 0.9rem; opacity: 0.9;">💡 Ação: {alerta.action}</div>' if alerta.action else ''}
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

# Inicializa session state
if 'config' not in st.session_state:
    st.session_state.config = ConfigFinanceira()

if 'df_projecao' not in st.session_state:
    st.session_state.df_projecao = None

if 'kpis' not in st.session_state:
    st.session_state.kpis = None

if 'insights' not in st.session_state:
    st.session_state.insights = None

# ============================================================================
# SIDEBAR - FILTROS GLOBAIS
# ============================================================================

with st.sidebar:
    st.markdown("## 🎛️ Controles")
    
    # Botão de recálculo
    if st.button("▶️ Executar Projeção", type="primary", use_container_width=True):
        with st.spinner("Calculando projeção..."):
            motor = MotorProjecaoFinanceira(st.session_state.config)
            st.session_state.df_projecao = motor.executar_projecao(meses=36)
            st.session_state.kpis = motor.calcular_kpis()
            
            # Gera insights
            if st.session_state.df_projecao is not None:
                insights_engine = InsightsEngine(
                    st.session_state.df_projecao,
                    st.session_state.kpis,
                    st.session_state.config
                )
                st.session_state.insights = insights_engine.generate_all()
        
        st.success("✅ Projeção calculada!")
        st.rerun()
    
    st.markdown("---")
    
    # Filtros de período
    st.markdown("### 📅 Período de Análise")
    if st.session_state.df_projecao is not None:
        max_mes = len(st.session_state.df_projecao)
        mes_inicio = st.slider("Mês inicial", 1, max_mes, 1)
        mes_fim = st.slider("Mês final", mes_inicio, max_mes, min(max_mes, 36))
        st.session_state.filtro_periodo = (mes_inicio, mes_fim)
    
    st.markdown("---")
    
    # Info do modelo
    st.markdown("### ℹ️ Informações")
    st.caption(f"**Versão:** 4.0")
    st.caption(f"**Engine:** Integrado com Builders")
    st.caption(f"**Última execução:** {pd.Timestamp.now().strftime('%H:%M:%S')}")

# ============================================================================
# CORPO PRINCIPAL
# ============================================================================

# Header
st.markdown('<div class="main-header">📊 SAM Financial Model</div>', unsafe_allow_html=True)
st.markdown("**Centro de Comando Estratégico** - Projeções, Análises e Insights")

# Verifica se há projeção
if 'df_projecao' not in st.session_state or st.session_state.df_projecao is None:
    
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
        st.rerun()

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
            config.churn_mensal = st.slider("Churn Mensal (%)", 0.0, 20.0, float(config.churn_mensal * 100), help="Taxa de cancelamento de clientes a cada mês.") / 100
            config.cac_pago_meta = st.number_input("CAC Meta (R$)", value=config.cac_pago_meta, step=50.0, help="Custo de Aquisição de Cliente: quanto você gasta em marketing para adquirir um novo cliente.")
    with col_param3:
        with st.expander("💵 Monetização", expanded=True):
            arpu_value = config.arpu_medio_override if config.arpu_medio_override is not None else config.arpu_medio
            config.arpu_medio_override = st.number_input("ARPU Médio (R$)", value=float(arpu_value), step=5.0, key="arpu_override", help="Receita Média Por Usuário. Altere aqui para um ajuste rápido ou ajuste os preços dos planos na página de Configurações.")

    if executar_main:
        with st.spinner("🔄 Executando simulação com as configurações atuais..."):
            try:
                config_atual = st.session_state.config
                
                # Garante que os builders sejam aplicados à configuração antes de rodar
                config = criar_estrategia_sam_revenue(config_atual).build()
                config = criar_estrategia_sam_canais(config).build()
                config = criar_estrategia_sam_capital(config).build()
                config = criar_equipe_sam(config).build()
                
                st.session_state.config = config

                motor = MotorProjecaoFinanceira(config)
                df = motor.executar_projecao(meses=36)
                kpis = motor.calcular_kpis()
                
                st.session_state.df_projecao = df
                st.session_state.kpis = kpis
                
                st.success("✅ Simulação concluída com sucesso!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erro na simulação: {str(e)}")
                st.exception(e)
else:
    # Aplica filtros
    df = st.session_state.df_projecao.copy()
    kpis = st.session_state.kpis
    insights = st.session_state.get('insights', {})

    if 'filtro_periodo' in st.session_state:
        mes_inicio, mes_fim = st.session_state.filtro_periodo
        df = df[(df['mes'] >= mes_inicio) & (df['mes'] <= mes_fim)]

    # ============================================================================
    # SEÇÃO 1: ALERTAS CRÍTICOS
    # ============================================================================

    if insights and 'alertas' in insights and insights['alertas']:
        st.markdown('<div class="section-header">⚠️ Alertas Críticos</div>', unsafe_allow_html=True)
        
        # Agrupa por nível de severidade
        alertas_criticos = [a for a in insights['alertas'] if a.level == AlertLevel.CRITICAL]
        alertas_warning = [a for a in insights['alertas'] if a.level == AlertLevel.WARNING]
        
        if alertas_criticos:
            st.markdown("### 🔴 Crítico")
            for alerta in alertas_criticos[:3]:  # Mostra no máximo 3
                renderizar_alerta(alerta)
        
        if alertas_warning:
            st.markdown("### 🟡 Atenção")
            for alerta in alertas_warning[:2]:  # Mostra no máximo 2
                renderizar_alerta(alerta)

    # ============================================================================
    # SEÇÃO 2: KPIs PRINCIPAIS
    # ============================================================================

    st.markdown('<div class="section-header">🎯 Métricas Principais</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    # MRR
    with col1:
        mrr_atual = df.iloc[-1]['MRR']
        mrr_anterior = df.iloc[-2]['MRR'] if len(df) > 1 else None
        delta_mrr = calcular_delta(mrr_atual, mrr_anterior)
        
        st.metric(
            label="💰 MRR",
            value=formatar_moeda(mrr_atual),
            delta=f"{delta_mrr:+.1f}%" if delta_mrr else None
        )
        st.plotly_chart(criar_sparkline(df['MRR'].tail(12).values), use_container_width=True)

    # Usuários
    with col2:
        usuarios_atual = df.iloc[-1]['Usuarios_Finais']
        usuarios_anterior = df.iloc[-2]['Usuarios_Finais'] if len(df) > 1 else None
        delta_usuarios = calcular_delta(usuarios_atual, usuarios_anterior)
        
        st.metric(
            label="👥 Usuários Pagantes",
            value=f"{int(usuarios_atual):,}".replace(",", "."),
            delta=f"{delta_usuarios:+.1f}%" if delta_usuarios else None
        )
        st.plotly_chart(criar_sparkline(df['Usuarios_Finais'].tail(12).values), use_container_width=True)

    # Caixa
    with col3:
        caixa_atual = df.iloc[-1]['Saldo_Caixa']
        caixa_anterior = df.iloc[-2]['Saldo_Caixa'] if len(df) > 1 else None
        delta_caixa = caixa_atual - caixa_anterior if caixa_anterior is not None else None
        
        st.metric(
            label="💵 Saldo de Caixa",
            value=formatar_moeda(caixa_atual),
            delta=formatar_moeda(delta_caixa) if delta_caixa else None
        )
        st.plotly_chart(criar_sparkline(df['Saldo_Caixa'].tail(12).values), use_container_width=True)

    # LTV/CAC
    with col4:
        ltv_cac = kpis.get('LTV_CAC_Ratio_Final', 0)
        
        # Cor baseada no valor
        if ltv_cac >= 5:
            cor = "🟢"
        elif ltv_cac >= 3:
            cor = "🟡"
        else:
            cor = "🔴"
        
        st.metric(
            label=f"{cor} LTV/CAC Ratio",
            value=f"{ltv_cac:.1f}x" if not pd.isna(ltv_cac) else "N/A",
            delta="Excelente" if ltv_cac >= 5 else ("Bom" if ltv_cac >= 3 else "Ruim")
        )

    # ============================================================================
    # SEÇÃO 3: MARCOS IMPORTANTES
    # ============================================================================

    st.markdown('<div class="section-header">🎯 Marcos e Metas</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🎊 Break-Even")
        break_even = kpis.get('Break_Even_Mes')
        if break_even and break_even != 'N/A':
            st.success(f"**Mês {break_even}**")
            meses_restantes = break_even - len(df)
            if meses_restantes > 0:
                st.caption(f"Faltam {meses_restantes} meses")
            else:
                st.caption("✅ Atingido!")
        else:
            st.warning("Não projetado no período")

    with col2:
        st.markdown("### 💀 Vale da Morte")
        vale_mes = kpis.get('Vale_da_Morte_Mes', 0)
        vale_valor = kpis.get('Vale_da_Morte_Minimo_Caixa', 0)
        
        if vale_valor < 0:
            st.error(f"**Mês {vale_mes}**")
            st.caption(f"Caixa mínimo: {formatar_moeda(vale_valor)}")
        else:
            st.success("✅ Sem vale da morte")

    with col3:
        st.markdown("### 🛣️ Runway")
        runway = kpis.get('Runway_Meses', 'N/A')
        
        if isinstance(runway, int):
            if runway < 6:
                st.error(f"**{runway} meses**")
                st.caption("⚠️ Crítico")
            elif runway < 12:
                st.warning(f"**{runway} meses**")
                st.caption("🟡 Atenção")
            else:
                st.success(f"**{runway} meses**")
                st.caption("✅ Saudável")
        else:
            st.success(f"**{runway}**")
            st.caption("✅ Positivo em todo período")

    # ============================================================================
    # SEÇÃO 4: GRÁFICO PRINCIPAL - TRAJETÓRIA FINANCEIRA
    # ============================================================================

    st.markdown('<div class="section-header">📈 Trajetória Financeira</div>', unsafe_allow_html=True)

    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        subplot_titles=("Receita, Custos e Resultado", "Fluxo de Caixa"),
        vertical_spacing=0.12
    )

    # Gráfico 1: Receita vs Custos
    fig.add_trace(
        go.Scatter(
            x=df['mes'], y=df['MRR'],
            name='MRR',
            line=dict(color='#00c851', width=3),
            fill='tozeroy'
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['mes'], y=df['OPEX_Total'],
            name='OPEX Total',
            line=dict(color='#ff4444', width=2, dash='dot')
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['mes'], y=df['Resultado_Operacional'],
            name='Resultado Operacional',
            line=dict(color='#1f77b4', width=2)
        ),
        row=1, col=1
    )

    # Gráfico 2: Fluxo de Caixa
    cores_caixa = ['#00c851' if x >= 0 else '#ff4444' for x in df['Saldo_Caixa']]
    fig.add_trace(
        go.Bar(
            x=df['mes'], y=df['Saldo_Caixa'],
            name='Saldo de Caixa',
            marker_color=cores_caixa
        ),
        row=2, col=1
    )

    # Layout
    fig.update_xaxes(title_text="Mês", row=2, col=1)
    fig.update_yaxes(title_text="R$", row=1, col=1)
    fig.update_yaxes(title_text="R$", row=2, col=1)

    fig.update_layout(
        height=700,
        showlegend=True,
        hovermode='x unified',
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)

    # ============================================================================
    # SEÇÃO 5: UNIT ECONOMICS
    # ============================================================================

    st.markdown('<div class="section-header">💎 Unit Economics</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        arpu = df.iloc[-1]['ARPU']
        st.metric("ARPU", formatar_moeda(arpu))

    with col2:
        ltv = kpis.get('LTV_Final', 0)
        st.metric("LTV", formatar_moeda(ltv))

    with col3:
        cac = kpis.get('CAC_Medio_Periodo', 0)
        st.metric("CAC Médio", formatar_moeda(cac))

    with col4:
        payback = kpis.get('CAC_Payback_Meses_Config', 0)
        st.metric("Payback", f"{payback:.1f} meses" if not pd.isna(payback) else "N/A")

    # Gráfico de decomposição LTV
    st.markdown("#### 📊 Decomposição do LTV")

    arpu_valor = df.iloc[-1]['ARPU']
    margem_bruta_pct = df.iloc[-1]['Margem_Bruta_Pct'] / 100
    lifetime_meses = 1 / st.session_state.config.churn_mensal
    margem_mensal = arpu_valor * margem_bruta_pct
    ltv_calculado = margem_mensal * lifetime_meses

    fig_ltv = go.Figure()

    fig_ltv.add_trace(go.Waterfall(
        name="LTV",
        orientation="h",
        measure=["absolute", "relative", "relative", "total"],
        y=["ARPU", "- COGS", "× Lifetime", "= LTV"],
        x=[arpu_valor, -arpu_valor * (1-margem_bruta_pct), margem_mensal * (lifetime_meses-1), ltv_calculado],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))

    fig_ltv.update_layout(
        height=300,
        showlegend=False,
        xaxis_title="R$"
    )

    st.plotly_chart(fig_ltv, use_container_width=True)

    # ============================================================================
    # SEÇÃO 6: TABELA RESUMO
    # ============================================================================

    st.markdown('<div class="section-header">📋 Resumo Mês a Mês</div>', unsafe_allow_html=True)

    # Seletor de colunas
    colunas_disponiveis = {
        'Funil': ['mes', 'Visitantes', 'Novos_Trials', 'Novos_Pagantes', 'Usuarios_Finais'],
        'Receita': ['mes', 'MRR', 'ARR', 'ARPU', 'Lucro_Bruto', 'Margem_Bruta_Pct'],
        'Custos': ['mes', 'COGS_Total', 'OPEX_Total', 'Custo_Marketing', 'Custo_Pessoal_CLT', 'Custo_Infra'],
        'Resultado': ['mes', 'Resultado_Operacional', 'EBITDA', 'Fluxo_Caixa', 'Saldo_Caixa'],
        'Métricas': ['mes', 'CAC_Mensal', 'LTV', 'LTV_CAC_Ratio', 'Taxa_Conv_Geral']
    }

    col1, col2 = st.columns([1, 3])

    with col1:
        tipo_tabela = st.selectbox(
            "Tipo de Tabela",
            list(colunas_disponiveis.keys())
        )

    cols_exibir = colunas_disponiveis[tipo_tabela]

    # Formata DataFrame
    df_display = df[cols_exibir].copy()

    # Renomeia colunas para português
    nomes_colunas = {
        'mes': 'Mês',
        'Visitantes': 'Visitantes',
        'Novos_Trials': 'Trials',
        'Novos_Pagantes': 'Novos Pagantes',
        'Usuarios_Finais': 'Usuários',
        'MRR': 'MRR',
        'ARR': 'ARR',
        'ARPU': 'ARPU',
        'Lucro_Bruto': 'Lucro Bruto',
        'Margem_Bruta_Pct': 'Margem %',
        'COGS_Total': 'COGS',
        'OPEX_Total': 'OPEX',
        'Custo_Marketing': 'Marketing',
        'Custo_Pessoal_CLT': 'Pessoal CLT',
        'Custo_Infra': 'Infraestrutura',
        'Resultado_Operacional': 'Resultado Op.',
        'EBITDA': 'EBITDA',
        'Fluxo_Caixa': 'Fluxo de Caixa',
        'Saldo_Caixa': 'Saldo Caixa',
        'CAC_Mensal': 'CAC',
        'LTV': 'LTV',
        'LTV_CAC_Ratio': 'LTV/CAC',
        'Taxa_Conv_Geral': 'Conv. %'
    }

    df_display.rename(columns=nomes_colunas, inplace=True)

    # Formata valores monetários
    colunas_moeda = ['MRR', 'ARR', 'ARPU', 'Lucro Bruto', 'COGS', 'OPEX', 
                     'Marketing', 'Pessoal CLT', 'Infraestrutura', 
                     'Resultado Op.', 'EBITDA', 'Fluxo de Caixa', 'Saldo Caixa', 
                     'CAC', 'LTV']

    for col in colunas_moeda:
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(formatar_moeda)

    # Formata percentuais
    colunas_pct = ['Margem %', 'Conv. %']
    for col in colunas_pct:
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(formatar_percentual)

    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.caption("SAM Financial Model v4.0 | Desenvolvido com ❤️ para decisões financeiras inteligentes")
