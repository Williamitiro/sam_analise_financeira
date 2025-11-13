"""
SAM Financial Model - Streamlit App (Versão 2.0 - Protótipo Completo)
Interface web interativa para simulação de cenários financeiros completos.

Para executar localmente:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO

# Módulos do projeto
from config import (
    ConfigFinanceira, 
    CONFIG_PADRAO, 
    CONFIG_PESSIMISTA, 
    CONFIG_OTIMISTA,
    criar_config_com_contratacoes,
    Funcionario,
    FerramentaSaaS,
    AtivoDepreciavel,
    DespesaAnual
)
from engine import MotorProjecaoFinanceira

# ═══════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES DO APP
# ═══════════════════════════════════════════════════════════════

def exibir_kpis_principais(kpis: dict):
    """Exibe os KPIs principais em colunas."""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Break-Even", f"Mês {kpis.get('Break_Even_Mes', 'N/A')}")
    with col2:
        st.metric("💰 Payback", f"Mês {kpis.get('Payback_Investimento_Mes', 'N/A')}")
    with col3:
        ltv_cac = kpis.get('LTV_CAC_Ratio_Final', 0)
        delta_ltv = "✅ Saudável" if ltv_cac > 3 else "⚠️ Atenção"
        st.metric("📈 LTV/CAC", f"{ltv_cac:.2f}x", delta=delta_ltv)
    with col4:
        vale = kpis.get('Vale_da_Morte_Minimo_Caixa', 0)
        st.metric("⚠️ Vale da Morte", f"R$ {vale:,.0f}", delta=f"Mês {kpis.get('Vale_da_Morte_Mes', 'N/A')}")

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("👥 Usuários (Ano 3)", f"{int(kpis.get('Usuarios_Ano3', 0)):,}")
    with col6:
        st.metric("💵 MRR (Ano 3)", f"R$ {kpis.get('MRR_Ano3', 0):,.0f}")
    with col7:
        st.metric("💎 LTV", f"R$ {kpis.get('LTV_Final', 0):,.0f}")
    with col8:
        saldo_final = kpis.get('Saldo_Caixa_Final', 0)
        delta_saldo = "✅ Positivo" if saldo_final > 0 else "❌ Negativo"
        st.metric("💰 Caixa Final", f"R$ {saldo_final:,.0f}", delta=delta_saldo)

def exibir_graficos_projecao(projecao_df: pd.DataFrame, kpis: dict):
    """Exibe as abas com os gráficos da projeção."""
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Usuários & MRR", "💰 Fluxo de Caixa", "📊 Custos", "🎯 Eficiência (CAC)"])
    
    with tab1:
        fig_usuarios = go.Figure()
        fig_usuarios.add_trace(go.Scatter(x=projecao_df['Mes'], y=projecao_df['Usuarios_Finais'], mode='lines+markers', name='Usuários Finais', line=dict(color='royalblue', width=3)))
        fig_usuarios.update_layout(title="Crescimento de Usuários Pagantes", xaxis_title="Mês", yaxis_title="Usuários", hovermode='x unified')
        st.plotly_chart(fig_usuarios, use_container_width=True)

        fig_mrr = go.Figure()
        fig_mrr.add_trace(go.Scatter(x=projecao_df['Mes'], y=projecao_df['MRR'], mode='lines', name='MRR', fill='tozeroy', line=dict(color='green', width=3)))
        fig_mrr.update_layout(title="Evolução da Receita Mensal Recorrente (MRR)", xaxis_title="Mês", yaxis_title="MRR (R$)", hovermode='x unified')
        st.plotly_chart(fig_mrr, use_container_width=True)

    with tab2:
        fig_caixa = go.Figure()
        fig_caixa.add_trace(go.Scatter(x=projecao_df['Mes'], y=projecao_df['Saldo_Caixa'], mode='lines', name='Saldo de Caixa', fill='tozeroy', line=dict(color='darkblue', width=3)))
        fig_caixa.add_hline(y=0, line_color="black", line_width=1)
        fig_caixa.update_layout(title="Projeção de Saldo de Caixa Acumulado", xaxis_title="Mês", yaxis_title="Saldo de Caixa (R$)", hovermode='x unified')
        st.plotly_chart(fig_caixa, use_container_width=True)

        fig_resultado = go.Figure()
        cores_resultado = ['red' if x < 0 else 'green' for x in projecao_df['Resultado_Operacional']]
        fig_resultado.add_trace(go.Bar(x=projecao_df['Mes'], y=projecao_df['Resultado_Operacional'], marker_color=cores_resultado, name='Resultado Operacional'))
        fig_resultado.add_hline(y=0, line_color="black", line_width=1)
        fig_resultado.update_layout(title="Lucro/Prejuízo Mensal", xaxis_title="Mês", yaxis_title="Resultado (R$)", hovermode='x unified')
        st.plotly_chart(fig_resultado, use_container_width=True)

    with tab3:
        # O engine atual agrupa os custos. Para um gráfico de pizza, precisaríamos de mais detalhes.
        # Por enquanto, vamos mostrar os custos principais que já estão no DF.
        st.markdown("##### 📊 Composição de Custos Principais (OPEX)")
        custo_cols = ['Custo_Infra', 'Custo_Marketing', 'Salario_Pago']
        df_custos = projecao_df[custo_cols]
        fig_custos = px.area(df_custos, x=df_custos.index, y=custo_cols, title="Evolução dos Custos Principais", labels={"value": "Custo (R$)", "variable": "Tipo de Custo", "index": "Mês"})
        st.plotly_chart(fig_custos, use_container_width=True)
        
        st.markdown("##### 📊 Distribuição de Custos (Mês 36)")
        ultimo_mes = projecao_df.iloc[-1]
        fig_pizza = go.Figure(data=[go.Pie(labels=custo_cols, values=[ultimo_mes[col] for col in custo_cols], hole=0.3)])
        fig_pizza.update_layout(height=400)
        st.plotly_chart(fig_pizza, use_container_width=True)

    with tab4:
        fig_cac = go.Figure()
        fig_cac.add_trace(go.Scatter(x=projecao_df['Mes'], y=projecao_df['CAC_Mensal'], mode='lines+markers', name='CAC Mensal', line=dict(color='red', width=2)))
        fig_cac.update_layout(title="Custo de Aquisição de Cliente (CAC) Mensal", xaxis_title="Mês", yaxis_title="CAC (R$)", hovermode='x unified')
        st.plotly_chart(fig_cac, use_container_width=True)
        
        fig_ltv_cac = go.Figure()
        fig_ltv_cac.add_trace(go.Scatter(x=projecao_df['Mes'], y=projecao_df['LTV_CAC_Ratio_Mensal'], mode='lines+markers', name='LTV/CAC Ratio', line=dict(color='purple', width=2)))
        fig_ltv_cac.add_hline(y=3, line_dash="dash", line_color="gray", annotation_text="Meta Saldável (3x)")
        fig_ltv_cac.update_layout(title="Evolução da Relação LTV/CAC", xaxis_title="Mês", yaxis_title="LTV/CAC Ratio", hovermode='x unified')
        st.plotly_chart(fig_ltv_cac, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DA PÁGINA
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="SAM Financial Model",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💰 SAM Financial Model - Protótipo Completo")
st.markdown("### Simulador Avançado de Viabilidade Financeira e Análise de Cenários")

# ═══════════════════════════════════════════════════════════════
# SIDEBAR: CONFIGURAÇÕES E CENÁRIOS
# ═══════════════════════════════════════════════════════════════

st.sidebar.header("⚙️ Configurações e Cenários")

# --- Seletor de Cenários Predefinidos ---
st.sidebar.subheader("📂 Cenários Predefinidos")
tipo_cenario = st.sidebar.selectbox(
    "Escolha um cenário para começar:",
    ["Personalizado", "Realista (c/ contratações)", "Pessimista", "Otimista"]
)

# Inicializa a config com base na seleção
if tipo_cenario == "Realista (c/ contratações)":
    config = criar_config_com_contratacoes()
elif tipo_cenario == "Pessimista":
    config = CONFIG_PESSIMISTA
elif tipo_cenario == "Otimista":
    config = CONFIG_OTIMISTA
else: # Personalizado
    config = CONFIG_PADRAO

# --- Configurações Básicas (Sempre Visíveis) ---
st.sidebar.subheader("📊 Premissas Básicas")
config.visitantes_mes_1 = st.sidebar.number_input("Visitantes Mês 1", value=config.visitantes_mes_1, step=100)
config.taxa_crescimento_trafego_mensal = st.sidebar.slider("Crescimento de Tráfego (%/mês)", min_value=0, max_value=50, value=int(config.taxa_crescimento_trafego_mensal * 100)) / 100
config.taxa_conversao_visitante_trial = st.sidebar.slider("Taxa Conv. Visitante→Trial (%)", min_value=1, max_value=20, value=int(config.taxa_conversao_visitante_trial * 100)) / 100
config.taxa_conversao_trial_pagante = st.sidebar.slider("Taxa Conv. Trial→Pagante (%)", min_value=5, max_value=30, value=int(config.taxa_conversao_trial_pagante * 100)) / 100
config.churn_mensal = st.sidebar.slider("Churn Mensal (%)", min_value=1, max_value=10, value=int(config.churn_mensal * 100)) / 100
config.arpu_medio_override = st.sidebar.number_input("ARPU Médio (R$)", value=config.arpu_medio, step=10.0, format="%.2f")

# --- Configurações de Capital ---
st.sidebar.subheader("💵 Capital e Financiamento")
config.capital_inicial_caixa = st.sidebar.number_input("Capital Inicial (Capex)", value=config.capital_inicial_caixa, step=1000.0, format="%.2f")
config.aporte_mensal_fixo = st.sidebar.number_input("Aporte Mensal", value=config.aporte_mensal_fixo, step=100.0, format="%.2f")
config.meses_aporte_fixo = st.sidebar.slider("Duração do Aporte (meses)", min_value=1, max_value=36, value=config.meses_aporte_fixo)

# --- Configurações Avançadas (Expansível) ---
with st.sidebar.expander("🧑‍💼 Gestão de Pessoal (CLT/PJ)"):
    if st.button("Adicionar Funcionário"):
        config.equipe.append(Funcionario(nome="Novo Funcionário", cargo="Cargo", salario_bruto=5000.0, mes_inicio=12))
    
    # st.data_editor é ideal aqui, mas para simplificar, vamos exibir como texto por enquanto
    for i, func in enumerate(config.equipe):
        st.markdown(f"**{func.nome}** ({func.tipo}): R$ {func.salario_bruto:,.2f} a partir do mês {func.mes_inicio}")

with st.sidebar.expander("🏢 Escritório e Operações"):
    config.escritorio_mes_inicio = st.slider("Início das Despesas de Escritório", min_value=1, max_value=36, value=config.escritorio_mes_inicio)
    if config.escritorio_mes_inicio < 36:
        config.escritorio_aluguel_mensal = st.number_input("Aluguel Mensal", value=0.0, step=100.0)
        config.escritorio_agua_luz_mensal = st.number_input("Água/Luz/Internet", value=0.0, step=50.0)

# Botão principal de execução
executar = st.sidebar.button("🚀 EXECUTAR SIMULAÇÃO", type="primary")

# ═══════════════════════════════════════════════════════════════
# MAIN: RESULTADOS E ANÁLISES
# ═══════════════════════════════════════════════════════════════

if executar:
    # Executa a projeção principal
    with st.spinner("🔄 Processando projeção... Isso pode levar alguns segundos."):
        motor = MotorProjecaoFinanceira(config)
        projecao_df = motor.executar_projecao(meses=36)
        kpis = motor.calcular_kpis()

    st.success("✅ Simulação concluída!")
    
    # --- Seção 1: KPIs Principais ---
    exibir_kpis_principais(kpis)

    # --- Seção 2: Gráficos Interativos ---
    st.markdown("---")
    st.subheader("📈 Análise Visual da Projeção")
    exibir_graficos_projecao(projecao_df, kpis)

    # --- Seção 3: Análise Comparativa de Cenários ---
    st.markdown("---")
    st.subheader("🔬 Análise Comparativa de Cenários")
    st.markdown("Compare o cenário atual com os outros dois cenários padrão.")
    
    if st.button("Comparar com Pessimista e Otimista"):
        with st.spinner("🔄 Rodando cenários comparativos..."):
            motor_pessimista = MotorProjecaoFinanceira(CONFIG_PESSIMISTA)
            motor_pessimista.executar_projecao(36)
            kpis_pessimista = motor_pessimista.calcular_kpis()

            motor_otimista = MotorProjecaoFinanceira(CONFIG_OTIMISTA)
            motor_otimista.executar_projecao(36)
            kpis_otimista = motor_otimista.calcular_kpis()
        
        df_comparacao = pd.DataFrame([
            {'Cenário': 'Pessimista', **kpis_pessimista},
            {'Cenário': 'Atual (Sua Simulação)', **kpis},
            {'Cenário': 'Otimista', **kpis_otimista}
        ]).set_index('Cenário')

        cols_to_show = ['MRR_Ano3', 'Usuarios_Ano3', 'Saldo_Caixa_Final', 'Vale_da_Morte_Minimo_Caixa', 'LTV_CAC_Ratio_Final']
        st.dataframe(df_comparacao[cols_to_show].style.format({
            "MRR_Ano3": "R$ {:,.0f}",
            "Usuarios_Ano3": "{:,.0f}",
            "Saldo_Caixa_Final": "R$ {:,.0f}",
            "Vale_da_Morte_Minimo_Caixa": "R$ {:,.0f}",
            "LTV_CAC_Ratio_Final": "{:.2f}x"
        }), use_container_width=True)
        
        # Gráfico comparativo
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(name='Pessimista', x=df_comparacao.index, y=df_comparacao['MRR_Ano3']))
        fig_comp.add_trace(go.Bar(name='Atual', x=df_comparacao.index, y=df_comparacao['MRR_Ano3']))
        fig_comp.add_trace(go.Bar(name='Otimista', x=df_comparacao.index, y=df_comparacao['MRR_Ano3']))
        fig_comp.update_layout(title='Comparativo de MRR no Ano 3', barmode='group', yaxis_title='MRR (R$)')
        st.plotly_chart(fig_comp, use_container_width=True)


    # --- Seção 4: Análise de Sensibilidade ---
    st.markdown("---")
    st.subheader("🎛️ Análise de Sensibilidade (Impacto do Churn)")
    st.markdown("Veja como a variação do Churn impacta a saúde do negócio.")
    
    if st.button("Rodar Análise de Sensibilidade"):
        with st.spinner("🔄 Calculando sensibilidade..."):
            churns = np.arange(0.02, 0.09, 0.01)
            resultados_sens = []
            for churn in churns:
                config_temp = ConfigFinanceira(churn_mensal=churn)
                motor_temp = MotorProjecaoFinanceira(config_temp)
                motor_temp.executar_projecao(36)
                kpis_temp = motor_temp.calcular_kpis()
                resultados_sens.append({'Churn (%)': f"{churn*100:.0f}%", 'LTV (R$)': kpis_temp['LTV_Final'], 'LTV/CAC': kpis_temp['LTV_CAC_Ratio_Final']})
            
            df_sensibilidade = pd.DataFrame(resultados_sens)
            
            fig_sens, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
            sns.lineplot(data=df_sensibilidade, x='Churn (%)', y='LTV (R$)', ax=ax1, marker='o', lw=3)
            ax1.set_title('Impacto do Churn no LTV')
            ax1.grid(True, alpha=0.3)

            sns.lineplot(data=df_sensibilidade, x='Churn (%)', y='LTV/CAC', ax=ax2, marker='o', lw=3)
            ax2.axhline(3, color='red', linestyle='--', lw=2, label='Meta Saldável (3x)')
            ax2.set_title('Impacto do Churn na Relação LTV/CAC')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            st.pyplot(fig_sens)
            st.dataframe(df_sensibilidade.style.format({"LTV (R$)": "R$ {:,.0f}", "LTV/CAC": "{:.2f}x"}), use_container_width=True)

    # --- Seção 5: Download de Dados ---
    st.markdown("---")
    st.subheader("💾 Exportar Resultados")
    
    # Download CSV
    csv = projecao_df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download Projeção (CSV)", data=csv, file_name="projecao_sam.csv", mime="text/csv")

    # Download Excel
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        projecao_df.to_excel(writer, sheet_name='Projeção', index=False)
        pd.DataFrame(list(kpis.items()), columns=['KPI', 'Valor']).to_excel(writer, sheet_name='KPIs', index=False)
    st.download_button(
        label="📥 Download Projeção (Excel)",
        data=excel_buffer.getvalue(),
        file_name="projecao_sam.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("👈 Configure os parâmetros na barra lateral e clique em **EXECUTAR SIMULAÇÃO** para começar.")
    st.markdown("### 📋 O que este protótipo oferece:")
    st.markdown("""
    - **Configuração Completa:** Altere desde as premissas básicas até a gestão de pessoal e custos de escritório.
    - **Cenários Predefinidos:** Comece com cenários Pessimista, Realista ou Otimista.
    - **Análise Comparativa:** Compare sua simulação com outros cenários lado a lado.
    - **Análise de Sensibilidade:** Entenda o impacto de variáveis-chave (como o Churn) no seu negócio.
    - **Visualizações Ricas:** Gráficos interativos para entender a trajetória financeira.
    - **Exportação de Dados:** Baixe os resultados em CSV ou Excel para análises futuras.
    """)

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray; padding: 20px;'><p><strong>SAM Financial Model v2.0</strong></p><p>Protótipo Completo para Análise de Viabilidade</p></div>", unsafe_allow_html=True)