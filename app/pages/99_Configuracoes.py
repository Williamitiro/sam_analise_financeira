"""
app/pages/99_Configuracoes.py
Página dedicada para a configuração avançada do modelo financeiro.
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto ao sys.path
RAIZ = Path(__file__).resolve().parent.parent.parent
if str(RAIZ) not in sys.path:
    sys.path.append(str(RAIZ))

import streamlit as st
from core.config import (
    criar_config_padrao,
    criar_config_com_contratacoes,
    criar_config_pessimista,
    criar_config_otimista
)
# Imports para a UI do TeamBuilder
from core.builders.team_builder import Cargo, TipoPessoa, GatilhoContratacao, TipoGatilho

st.set_page_config(
    page_title="Configurações - SAM",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Configurações Avançadas")
st.markdown("Use esta página para customizar em detalhes o cenário carregado no Dashboard Principal.")
st.markdown("---")

# Verifica se uma configuração já foi carregada no dashboard principal
if 'config' not in st.session_state:
    st.warning("⬅️ Por favor, gere uma projeção inicial no '00 Dashboard Principal' antes de acessar as configurações detalhadas.")
    st.stop()


# Inicializa a lista de cargos planejados se não existir
if not hasattr(st.session_state.config, 'cargos_planejados'):
    st.session_state.config.cargos_planejados = []

# ============================================================================
# UI BUILDER - EQUIPE
# ============================================================================
with st.expander("👥 Planejamento de Equipe", expanded=True):
    
    st.subheader("Cargos Planejados")
    if not st.session_state.config.cargos_planejados:
        st.info("Nenhum cargo planejado. Adicione o primeiro no formulário abaixo.")
    else:
        for i, cargo in enumerate(st.session_state.config.cargos_planejados):
            gatilho_str = ", ".join(str(g) for g in cargo.gatilhos_contratacao) if cargo.gatilhos_contratacao else f"no mês {cargo.mes_contratacao_manual}"
            col1, col2, col3 = st.columns([2, 3, 1])
            col1.write(f"**{cargo.cargo_funcao}** ({cargo.tipo.value}) - R$ {cargo.salario_base:,.2f}")
            col2.write(f"↳ Contratar quando: *{gatilho_str}*")
            if col3.button("Remover", key=f"del_cargo_{i}"):
                st.session_state.config.cargos_planejados.pop(i)
                st.rerun()

    st.markdown("---")

    with st.form("form_add_cargo", clear_on_submit=True):
        st.subheader("Adicionar Novo Cargo")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            cargo_nome = st.text_input("Nome do Cargo/Função", "Ex: Dev. Backend Sênior")
            tipo_pessoa = st.selectbox("Tipo de Contratação", [p.value for p in TipoPessoa if p in [TipoPessoa.CLT, TipoPessoa.PJ]])
        with col2:
            salario = st.number_input("Salário Base / Valor Mensal", min_value=0.0, step=500.0, format="%.2f")
        with col3:
            encargos = st.slider("Encargos % (CLT)", min_value=0, max_value=120, value=68, disabled=(tipo_pessoa != TipoPessoa.CLT.value)) / 100

        st.subheader("Gatilho para Contratação")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            tipo_gatilho = st.selectbox("Contratar quando...", [g.value for g in TipoGatilho])
        with col_g2:
            valor_gatilho = st.number_input(f"Valor para '{tipo_gatilho}'", min_value=0.0, step=100.0)

        submitted = st.form_submit_button("➕ Adicionar Cargo ao Planejamento")

        if submitted:
            if not cargo_nome or cargo_nome == "Ex: Dev. Backend Sênior":
                st.error("Por favor, insira um nome para o cargo.")
            else:
                # Cria o gatilho
                gatilho = GatilhoContratacao(tipo=TipoGatilho(tipo_gatilho), valor=valor_gatilho)
                
                # Cria o objeto Cargo
                novo_cargo = Cargo(
                    nome=cargo_nome,
                    cargo_funcao=cargo_nome,
                    tipo=TipoPessoa(tipo_pessoa),
                    salario_base=salario,
                    encargos_percentual=encargos if tipo_pessoa == TipoPessoa.CLT.value else 0.0,
                    gatilhos_contratacao=[gatilho]
                )
                
                # Adiciona à lista no session_state
                st.session_state.config.cargos_planejados.append(novo_cargo)
                st.success(f"Cargo '{cargo_nome}' adicionado ao planejamento!")
                st.rerun()

st.markdown("---")
    
with st.expander("📢 Estratégia de Marketing (Exemplo de UI)"):
    st.write("Aqui entrará a interface para definir as fases de investimento em marketing.")
