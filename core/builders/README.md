# 🔧 SAM Financial Model - Sistema de Builders

Documentação completa do sistema de configuração avançada via Builders.

---

## 📚 Índice

1. [Visão Geral](#visão-geral)
2. [Builders Disponíveis](#builders-disponíveis)
3. [Quick Start](#quick-start)
4. [Guia Detalhado por Builder](#guia-detalhado)
5. [Exemplos Práticos](#exemplos-práticos)
6. [Integração com Streamlit](#integração-com-streamlit)

---

## 🎯 Visão Geral

O sistema de Builders permite configurar **TODOS os aspectos** do modelo financeiro SAM de forma programática, modular e reutilizável.

### Por que Builders?

**Antes (config manual):**
```python
config = ConfigFinanceira()
config.visitantes_mes_1 = 1000
config.taxa_conversao_trial = 0.05
config.churn_mensal = 0.04
# ... 50+ linhas de configuração manual
```

**Depois (com builders):**
```python
scenario = ScenarioBuilder("SAM - Base")
scenario.configurar_funil(1000, 0.20, 0.05, 0.15, 0.04)
scenario.usar_canais(criar_estrategia_sam_canais)
scenario.usar_infra(criar_infra_sam)
config = scenario.build()
```

### Vantagens

✅ **Modular** - Cada builder cuida de uma área específica  
✅ **Reutilizável** - Crie templates e compartilhe  
✅ **Validação** - Builders validam dados antes de aplicar  
✅ **Versionamento** - Salve cenários em JSON  
✅ **Fluent Interface** - Encadeamento de métodos  
✅ **Type-Safe** - Classes com dataclasses  

---

## 🧩 Builders Disponíveis

| # | Builder | Propósito | Arquivo |
|---|---------|-----------|---------|
| 1 | **ChannelsBuilder** | Canais de aquisição (SEO, Ads, Afiliados) | `channels_builder.py` |
| 2 | **InfraBuilder** | Infraestrutura escalável em tiers | `infra_builder.py` |
| 3 | **TeamBuilder** | Equipe com gatilhos de contratação | `team_builder.py` |
| 4 | **ToolsBuilder** | Stack de ferramentas SaaS | `tools_builder.py` |
| 5 | **MarketingBuilder** | Marketing em 4 fases | `marketing_builder.py` |
| 6 | **COGSBuilder** | Custos variáveis completos | `cogs_builder.py` |
| 7 | **RevenueBuilder** | Modelo de receita (planos, upsell) | `revenue_builder.py` |
| 8 | **CapitalBuilder** | Aportes e financiamento | `capital_builder.py` |
| 9 | **RiskBuilder** | Cenários de risco e contingência | `risk_builder.py` |
| 10 | **TaxBuilder** | Impostos progressivos | `tax_builder.py` |
| 11 | **ScenarioBuilder** | Orquestrador de cenários completos | `scenario_builder.py` |

---

## 🚀 Quick Start

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-repo/sam-financial-model
cd sam-financial-model

# Instale dependências
pip install -r requirements.txt

# Execute exemplo completo
python examples/configurar_sam_completo.py
```

### Uso Básico

```python
from core.builders.scenario_builder import ScenarioBuilder

# Criar cenário
scenario = ScenarioBuilder("Meu Cenário")

# Configurar funil
scenario.configurar_funil(
    visitantes_mes_1=1000,
    crescimento_mensal=0.20,
    conv_trial=0.05,
    conv_pagante=0.15,
    churn=0.04
)

# Configurar receita
scenario.configurar_receita(
    planos=[
        ("Lite", 70, 0.50),
        ("Pro", 150, 0.50)
    ]
)

# Build
config = scenario.build()

# Executar projeção
from core.engine import MotorProjecaoFinanceira
motor = MotorProjecaoFinanceira(config)
df = motor.executar_projecao(meses=36)
```

---

## 📖 Guia Detalhado por Builder

### 1️⃣ ChannelsBuilder - Canais de Aquisição

**Problema:** CAC e conversão variam drasticamente por canal.

**Solução:** Configure cada canal com suas métricas específicas.

```python
from core.builders.channels_builder import ChannelsBuilder

builder = ChannelsBuilder(config)

# SEO Orgânico: mix=40%, conv=8%→20%, CAC=R$200
builder.add_canal_organico(
    "SEO & Content",
    percentual_trafego=0.40,
    taxa_conversao_trial=0.08,
    taxa_conversao_pagante=0.20,
    cac_medio=200
)

# Google Ads: mix=30%, conv=4%→15%, CAC=R$500
builder.add_canal_pago(
    "Google Ads",
    percentual_trafego=0.30,
    taxa_conversao_trial=0.04,
    taxa_conversao_pagante=0.15,
    cac_medio=500,
    cpc=2.50
)

# Programa de Afiliados: mix=20%, comissão=20%
builder.add_canal_afiliado(
    "Afiliados",
    percentual_trafego=0.20,
    taxa_conversao_trial=0.12,
    taxa_conversao_pagante=0.30,
    cac_medio=100,
    comissao_percentual=0.20
)

# Referral: mix=10%, CAC mínimo
builder.add_canal_referral(
    "Indicação",
    percentual_trafego=0.10,
    taxa_conversao_trial=0.15,
    taxa_conversao_pagante=0.35,
    cac_medio=50
)

config = builder.build()

# Métricas calculadas automaticamente:
print(f"CAC Blended: R$ {builder.calcular_cac_blended():.2f}")
print(f"CAC Pago: R$ {builder.calcular_cac_pago():.2f}")
```

**Resultado:**
- CAC Blended (todos os canais): ~R$ 212
- CAC Pago (só ads): R$ 500
- Conversão média ponderada automática

---

### 2️⃣ InfraBuilder - Infraestrutura Escalável

**Problema:** Custos de infra mudam drasticamente conforme você escala.

**Solução:** Configure tiers com transição automática.

```python
from core.builders.infra_builder import InfraBuilder, TipoComponente

builder = InfraBuilder(config)

# TIER 1: 0-100 usuários = R$209/mês
builder.criar_tier(1, "Validação", 0, 100)
builder.add_componente("VPS Principal", TipoComponente.VPS, 55, provider="Hostinger")
builder.add_componente("VPS MT5", TipoComponente.VPS, 150, provider="AWS")
builder.add_componente("Domínio", TipoComponente.DOMINIO, 4)

# TIER 2: 101-500 usuários = R$5.650/mês
builder.criar_tier(2, "Escala", 101, 500)
builder.add_componente("API Cedro", TipoComponente.API_EXTERNA, 5000)
builder.add_componente("VPS Robusta", TipoComponente.VPS, 500)
builder.add_componente("Backup S3", TipoComponente.BACKUP, 50)

# TIER 3: 501+ usuários = Tier 2 + R$1,50/usuário
builder.criar_tier(3, "Hiperescala", 501, 999999, custo_por_usuario=1.50)

config = builder.build()

# Testar custos
tier, custo = builder.calcular_custo_para_usuarios(250)
print(f"250 usuários → Tier {tier} → R$ {custo:,.2f}/mês")
```

**Resultado:**
- 50 usuários → Tier 1 → R$ 209/mês
- 250 usuários → Tier 2 → R$ 5.650/mês
- 750 usuários → Tier 3 → R$ 6.025/mês (5.650 + 250×1.50)

---

### 3️⃣ TeamBuilder - Equipe com Gatilhos

**Problema:** Quando contratar? Como escalar salários?

**Solução:** Gatilhos automáticos + fases salariais.

```python
from core.builders.team_builder import TeamBuilder

builder = TeamBuilder(config)

# Fundador com 3 fases salariais + pró-labore
builder.add_fundador("João Silva", "CEO", equity=0.70) \
    .fase_sem_salario(1, 6) \
    .fase_salario_minimo(7, 12, 3000) \
    .fase_salario_pleno(13, None, 8000, gatilho_mrr=30000) \
    .com_pro_labore(0.10, gatilho_lucro=10000)

# Dev Backend: contratar quando MRR > R$50k
builder.add_clt("Dev Backend", "Engenheiro", 8000) \
    .quando_mrr_atingir(50000) \
    .com_beneficios(vr=500, vt=300, plano=400) \
    .com_reajuste_anual(0.08)

# Community Manager: contratar quando usuários > 1000
builder.add_clt("Community Manager", "CS", 5000) \
    .quando_usuarios_atingir(1000) \
    .com_beneficios(vr=500, vt=300, plano=300)

# Designer PJ: contratar no mês 6
builder.add_pj("Designer", "Designer", 3000) \
    .no_mes(6)

config = builder.build()
```

**Resultado:**
- Fundador: R$0 (mês 1-6) → R$3k (mês 7-12) → R$8k (mês 13+, se MRR>30k) + pró-labore
- Dev Backend: contratado automaticamente quando MRR atingir R$50k
- Timeline de contratações visível nos relatórios

---

### 4️⃣ MarketingBuilder - 4 Fases

**Problema:** Orçamento de marketing muda ao longo do tempo.

**Solução:** Configure fases com regras diferentes.

```python
from core.builders.marketing_builder import MarketingBuilder

builder = MarketingBuilder(config)

# Fase 1: Validação (meses 1-6) - Orçamento fixo
builder.fase_validacao(1, 6, orcamento_fixo=1000)

# Fase 2: Crescimento (meses 7-18) - 25% do lucro bruto
builder.fase_crescimento(7, 18, percentual=0.25, base='percentual_lucro')

# Fase 3: Escala (meses 19-36) - 20% da receita
builder.fase_escala(19, 36, percentual_receita=0.20)

# Fase 4: Maturidade (mês 37+) - CAC target R$300
builder.fase_maturidade(37, cac_target=300)

config = builder.build()
```

**Resultado:**
- Mês 3: R$1.000 fixo (Fase 1)
- Mês 12: R$5.000 (25% do lucro bruto de R$20k)
- Mês 24: R$18.000 (20% da receita de R$90k)
- Mês 40: Otimizado para CAC=R$300

---

### 5️⃣ ScenarioBuilder - Orquestrador

**Problema:** Como combinar todos os builders?

**Solução:** ScenarioBuilder como orquestrador.

```python
from core.builders.scenario_builder import ScenarioBuilder

# Criar cenário
scenario = ScenarioBuilder("SAM - Base", "Projeção realista")

# Aplicar builders
scenario \
    .configurar_capital_basico(8000, 1800, 12) \
    .configurar_funil(1000, 0.20, 0.05, 0.15, 0.04) \
    .configurar_receita([("Lite", 70, 0.5), ("Pro", 150, 0.5)]) \
    .usar_canais(criar_estrategia_sam_canais) \
    .usar_infra(criar_infra_sam) \
    .usar_equipe(criar_equipe_sam)

# Build
config = scenario.build()

# Salvar
scenario.salvar("data/scenarios/sam_base.json")

# Criar variações
scenario_pessimista = scenario.criar_pessimista()
scenario_otimista = scenario.criar_otimista()
```

---

## 💡 Exemplos Práticos

### Exemplo 1: Configuração Mínima

```python
from core.builders.scenario_builder import ScenarioBuilder

scenario = ScenarioBuilder("Startup Simples")
scenario.configurar_funil(500, 0.15, 0.05, 0.20, 0.05)
scenario.configurar_receita([("Básico", 50, 1.0)])
config = scenario.build()
```

### Exemplo 2: Comparar Cenários

```python
from core.builders.scenario_builder import GerenciadorCenarios

gerenciador = GerenciadorCenarios()

# Carregar cenários
base = gerenciador.carregar_cenario("sam_base")
pess = gerenciador.carregar_cenario("sam_pessimista")
otim = gerenciador.carregar_cenario("sam_otimista")

# Comparar
gerenciador.imprimir_comparacao([
    "sam_base",
    "sam_pessimista",
    "sam_otimista"
])
```

### Exemplo 3: Cenário Customizado

```python
scenario = ScenarioBuilder("E-commerce SaaS")

# Receita com 3 planos
scenario.configurar_receita([
    ("Starter", 29, 0.60),
    ("Pro", 79, 0.30),
    ("Enterprise", 199, 0.10)
])

# Canais diferentes
def canais_ecommerce(config):
    builder = ChannelsBuilder(config)
    builder.add_canal_pago("Facebook Ads", 0.50, 0.03, 0.12, 400)
    builder.add_canal_pago("Instagram Ads", 0.30, 0.04, 0.15, 450)
    builder.add_canal_organico("SEO", 0.20, 0.10, 0.25, 150)
    return builder.build()

scenario.usar_canais(canais_ecommerce)
config = scenario.build()
```

---

## 🖥️ Integração com Streamlit

### Carregar Cenário no App

```python
# app/main.py

import streamlit as st
from core.builders.scenario_builder import GerenciadorCenarios

# Sidebar: Seletor de cenário
gerenciador = GerenciadorCenarios()
cenarios_disponiveis = gerenciador.listar_cenarios()

cenario_selecionado = st.sidebar.selectbox(
    "Cenário",
    [c['nome'] for c in cenarios_disponiveis]
)

# Carregar
if st.sidebar.button("Carregar Cenário"):
    scenario = gerenciador.carregar_cenario(cenario_selecionado)
    st.session_state.config = scenario.build()
    st.success(f"✅ Cenário '{cenario_selecionado}' carregado!")
```

### Editor Interativo de Builder

```python
# app/pages/Config_Avancada.py

st.title("⚙️ Configuração Avançada")

tab_canais, tab_infra, tab_equipe = st.tabs(["Canais", "Infra", "Equipe"])

with tab_canais:
    st.subheader("Canais de Aquisição")
    
    # UI para adicionar canais
    with st.expander("➕ Adicionar Canal"):
        nome = st.text_input("Nome do Canal")
        tipo = st.selectbox("Tipo", ["Orgânico", "Pago", "Afiliado", "Referral"])
        mix = st.slider("Mix de Tráfego (%)", 0, 100, 25) / 100
        cac = st.number_input("CAC Médio (R$)", 0, 5000, 300)
        
        if st.button("Adicionar"):
            # Adiciona ao builder
            builder = ChannelsBuilder(st.session_state.config)
            if tipo == "Orgânico":
                builder.add_canal_organico(nome, mix, 0.08, 0.20, cac)
            # ... outros tipos
            st.session_state.config = builder.build()
            st.success(f"Canal '{nome}' adicionado!")
    
    # Mostrar canais existentes
    if hasattr(st.session_state.config, 'canais_aquisicao'):
        for canal in st.session_state.config.canais_aquisicao:
            with st.expander(f"📢 {canal.nome}"):
                st.write(f"Tipo: {canal.tipo.value}")
                st.write(f"Mix: {canal.percentual_trafego*100:.1f}%")
                st.write(f"CAC: R$ {canal.cac_medio:,.2f}")
                if st.button(f"Remover {canal.nome}"):
                    # Remove canal
                    pass
```

---

## 🎓 Boas Práticas

### 1. Use Builders para Complexidade

❌ **Não faça:**
```python
config.visitantes_mes_1 = 1000
config.taxa_conversao_trial = 0.05
# ... 50+ linhas
```

✅ **Faça:**
```python
scenario.configurar_funil(1000, 0.20, 0.05, 0.15, 0.04)
```

### 2. Salve Cenários Importantes

```python
# Sempre salve configurações de produção
scenario.salvar("data/scenarios/producao_2025_q1.json")
```

### 3. Valide Antes de Aplicar

```python
builder = ChannelsBuilder(config)
# ... adiciona canais

# Valida
erros = builder.validar()
if erros:
    print("Erros encontrados:")
    for erro in erros:
        print(f"  • {erro}")
else:
    config = builder.build()
```

### 4. Use Funções Reutilizáveis

```python
# Crie templates
def criar_canais_b2b_padrao(config):
    builder = ChannelsBuilder(config)
    builder.add_canal_pago("LinkedIn Ads", 0.40, 0.06, 0.25, 800)
    builder.add_canal_organico("SEO B2B", 0.40, 0.10, 0.30, 300)
    builder.add_canal_referral("Referral", 0.20, 0.15, 0.40, 100)
    return builder.build()

# Reutilize
scenario.usar_canais(criar_canais_b2b_padrao)
```

### 5. Documente Seus Cenários

```python
scenario = ScenarioBuilder(
    "SAM - Lançamento Q1 2025",
    descricao="""
    Projeção para lançamento no Q1 2025:
    - Foco em SEO orgânico (60%)
    - Orçamento marketing conservador (R$1k/mês)
    - Contratações apenas após validação (MRR>50k)
    - Churn alvo: 4% (mercado brasileiro)
    """
)
```

---

## 🐛 Troubleshooting

### Erro: "Soma dos percentuais é 105%"

**Problema:** Mix de canais/planos não soma 100%

**Solução:**
```python
# Certifique-se que soma = 1.0
builder.add_canal_organico("SEO", 0.40, ...)  # 40%
builder.add_canal_pago("Ads", 0.30, ...)      # 30%
builder.add_canal_afiliado("Afiliados", 0.20, ...)  # 20%
builder.add_canal_referral("Referral", 0.10, ...)   # 10%
# Total: 100% ✅
```

### Erro: "Gap entre Tier 1 e Tier 2"

**Problema:** Ranges de tiers não são contíguos

**Solução:**
```python
builder.criar_tier(1, "Tier 1", 0, 100)      # 0-100
builder.criar_tier(2, "Tier 2", 101, 500)    # 101-500 ✅
# NÃO: builder.criar_tier(2, "Tier 2", 150, 500)  # Gap de 101-149 ❌
```

### Erro: "Funcionário não contratado"

**Problema:** Gatilhos muito agressivos

**Solução:**
```python
# Verifique se gatilhos são realistas
builder.add_clt("Dev", "Dev", 8000) \
    .quando_mrr_atingir(50000)  # MRR real atinge isso?

# Ou use contratação manual
builder.add_clt("Dev", "Dev", 8000) \
    .no_mes(12)  # Contrata no mês 12 independente de gatilhos
```

---

## 📝 Changelog

### v4.0.0 (2025-01-15)
- ✅ Sistema completo de 11 builders
- ✅ ScenarioBuilder como orquestrador
- ✅ Save/Load de cenários em JSON
- ✅ Comparação de cenários
- ✅ Validação em todos os builders
- ✅ Fluent interface
- ✅ Documentação completa

---

## 🤝 Contribuindo

Para adicionar um novo builder:

1. Crie arquivo `core/builders/novo_builder.py`
2. Implemente classe `NovoBuilder` com método `build()`
3. Adicione ao `__init__.py`
4. Adicione método `usar_novo()` no `ScenarioBuilder`
5. Documente no README

---

## 📧 Suporte

- **Issues:** https://github.com/seu-repo/issues
- **Docs:** https://docs.sam-financial.com
- **Email:** suporte@sam-financial.com

---

**Desenvolvido com ❤️ para o SAM Financial Model v4.0**