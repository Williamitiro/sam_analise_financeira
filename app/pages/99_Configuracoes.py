"""
app/pages/99_Configuracoes.py
Página de Configurações Avançadas - VERSÃO COMPLETA
Centro de controle para todas as configurações do modelo financeiro SAM.
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto ao sys.path
RAIZ = Path(__file__).resolve().parent.parent.parent
if str(RAIZ) not in sys.path:
    sys.path.append(str(RAIZ))

import streamlit as st
import pandas as pd
from datetime import datetime

# Imports dos Builders
from core.builders.capital_builder import CapitalBuilder, Aporte
from core.builders.team_builder import TeamBuilder, Cargo, TipoPessoa, GatilhoContratacao, TipoGatilho
from core.builders.tools_builder import ToolsBuilder, FerramentaSaaS, CategoriaFerramenta
from core.builders.infra_builder import InfraBuilder, TierInfra
from core.builders.marketing_builder import MarketingBuilder, FaseMarketing
from core.builders.revenue_builder import RevenueBuilder, Plano
from core.builders.cogs_builder import COGSBuilder
from core.builders.channels_builder import ChannelsBuilder, CanalAquisicao
from core.builders.tax_builder import TaxBuilder
from core.builders.risk_builder import RiskBuilder, CenarioRisco

# Import da config
from core.config import ConfigFinanceira, criar_config_padrao

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Configurações - SAM",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Customizado
st.markdown("""
<style>
    /* Tabs customizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 10px 20px;
        background-color: rgba(49, 51, 63, 0.2);
        border-radius: 5px 5px 0 0;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    
    /* Headers de seção */
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1f77b4;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #1f77b4;
    }
    
    /* Cards de item */
    .item-card {
        background: rgba(49, 51, 63, 0.1);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #1f77b4;
    }
    
    /* Alertas */
    .validation-warning {
        background: rgba(255, 170, 0, 0.1);
        border-left: 3px solid #ffaa00;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

# Verifica se config existe no session_state
if 'config' not in st.session_state:
    st.session_state.config = criar_config_padrao()

# Inicializa listas vazias se não existirem
if not hasattr(st.session_state.config, 'cargos_planejados'):
    st.session_state.config.cargos_planejados = []

if not hasattr(st.session_state.config, 'aportes_programados'):
    st.session_state.config.aportes_programados = []

if not hasattr(st.session_state.config, 'tiers_infraestrutura'):
    st.session_state.config.tiers_infraestrutura = []

if not hasattr(st.session_state.config, 'fases_marketing'):
    st.session_state.config.fases_marketing = []

if not hasattr(st.session_state.config, 'planos_receita'):
    st.session_state.config.planos_receita = []

if not hasattr(st.session_state.config, 'canais_aquisicao'):
    st.session_state.config.canais_aquisicao = []

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def validar_percentuais(valores: list, nome_campo: str = "Mix") -> bool:
    """Valida se percentuais somam 100%"""
    total = sum(valores)
    if abs(total - 100) > 0.1:  # Tolerância de 0.1%
        st.warning(f"⚠️ {nome_campo} soma {total:.1f}% (deve somar 100%)")
        return False
    return True

def formatar_moeda(valor):
    """Formata valor em reais"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def salvar_config():
    """Salva configuração e mostra feedback"""
    st.success("✅ Configuração atualizada!")
    # Invalida cache se necessário
    if 'df_projecao' in st.session_state:
        st.session_state.df_projecao = None
    if 'kpis' in st.session_state:
        st.session_state.kpis = None

# ============================================================================
# HEADER
# ============================================================================

st.title("⚙️ Configurações Avançadas")
st.markdown("**Centro de Comando** - Configure todos os aspectos do seu modelo financeiro")
st.markdown("---")

# ============================================================================
# INFORMAÇÕES GERAIS
# ============================================================================

with st.expander("ℹ️ Informações da Projeção", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        nome_proj = st.text_input(
            "Nome da Projeção",
            value=getattr(st.session_state.config, 'nome_projecao', "Projeção Realista - Validação SAM"),
            help="Dê um nome descritivo para esta configuração"
        )
        st.session_state.config.nome_projecao = nome_proj
    
    with col2:
        autor = st.text_input(
            "Autor/Responsável",
            value=getattr(st.session_state.config, 'autor', "Equipe SAM"),
            help="Quem criou/mantém esta configuração"
        )
        st.session_state.config.autor = autor
    
    with col3:
        st.markdown("**Última Modificação:**")
        st.caption(datetime.now().strftime("%d/%m/%Y %H:%M"))

st.markdown("---")

# ============================================================================
# TABS PRINCIPAIS
# ============================================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "💰 Capital",
    "📊 Receita",
    "📈 Funil & Canais",
    "💸 COGS",
    "🏗️ Infraestrutura",
    "📢 Marketing",
    "👥 Equipe",
    "⚙️ Geral"
])

# ============================================================================
# TAB 1: CAPITAL & FINANCIAMENTO
# ============================================================================

with tab1:
    st.markdown('<div class="section-header">💰 Capital & Financiamento</div>', unsafe_allow_html=True)
    
    # Capital Inicial
    with st.expander("💵 Capital Inicial & Investimento", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            capital_inicial = st.number_input(
                "Investimento Inicial (R$)",
                min_value=-1000000.0,
                max_value=0.0,
                value=float(st.session_state.config.capital_inicial_caixa),
                step=1000.0,
                help="CAPEX inicial (negativo = saída de caixa). Ex: -8000 para compra de equipamento"
            )
            st.session_state.config.capital_inicial_caixa = capital_inicial
        
        with col2:
            aporte_fixo = st.number_input(
                "Aporte Mensal Fixo (R$)",
                min_value=0.0,
                max_value=1000000.0,
                value=float(st.session_state.config.aporte_mensal_fixo),
                step=100.0,
                help="Aporte regular mensal (se houver)"
            )
            st.session_state.config.aporte_mensal_fixo = aporte_fixo
        
        meses_aporte = st.slider(
            "Duração do Aporte Fixo (meses)",
            min_value=0,
            max_value=60,
            value=int(st.session_state.config.meses_aporte_fixo),
            help="Por quantos meses o aporte fixo será mantido"
        )
        st.session_state.config.meses_aporte_fixo = meses_aporte
    
    # Aportes Programados (Múltiplos)
    with st.expander("📅 Aportes Programados (Rodadas, Empréstimos)", expanded=False):
        st.markdown("Adicione aportes específicos que acontecerão em datas determinadas")
        
        # Lista de aportes existentes
        if hasattr(st.session_state.config, 'aportes_programados') and st.session_state.config.aportes_programados:
            st.markdown("**Aportes Cadastrados:**")
            for idx, aporte in enumerate(st.session_state.config.aportes_programados):
                col1, col2, col3 = st.columns([3, 2, 1])
                col1.write(f"**{aporte.data.strftime('%d/%m/%Y')}:** {formatar_moeda(aporte.valor)}")
                col2.write(f"📝 {aporte.socio}")
                if col3.button("🗑️", key=f"del_aporte_{idx}"):
                    st.session_state.config.aportes_programados.pop(idx)
                    st.rerun()
        else:
            st.info("Nenhum aporte programado ainda. Adicione o primeiro abaixo.")
        
        st.markdown("---")
        
        # Formulário para adicionar novo aporte
        with st.form("form_add_aporte", clear_on_submit=True):
            st.subheader("Adicionar Novo Aporte de Capital (Equity)")
            col1, col2 = st.columns(2)
            
            with col1:
                data_aporte = st.date_input("Data do Aporte")
            
            with col2:
                valor_aporte = st.number_input("Valor (R$)", min_value=0.0, step=1000.0, value=50000.0)
            
            socio_aporte = st.text_input("Sócio / Origem do Capital", placeholder="Ex: Rodada Seed, Investidor Anjo")
            
            submitted = st.form_submit_button("➕ Adicionar Aporte", use_container_width=True)
            
            if submitted:
                novo_aporte = Aporte(
                    data=data_aporte,
                    valor=valor_aporte,
                    socio=socio_aporte
                )
                if not hasattr(st.session_state.config, 'aportes_programados'):
                    st.session_state.config.aportes_programados = []
                st.session_state.config.aportes_programados.append(novo_aporte)
                salvar_config()
                st.rerun()
    
    # Reserva de Contingência
    with st.expander("🛡️ Reserva de Contingência", expanded=False):
        st.markdown("Defina uma reserva de segurança como % da receita")
        
        col1, col2 = st.columns(2)
        with col1:
            ativar_reserva = st.checkbox(
                "Ativar Reserva de Contingência",
                value=getattr(st.session_state.config, 'ativar_reserva_contingencia', False)
            )
            st.session_state.config.ativar_reserva_contingencia = ativar_reserva
        
        with col2:
            if ativar_reserva:
                percentual_reserva = st.slider(
                    "% da Receita para Reserva",
                    min_value=0,
                    max_value=50,
                    value=getattr(st.session_state.config, 'percentual_reserva', 10),
                    help="Percentual da receita mensal que será guardado como reserva"
                )
                st.session_state.config.percentual_reserva = percentual_reserva

# ============================================================================
# TAB 2: MODELO DE RECEITA
# ============================================================================

with tab2:
    st.markdown('<div class="section-header">💰 Modelo de Receita</div>', unsafe_allow_html=True)
    
    # Planos de Assinatura
    with st.expander("📋 Planos de Assinatura", expanded=True):
        st.markdown("Configure os planos de assinatura e o mix de aquisição")
        
        # Lista de planos existentes
        if hasattr(st.session_state.config, 'planos_receita') and st.session_state.config.planos_receita:
            st.markdown("**Planos Cadastrados:**")
            
            total_mix = 0
            for idx, plano in enumerate(st.session_state.config.planos_receita):
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                col1.write(f"**{plano.nome}**")
                col2.write(f"💰 {formatar_moeda(plano.preco_mensal)}/mês")
                col3.write(f"📊 Mix: {plano.percentual_clientes*100:.0f}%")
                total_mix += plano.percentual_clientes * 100
                
                if col4.button("🗑️", key=f"del_plano_{idx}"):
                    st.session_state.config.planos_receita.pop(idx)
                    st.rerun()
            
            # Validação do mix
            if not validar_percentuais([p.percentual_clientes * 100 for p in st.session_state.config.planos_receita], "Mix de Planos"):
                st.markdown('<div class="validation-warning">⚠️ Ajuste o mix para somar exatamente 100%</div>', unsafe_allow_html=True)
            
            # Cálculo do ARPU
            arpu_calculado = sum([
                p.preco_mensal * p.percentual_clientes
                for p in st.session_state.config.planos_receita
            ])
            st.metric("ARPU Médio Calculado", formatar_moeda(arpu_calculado))
            
        else:
            st.info("Nenhum plano cadastrado. Adicione o primeiro plano abaixo.")
        
        st.markdown("---")
        
        # Formulário para adicionar novo plano
        with st.form("form_add_plano", clear_on_submit=True):
            st.subheader("Adicionar Novo Plano")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                nome_plano = st.text_input("Nome do Plano", placeholder="Ex: Lite, Pro, Enterprise")
            
            with col2:
                preco_plano = st.number_input("Preço Mensal (R$)", min_value=0.0, step=10.0, value=99.0)
            
            with col3:
                mix_plano = st.number_input("Mix de Aquisição (%)", min_value=0.0, max_value=100.0, step=5.0, value=33.0)

            with col4:
                churn_plano = st.number_input("Churn do Plano (%)", min_value=0.0, max_value=100.0, step=0.1, value=4.0)
            
            submitted = st.form_submit_button("➕ Adicionar Plano", use_container_width=True)
            
            if submitted:
                if not nome_plano:
                    st.error("Nome do plano é obrigatório")
                else:
                    novo_plano = Plano(
                        nome=nome_plano,
                        preco_mensal=preco_plano,
                        percentual_clientes=mix_plano / 100.0,
                        churn_mensal=churn_plano / 100.0
                    )
                    if not hasattr(st.session_state.config, 'planos_receita'):
                        st.session_state.config.planos_receita = []
                    st.session_state.config.planos_receita.append(novo_plano)
                    salvar_config()
                    st.rerun()
    
    # ARPU Override
    with st.expander("🎯 Override de ARPU", expanded=False):
        st.markdown("Caso queira definir um ARPU manualmente (ignorando o mix de planos)")
        
        col1, col2 = st.columns(2)
        with col1:
            usar_override = st.checkbox(
                "Usar ARPU Manual",
                value=st.session_state.config.arpu_medio_override is not None
            )
        
        with col2:
            if usar_override:
                arpu_manual = st.number_input(
                    "ARPU Manual (R$)",
                    min_value=0.0,
                    step=10.0,
                    value=float(st.session_state.config.arpu_medio_override or 97.0)
                )
                st.session_state.config.arpu_medio_override = arpu_manual
            else:
                st.session_state.config.arpu_medio_override = None
    
    # Upsell/Downsell (Futuro)
    with st.expander("📈 Upsell & Downsell (Em Desenvolvimento)", expanded=False):
        st.info("🚧 Funcionalidade de migração entre planos será implementada na próxima versão")

# ============================================================================
# TAB 3: FUNIL & CANAIS
# ============================================================================

with tab3:
    st.markdown('<div class="section-header">📈 Funil de Aquisição & Canais</div>', unsafe_allow_html=True)
    
    # Parâmetros Gerais do Funil
    with st.expander("🔢 Parâmetros Gerais do Funil", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            visitantes_mes1 = st.number_input(
                "Visitantes no Mês 1",
                min_value=0,
                step=100,
                value=int(st.session_state.config.visitantes_mes_1),
                help="Número inicial de visitantes do site/app"
            )
            st.session_state.config.visitantes_mes_1 = visitantes_mes1
            
            crescimento_trafego = st.slider(
                "Crescimento de Tráfego Mensal (%)",
                min_value=0,
                max_value=100,
                value=int(st.session_state.config.taxa_crescimento_trafego_mensal * 100),
                help="Percentual de crescimento mensal do tráfego"
            )
            st.session_state.config.taxa_crescimento_trafego_mensal = crescimento_trafego / 100
        
        with col2:
            conv_trial = st.slider(
                "Conversão Visitante → Trial (%)",
                min_value=0.0,
                max_value=20.0,
                value=float(st.session_state.config.taxa_conversao_visitante_trial * 100),
                step=0.5,
                help="% de visitantes que iniciam trial"
            )
            st.session_state.config.taxa_conversao_visitante_trial = conv_trial / 100
            
            conv_pagante = st.slider(
                "Conversão Trial → Pagante (%)",
                min_value=0.0,
                max_value=50.0,
                value=float(st.session_state.config.taxa_conversao_trial_pagante * 100),
                step=1.0,
                help="% de trials que viram clientes pagantes"
            )
            st.session_state.config.taxa_conversao_trial_pagante = conv_pagante / 100
        
        # Cálculo da conversão geral
        conv_geral = (conv_trial / 100) * (conv_pagante / 100) * 100
        st.metric("Conversão Geral (Visitante → Pagante)", f"{conv_geral:.2f}%")
    
    # Retenção
    with st.expander("🔄 Retenção & Churn", expanded=True):
        churn_mensal = st.slider(
            "Churn Mensal (%)",
            min_value=0.0,
            max_value=20.0,
            value=float(st.session_state.config.churn_mensal * 100),
            step=0.5,
            help="Percentual de clientes que cancelam por mês"
        )
        st.session_state.config.churn_mensal = churn_mensal / 100
        
        # Métricas derivadas
        col1, col2, col3 = st.columns(3)
        with col1:
            retencao = (1 - churn_mensal/100) * 100
            st.metric("Taxa de Retenção", f"{retencao:.1f}%")
        with col2:
            lifetime_meses = 1 / (churn_mensal/100) if churn_mensal > 0 else float('inf')
            st.metric("Lifetime Médio", f"{lifetime_meses:.1f} meses" if lifetime_meses != float('inf') else "∞")
        with col3:
            st.metric("Retenção Anual", f"{(retencao/100)**12*100:.0f}%")
    
    # Canais de Aquisição (Avançado)
    with st.expander("🎯 Canais de Aquisição Detalhados", expanded=False):
        st.markdown("Configure diferentes canais com conversões e CACs específicos")
        st.info("🚧 Funcionalidade multi-canal será implementada em breve. Por ora, use os parâmetros gerais acima.")

# ============================================================================
# TAB 4: COGS (Custos Variáveis)
# ============================================================================

with tab4:
    st.markdown('<div class="section-header">💸 COGS - Custos Variáveis</div>', unsafe_allow_html=True)
    
    # Custo de IA
    with st.expander("🤖 Custos de IA & APIs", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            ativar_ia = st.checkbox(
                "Ativar Custo de IA",
                value=st.session_state.config.ativar_custo_ia,
                help="Custo de APIs de LLM por usuário"
            )
            st.session_state.config.ativar_custo_ia = ativar_ia
        
        with col2:
            if ativar_ia:
                custo_ia = st.number_input(
                    "Custo IA por Usuário (R$/mês)",
                    min_value=0.0,
                    step=1.0,
                    value=float(st.session_state.config.custo_ia_por_usuario),
                    help="Custo médio de IA por usuário ativo"
                )
                st.session_state.config.custo_ia_por_usuario = custo_ia
    
    # Impostos
    with st.expander("🧾 Impostos sobre Receita", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            ativar_impostos = st.checkbox(
                "Ativar Impostos",
                value=st.session_state.config.ativar_impostos
            )
            st.session_state.config.ativar_impostos = ativar_impostos
        
        with col2:
            if ativar_impostos:
                aliquota_impostos = st.slider(
                    "Alíquota (%)",
                    min_value=0.0,
                    max_value=50.0,
                    value=float(st.session_state.config.aliquota_impostos * 100),
                    step=0.5,
                    help="Simples Nacional (geralmente 6-15%)"
                )
                st.session_state.config.aliquota_impostos = aliquota_impostos / 100
    
    # Taxas de Pagamento
    with st.expander("💳 Taxas de Gateway de Pagamento", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            ativar_taxas = st.checkbox(
                "Ativar Taxas de Pagamento",
                value=st.session_state.config.ativar_taxas_pgto
            )
            st.session_state.config.ativar_taxas_pgto = ativar_taxas
        
        if ativar_taxas:
            with col2:
                taxa_percentual = st.slider(
                    "Taxa Percentual (%)",
                    min_value=0.0,
                    max_value=10.0,
                    value=float(st.session_state.config.taxa_pagamento_percentual * 100),
                    step=0.1,
                    help="Taxa % sobre transação (ex: 3.49% Stripe)"
                )
                st.session_state.config.taxa_pagamento_percentual = taxa_percentual / 100
            
            taxa_fixa = st.number_input(
                "Taxa Fixa por Transação (R$)",
                min_value=0.0,
                step=0.1,
                value=float(st.session_state.config.taxa_pagamento_fixa_por_transacao),
                help="Taxa fixa por transação (ex: R$ 0.39)"
            )
            st.session_state.config.taxa_pagamento_fixa_por_transacao = taxa_fixa
    
    # Comissões
    with st.expander("🤝 Comissões (Afiliados, Parceiros)", expanded=False):
        st.info("🚧 Sistema de comissões será implementado em breve")

# ============================================================================
# TAB 5: INFRAESTRUTURA
# ============================================================================

with tab5:
    st.markdown('<div class="section-header">🏗️ Infraestrutura Escalável</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Configure os **tiers de infraestrutura** que serão ativados automaticamente 
    conforme o número de usuários cresce.
    """)
    
    # Lista de tiers existentes
    if hasattr(st.session_state.config, 'tiers_infraestrutura') and st.session_state.config.tiers_infraestrutura:
        st.markdown("**Tiers Cadastrados:**")
        
        for idx, tier in enumerate(st.session_state.config.tiers_infraestrutura):
            with st.expander(f"Tier {tier.numero}: {tier.nome}", expanded=False):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                col1.write(f"**Usuários:** {tier.limite_usuarios_min} - {tier.limite_usuarios_max}")
                col2.write(f"**Custo:** {formatar_moeda(tier.custo_fixo_total)}/mês")
                
                if col3.button("🗑️ Remover", key=f"del_tier_{idx}"):
                    st.session_state.config.tiers_infraestrutura.pop(idx)
                    st.rerun()
                
                # Detalhes
                if tier.descricao:
                    st.caption(f"📝 {tier.descricao}")
    
    else:
        st.warning("⚠️ Nenhum tier configurado. Configure pelo menos 1 tier.")
    
    st.markdown("---")
    
    # Formulário para adicionar novo tier
    with st.form("form_add_tier", clear_on_submit=True):
        st.subheader("Adicionar Novo Tier de Infraestrutura")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            numero_tier = st.number_input("Número do Tier", min_value=1, max_value=10, value=1, step=1)
            nome_tier = st.text_input("Nome do Tier", placeholder="Ex: Validação, Escala, Hiperescala")
        
        with col2:
            limite_min = st.number_input("Limite Mínimo (usuários)", min_value=0, step=10, value=0)
            limite_max = st.number_input("Limite Máximo (usuários)", min_value=0, step=10, value=100)
        
        with col3:
            custo_fixo = st.number_input("Custo Fixo Mensal (R$)", min_value=0.0, step=100.0, value=209.0)
            custo_var_usuario = st.number_input("Custo Variável/Usuário (R$)", min_value=0.0, step=0.1, value=0.0, 
                                               help="Custo adicional por usuário excedente")
        
        descricao_tier = st.text_area("Descrição/Componentes", 
                                     placeholder="Ex: VPS Principal R$55 + VPS MT5 R$150 + Domínio R$4")
        
        submitted = st.form_submit_button("➕ Adicionar Tier", use_container_width=True)
        
        if submitted:
            if not nome_tier:
                st.error("Nome do tier é obrigatório")
            elif limite_min >= limite_max:
                st.error("Limite mínimo deve ser menor que máximo")
            else:
                novo_tier = TierInfra(
                    numero=numero_tier,
                    nome=nome_tier,
                    limite_usuarios_min=limite_min,
                    limite_usuarios_max=limite_max,
                    custo_fixo_total=custo_fixo,
                    custo_variavel_por_usuario=custo_var_usuario,
                    descricao=descricao_tier
                )
                if not hasattr(st.session_state.config, 'tiers_infraestrutura'):
                    st.session_state.config.tiers_infraestrutura = []
                st.session_state.config.tiers_infraestrutura.append(novo_tier)
                # Ordena por número
                st.session_state.config.tiers_infraestrutura.sort(key=lambda x: x.numero)
                salvar_config()
                st.rerun()

# ============================================================================
# TAB 6: MARKETING
# ============================================================================

with tab6:
    st.markdown('<div class="section-header">📢 Estratégia de Marketing</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Configure as **fases de marketing** que serão ativadas automaticamente 
    conforme a empresa amadurece.
    """)
    
    # Lista de fases existentes
    if hasattr(st.session_state.config, 'fases_marketing') and st.session_state.config.fases_marketing:
        st.markdown("**Fases Cadastradas:**")
        
        for idx, fase in enumerate(st.session_state.config.fases_marketing):
            with st.expander(f"Fase {fase.numero}: {fase.nome}", expanded=False):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                col1.write(f"**Duração:** Mês {fase.mes_inicio} - {fase.mes_fim or '∞'}")
                
                tipo_orcamento = fase.tipo_orcamento
                if tipo_orcamento == 'fixo':
                    col2.write(f"**Orçamento:** {formatar_moeda(fase.valor)}/mês")
                elif tipo_orcamento == 'percentual_lucro':
                    col2.write(f"**Orçamento:** {fase.valor*100:.0f}% do Lucro Bruto")
                elif tipo_orcamento == 'percentual_receita':
                    col2.write(f"**Orçamento:** {fase.valor*100:.0f}% da Receita")
                
                if col3.button("🗑️", key=f"del_fase_{idx}"):
                    st.session_state.config.fases_marketing.pop(idx)
                    st.rerun()
                
                if fase.descricao:
                    st.caption(f"📝 {fase.descricao}")
    
    else:
        st.info("Nenhuma fase de marketing configurada. Adicione a primeira abaixo.")
    
    st.markdown("---")
    
    # Formulário para adicionar nova fase
    with st.form("form_add_fase", clear_on_submit=True):
        st.subheader("Adicionar Nova Fase de Marketing")
        
        col1, col2 = st.columns(2)
        
        with col1:
            numero_fase = st.number_input("Número da Fase", min_value=1, max_value=10, value=1, step=1)
            nome_fase = st.text_input("Nome da Fase", placeholder="Ex: Validação, Crescimento, Escala")
            mes_inicio = st.number_input("Mês de Início", min_value=1, step=1, value=1)
            mes_fim = st.number_input("Mês de Fim (0 = sem fim)", min_value=0, step=1, value=0)
        
        with col2:
            tipo_orcamento_map = {
                "Fixo Mensal": "fixo",
                "% Lucro Bruto": "percentual_lucro",
                "% Receita": "percentual_receita"
            }
            tipo_orcamento_label = st.selectbox(
                "Tipo de Orçamento",
                list(tipo_orcamento_map.keys()),
                help="Como o orçamento será calculado"
            )
            tipo_orcamento_value = tipo_orcamento_map[tipo_orcamento_label]

            if tipo_orcamento_value == "fixo":
                valor_orcamento = st.number_input("Valor Fixo (R$/mês)", min_value=0.0, step=100.0, value=1000.0)
            else:
                valor_orcamento = st.slider("Percentual (%)", min_value=0, max_value=100, value=25, step=5)
        
        descricao_fase = st.text_area("Descrição/Estratégia", 
                                      placeholder="Ex: Foco em SEO e marketing de conteúdo orgânico")
        
        submitted = st.form_submit_button("➕ Adicionar Fase", use_container_width=True)
        
        if submitted:
            if not nome_fase:
                st.error("Nome da fase é obrigatório")
            else:
                valor_final = valor_orcamento / 100.0 if tipo_orcamento_value != 'fixo' else valor_orcamento
                nova_fase = FaseMarketing(
                    numero=numero_fase,
                    nome=nome_fase,
                    mes_inicio=mes_inicio,
                    mes_fim=mes_fim if mes_fim > 0 else None,
                    tipo_orcamento=tipo_orcamento_value,
                    valor=valor_final,
                    descricao=descricao_fase
                )
                if not hasattr(st.session_state.config, 'fases_marketing'):
                    st.session_state.config.fases_marketing = []
                st.session_state.config.fases_marketing.append(nova_fase)
                # Ordena por número
                st.session_state.config.fases_marketing.sort(key=lambda x: x.numero)
                salvar_config()
                st.rerun()
    
    # CAC Meta
    with st.expander("🎯 CAC Meta & Análise", expanded=False):
        st.markdown("Defina o CAC meta para análises de eficiência")
        
        cac_meta = st.number_input(
            "CAC Pago Meta (R$)",
            min_value=0.0,
            step=50.0,
            value=float(st.session_state.config.cac_pago_meta),
            help="CAC meta para canais pagos (usado em análises LTV/CAC)"
        )
        st.session_state.config.cac_pago_meta = cac_meta

# ============================================================================
# TAB 7: EQUIPE & PESSOAL
# ============================================================================

with tab7:
    st.markdown('<div class="section-header">👥 Planejamento de Equipe</div>', unsafe_allow_html=True)
    
    # Salário do Fundador
    with st.expander("💼 Salário do Fundador", expanded=True):
        st.markdown("Configure quando e quanto o fundador começará a receber")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ativar_fundador = st.checkbox(
                "Ativar Salário do Fundador",
                value=st.session_state.config.ativar_fundador
            )
            st.session_state.config.ativar_fundador = ativar_fundador
        
        if ativar_fundador:
            with col2:
                salario_fundador = st.number_input(
                    "Salário Mensal (R$)",
                    min_value=0.0,
                    step=500.0,
                    value=float(st.session_state.config.salario_fundador_valor),
                    help="Salário do fundador quando as condições forem atingidas"
                )
                st.session_state.config.salario_fundador_valor = salario_fundador
            
            col1, col2 = st.columns(2)
            with col1:
                mes_inicio_ideal = st.number_input(
                    "Mês Início Ideal",
                    min_value=1,
                    max_value=60,
                    value=int(st.session_state.config.salario_fundador_mes_inicio_ideal),
                    help="A partir de qual mês considerar pagar"
                )
                st.session_state.config.salario_fundador_mes_inicio_ideal = mes_inicio_ideal
            
            with col2:
                caixa_minimo = st.number_input(
                    "Caixa Mínimo de Segurança (R$)",
                    min_value=0.0,
                    step=1000.0,
                    value=float(st.session_state.config.salario_fundador_caixa_minimo_seguranca),
                    help="Só paga se caixa estiver acima deste valor"
                )
                st.session_state.config.salario_fundador_caixa_minimo_seguranca = caixa_minimo
    
    st.markdown("---")
    
    # Cargos Planejados
    st.markdown("### 📋 Cargos Planejados")
    
    if st.session_state.config.cargos_planejados:
        st.markdown("**Cargos Cadastrados:**")
        
        for i, cargo in enumerate(st.session_state.config.cargos_planejados):
            with st.expander(f"{cargo.cargo_funcao} ({cargo.tipo.value})", expanded=False):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                col1.write(f"**Salário:** {formatar_moeda(cargo.salario_base)}")
                if cargo.tipo.value == 'clt':
                    col1.caption(f"+ Encargos {cargo.encargos_percentual*100:.0f}% = {formatar_moeda(cargo.salario_base * (1 + cargo.encargos_percentual))}")
                
                # Gatilhos
                if cargo.gatilhos_contratacao:
                    gatilhos_str = []
                    for g in cargo.gatilhos_contratacao:
                        if g.tipo == TipoGatilho.MRR:
                            gatilhos_str.append(f"MRR > {formatar_moeda(g.valor)}")
                        elif g.tipo == TipoGatilho.USUARIOS:
                            gatilhos_str.append(f"Usuários > {g.valor:.0f}")
                        elif g.tipo == TipoGatilho.LUCRO:
                            gatilhos_str.append(f"Lucro > {formatar_moeda(g.valor)}")
                        elif g.tipo == TipoGatilho.MES:
                            gatilhos_str.append(f"Mês {g.valor:.0f}")
                    
                    col2.write(f"**Contratar quando:**")
                    col2.caption(" OU ".join(gatilhos_str))
                else:
                    col2.write(f"**Contratar:** Mês {cargo.mes_contratacao_manual or 1}")
                
                if col3.button("🗑️", key=f"del_cargo_{i}"):
                    st.session_state.config.cargos_planejados.pop(i)
                    st.rerun()
    
    else:
        st.info("Nenhum cargo planejado. Adicione o primeiro abaixo.")
    
    st.markdown("---")
    
    # Formulário para adicionar cargo
    with st.form("form_add_cargo", clear_on_submit=True):
        st.subheader("Adicionar Novo Cargo")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cargo_nome = st.text_input("Nome do Cargo/Função", placeholder="Ex: Dev Backend Sênior")
            tipo_pessoa = st.selectbox("Tipo de Contratação", ["CLT", "PJ"])
        
        with col2:
            salario = st.number_input("Salário Base / Valor Mensal (R$)", min_value=0.0, step=500.0, value=8000.0)
        
        with col3:
            if tipo_pessoa == "CLT":
                encargos = st.slider("Encargos % (CLT)", min_value=0, max_value=120, value=68) / 100
            else:
                encargos = 0.0
        
        st.markdown("**Gatilho para Contratação:**")
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            tipo_gatilho = st.selectbox(
                "Contratar quando...",
                ["MRR atingir valor", "Usuários atingir quantidade", "Lucro atingir valor", "Mês específico"]
            )
        
        with col_g2:
            if tipo_gatilho == "Mês específico":
                valor_gatilho = st.number_input("Mês", min_value=1, max_value=60, value=12, step=1)
            else:
                valor_gatilho = st.number_input(f"Valor para '{tipo_gatilho}'", min_value=0.0, step=100.0, value=50000.0)
        
        submitted = st.form_submit_button("➕ Adicionar Cargo ao Planejamento", use_container_width=True)
        
        if submitted:
            if not cargo_nome or cargo_nome == "Ex: Dev Backend Sênior":
                st.error("Por favor, insira um nome para o cargo.")
            else:
                # Mapeia tipo de gatilho
                tipo_gatilho_enum = {
                    "MRR atingir valor": TipoGatilho.MRR,
                    "Usuários atingir quantidade": TipoGatilho.USUARIOS,
                    "Lucro atingir valor": TipoGatilho.LUCRO,
                    "Mês específico": TipoGatilho.MES
                }[tipo_gatilho]
                
                gatilho = GatilhoContratacao(tipo=tipo_gatilho_enum, valor=valor_gatilho)
                
                novo_cargo = Cargo(
                    nome=cargo_nome,
                    cargo_funcao=cargo_nome,
                    tipo=TipoPessoa.CLT if tipo_pessoa == "CLT" else TipoPessoa.PJ,
                    salario_base=salario,
                    encargos_percentual=encargos,
                    gatilhos_contratacao=[gatilho]
                )
                
                st.session_state.config.cargos_planejados.append(novo_cargo)
                salvar_config()
                st.rerun()

# ============================================================================
# TAB 8: CONFIGURAÇÕES GERAIS
# ============================================================================

with tab8:
    st.markdown('<div class="section-header">⚙️ Configurações Gerais</div>', unsafe_allow_html=True)
    
    # Ferramentas SaaS
    with st.expander("🛠️ Ferramentas SaaS", expanded=True):
        st.markdown("Gerencie as ferramentas e serviços que sua empresa utiliza")
        
        if st.session_state.config.ferramentas_saas:
            st.markdown("**Ferramentas Cadastradas:**")
            
            # Agrupa por categoria
            categorias = {}
            for ferramenta in st.session_state.config.ferramentas_saas:
                cat = ferramenta.categoria.value if hasattr(ferramenta.categoria, 'value') else str(ferramenta.categoria)
                if cat not in categorias:
                    categorias[cat] = []
                categorias[cat].append(ferramenta)
            
            # Mostra por categoria
            for categoria, ferramentas in categorias.items():
                st.markdown(f"**{categoria.upper()}:**")
                for idx, ferramenta in enumerate(ferramentas):
                    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                    col1.write(f"• {ferramenta.nome}")
                    col2.write(f"{formatar_moeda(ferramenta.custo_mensal)}/mês")
                    col3.write("✅" if ferramenta.ativa else "❌")
                    
                    # Botão para ativar/desativar
                    if col4.button("🔄", key=f"toggle_tool_{ferramenta.nome}_{idx}"):
                        ferramenta.ativa = not ferramenta.ativa
                        salvar_config()
                        st.rerun()
            
            # Total
            total_ferramentas = sum([f.custo_mensal for f in st.session_state.config.ferramentas_saas if f.ativa])
            st.metric("Total Ferramentas Ativas", formatar_moeda(total_ferramentas))
        
        else:
            st.info("Nenhuma ferramenta cadastrada")
        
        st.markdown("---")
        
        # Form para adicionar ferramenta
        with st.form("form_add_tool", clear_on_submit=True):
            st.subheader("Adicionar Nova Ferramenta")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                nome_tool = st.text_input("Nome da Ferramenta", placeholder="Ex: GitHub Copilot")
            
            with col2:
                categoria_tool = st.selectbox(
                    "Categoria",
                    ["DEV", "SEGURANCA", "GESTAO", "COMUNICACAO", "DESIGN", "IA", "INFRA", "OUTROS"]
                )
            
            with col3:
                custo_tool = st.number_input("Custo Mensal (R$)", min_value=0.0, step=10.0, value=100.0)
            
            col1, col2 = st.columns(2)
            with col1:
                mes_inicio_tool = st.number_input("Mês de Início", min_value=1, step=1, value=1)
            
            with col2:
                essencial_tool = st.checkbox("Essencial", value=True, help="Ferramenta crítica para operação")
            
            submitted = st.form_submit_button("➕ Adicionar Ferramenta", use_container_width=True)
            
            if submitted:
                if not nome_tool:
                    st.error("Nome da ferramenta é obrigatório")
                else:
                    # Mapeia categoria
                    cat_map = {
                        "DEV": CategoriaFerramenta.DEV,
                        "SEGURANCA": CategoriaFerramenta.SEGURANCA,
                        "GESTAO": CategoriaFerramenta.GESTAO,
                        "COMUNICACAO": CategoriaFerramenta.COMUNICACAO,
                        "DESIGN": CategoriaFerramenta.DESIGN,
                        "IA": CategoriaFerramenta.IA,
                        "INFRA": CategoriaFerramenta.INFRA,
                        "OUTROS": CategoriaFerramenta.OUTROS
                    }
                    
                    nova_ferramenta = FerramentaSaaS(
                        nome=nome_tool,
                        categoria=cat_map[categoria_tool],
                        custo_mensal=custo_tool,
                        mes_inicio=mes_inicio_tool,
                        essencial=essencial_tool,
                        ativa=True
                    )
                    
                    st.session_state.config.ferramentas_saas.append(nova_ferramenta)
                    salvar_config()
                    st.rerun()
    
    # Escritório
    with st.expander("🏢 Escritório & Operação", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            ativar_escritorio = st.checkbox(
                "Ativar Custos de Escritório",
                value=st.session_state.config.ativar_escritorio
            )
            st.session_state.config.ativar_escritorio = ativar_escritorio
        
        if ativar_escritorio:
            with col2:
                mes_inicio_escritorio = st.number_input(
                    "Mês de Início",
                    min_value=1,
                    max_value=60,
                    value=int(st.session_state.config.escritorio_mes_inicio if st.session_state.config.escritorio_mes_inicio < 999 else 12),
                    help="Quando começar a ter escritório"
                )
                st.session_state.config.escritorio_mes_inicio = mes_inicio_escritorio
            
            st.markdown("**Componentes do Custo:**")
            col1, col2 = st.columns(2)
            
            with col1:
                aluguel = st.number_input("Aluguel (R$/mês)", min_value=0.0, step=100.0, 
                                         value=float(st.session_state.config.escritorio_aluguel_mensal))
                st.session_state.config.escritorio_aluguel_mensal = aluguel
                
                condominio = st.number_input("Condomínio (R$/mês)", min_value=0.0, step=50.0,
                                            value=float(st.session_state.config.escritorio_condominio_mensal))
                st.session_state.config.escritorio_condominio_mensal = condominio
            
            with col2:
                agua_luz = st.number_input("Água + Luz (R$/mês)", min_value=0.0, step=50.0,
                                          value=float(st.session_state.config.escritorio_agua_luz_mensal))
                st.session_state.config.escritorio_agua_luz_mensal = agua_luz
                
                internet = st.number_input("Internet (R$/mês)", min_value=0.0, step=50.0,
                                          value=float(st.session_state.config.escritorio_internet_mensal))
                st.session_state.config.escritorio_internet_mensal = internet
            
            outros = st.number_input("Outros (R$/mês)", min_value=0.0, step=50.0,
                                    value=float(st.session_state.config.escritorio_outros_mensal))
            st.session_state.config.escritorio_outros_mensal = outros
            
            total_escritorio = aluguel + condominio + agua_luz + internet + outros
            st.metric("Total Escritório", formatar_moeda(total_escritorio))
    
    # Serviços Profissionais
    with st.expander("💼 Serviços Profissionais", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            ativar_servicos = st.checkbox(
                "Ativar Serviços Profissionais",
                value=st.session_state.config.ativar_servicos_profs
            )
            st.session_state.config.ativar_servicos_profs = ativar_servicos
        
        if ativar_servicos:
            st.markdown("**Contabilidade:**")
            col1, col2 = st.columns(2)
            with col1:
                contab_mensal = st.number_input(
                    "Contabilidade (R$/mês)",
                    min_value=0.0,
                    step=100.0,
                    value=float(st.session_state.config.contabilidade_mensal)
                )
                st.session_state.config.contabilidade_mensal = contab_mensal
            
            with col2:
                contab_inicio = st.number_input(
                    "Início (mês)",
                    min_value=1,
                    max_value=60,
                    value=int(st.session_state.config.contabilidade_mes_inicio)
                )
                st.session_state.config.contabilidade_mes_inicio = contab_inicio
            
            st.markdown("**Advogado:**")
            col1, col2 = st.columns(2)
            with col1:
                advogado_mensal = st.number_input(
                    "Advogado (R$/mês)",
                    min_value=0.0,
                    step=100.0,
                    value=float(st.session_state.config.advogado_retainer_mensal)
                )
                st.session_state.config.advogado_retainer_mensal = advogado_mensal
            
            with col2:
                advogado_inicio = st.number_input(
                    "Início (mês)",
                    min_value=1,
                    max_value=60,
                    value=int(st.session_state.config.advogado_mes_inicio if st.session_state.config.advogado_mes_inicio < 999 else 12)
                )
                st.session_state.config.advogado_mes_inicio = advogado_inicio
            
            st.markdown("**Consultorias/Outros:**")
            consultorias = st.number_input(
                "Consultorias Outras (R$/mês)",
                min_value=0.0,
                step=100.0,
                value=float(st.session_state.config.consultorias_outras_mensal)
            )
            st.session_state.config.consultorias_outras_mensal = consultorias
    
    # Depreciação
    with st.expander("📉 Depreciação & CAPEX", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            ativar_deprec = st.checkbox(
                "Ativar Depreciação",
                value=st.session_state.config.ativar_depreciacao
            )
            st.session_state.config.ativar_depreciacao = ativar_deprec
        
        if ativar_deprec:
            st.markdown("**Ativos Depreciáveis:**")
            
            if st.session_state.config.ativos_depreciaveis:
                for idx, ativo in enumerate(st.session_state.config.ativos_depreciaveis):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    col1.write(f"• {ativo.nome}")
                    col2.write(f"{formatar_moeda(ativo.valor_aquisicao)} / {ativo.meses_depreciacao} meses")
                    col3.write("✅" if ativo.ativo else "❌")
            else:
                st.info("Nenhum ativo cadastrado")

# ============================================================================
# FOOTER & AÇÕES
# ============================================================================

st.markdown("---")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("💡 **Dica:** Todas as alterações são salvas automaticamente no estado da sessão")

with col2:
    if st.button("🔄 Resetar para Padrão", use_container_width=True):
        st.session_state.config = criar_config_padrao()
        st.success("✅ Configuração resetada!")
        st.rerun()

with col3:
    if st.button("💾 Exportar Config", use_container_width=True):
        st.info("🚧 Export será implementado em breve")

st.markdown("---")
st.caption("SAM Financial Model v4.0 | Configurações Avançadas")