# 🎯 Objetivo Principal

Estamos construindo um sistema profissional de projeção, análise e tomada de decisão, que transforma um fluxo caótico de planilhas em uma plataforma inteligente para prever o futuro financeiro de um negócio.

---

# 🏗️ Padrões Técnicos e Arquitetura

## Estrutura de 3 Camadas

```
CAMADA 1: CONFIGURAÇÃO AVANÇADA (Config Builder)
├── Sistema de "Builders" para cada categoria
├── Validação em tempo real
├── Templates salvos (cenários nomeados)
└── Import/Export JSON

CAMADA 2: ENGINE INTELIGENTE (Analytics Engine)
├── Cálculos base (já existe)
├── Detecção de anomalias
├── Geração de insights
├── Simulação de "E se...?" em tempo real
└── Cálculos de decomposição (cada valor sabe sua origem)

CAMADA 3: VISUALIZAÇÃO INTERATIVA (Smart Dashboard)
├── Dashboards temáticos (Receita, Custos, Caixa, Equipe)
├── Gráficos com drill-down
├── Filtros globais + filtros específicos
├── Exportação de cada visual
└── Modo "Apresentação" (para investidores)
```

## Estrutura de Arquivos (Nova)

```
SAM_Financial_Model_v4/
│
├── app/
│   ├── __init__.py
│   ├── main.py                     # Home + Router
│   ├── pages/
│   │   ├── 01_📊_Dashboard_Receita.py
│   │   ├── 02_💸_Dashboard_Custos.py
│   │   ├── 03_💰_Dashboard_Caixa.py
│   │   ├── 04_👥_Dashboard_Equipe.py
│   │   ├── 05_📢_Dashboard_Marketing.py
│   │   ├── 06_🎯_Unit_Economics.py
│   │   ├── 07_📈_Analise_Sensibilidade.py
│   │   ├── 08_🔄_Cohorts.py
│   │   ├── 09_🎲_Cenarios_MonteCarlo.py
│   │   ├── 10_📋_Tabelas.py
│   │   ├── 11_⚙️_Configuracoes.py
│   │   └── 12_📚_Glossario.py
│   │
│   ├── components/                 # NOVO: Componentes reutilizáveis
│   │   ├── __init__.py
│   │   ├── metrics.py              # Cartões de métricas
│   │   ├── charts.py               # Gráficos padrão
│   │   ├── tables.py               # Tabelas interativas
│   │   ├── filters.py              # Filtros globais
│   │   ├── drill_down.py           # Popups de drill-down
│   │   └── insights.py             # Sistema de insights
│   │
│   └── utils/                      # NOVO: Utilitários
│       ├── __init__.py
│       ├── formatters.py           # Formatação de valores
│       ├── validators.py           # Validação de inputs
│       └── exporters.py            # Export PDF/Excel/PowerPoint
│
├── core/
│   ├── __init__.py
│   ├── config.py                   # ✅ Expandir
│   ├── engine.py                   # ✅ Expandir
│   ├── analysis.py                 # ✅ Criar/Expandir
│   ├── glossary.py                 # ✅ OK
│   ├── visualizations.py           # ✅ Expandir
│   │
│   ├── builders/                   # NOVO: Configuradores
│   │   ├── __init__.py
│   │   ├── capital_builder.py      # Aportes, empréstimos
│   │   ├── revenue_builder.py      # Planos, upsell, add-ons
│   │   ├── cogs_builder.py         # Taxas, comissões
│   │   ├── infra_builder.py        # Tiers de infraestrutura
│   │   ├── marketing_builder.py    # Fases, canais
│   │   ├── team_builder.py         # Equipe + gatilhos
│   │   └── scenario_builder.py     # Cenários completos
│   │
│   ├── analytics/                  # NOVO: Análises avançadas
│   │   ├── __init__.py
│   │   ├── sensitivity.py          # Análise de sensibilidade
│   │   ├── montecarlo.py           # Simulação Monte Carlo
│   │   ├── cohorts.py              # Análise de cohorts
│   │   ├── forecasting.py          # Previsões avançadas
│   │   └── insights_engine.py      # Gerador de insights
│   │
│   └── risk/                       # NOVO: Gestão de riscos
│       ├── __init__.py
│       ├── risk_scenarios.py       # Cenários de risco
│       ├── contingency.py          # Planos de contingência
│       └── alerts.py               # Sistema de alertas
│
├── data/                           # NOVO: Armazenamento
│   ├── scenarios/                  # Cenários salvos (JSON)
│   ├── exports/                    # Relatórios exportados
│   └── templates/                  # Templates de config
│
├── tests/   
│   ├── test_config.py
│   ├── test_engine.py
│   ├── test_builders.py
│   ├── test_analytics.py
│   └── test_integration.py
│
├── notebooks/                      # Jupyter notebooks
│   ├── 01_overview.ipynb
│   ├── 02_engine_deep_dive.ipynb
│   ├── 03_montecarlo.ipynb
│   ├── 04_sensibilidade.ipynb
│   └── 05_case_studies.ipynb
│
├── docs/                           # NOVO: Documentação
│   ├── user_guide.md
│   ├── technical_docs.md
│   ├── api_reference.md
│   └── screenshots/
│
├── requirements.txt
├── setup.py
├── README.md
└── .streamlit/                     # NOVO: Config Streamlit
    └── config.toml                 # Tema, cores, etc.
```

---

# 🗺️ Roadmap Atual

Estamos iniciando a **Fase 1: Foundation (Semana 1-2)**.

**Objetivo da Fase:** Criar a base sólida da nova arquitetura e as interfaces de configuração avançada.

**Próximas Tarefas Principais:**
1.  Criar a estrutura de pastas completa (`core/builders`, `core/analytics`, `app/components`, etc.).
2.  Expandir `core/config.py` para incluir os novos campos detalhados.
3.  Criar os `Builders` básicos para capital, equipe, infra e marketing.
4.  Expandir `core/engine.py` para usar a lógica dos novos builders.

---

# ✍️ Diário de Bordo

**14/11/2025 - Sessão 2**
- **FEITO:** Corrigido um `ModuleNotFoundError` em todos os scripts de `builder` (`channels`, `infra`, `team`, `scenario`) para permitir a execução independente para testes. A correção envolveu a adição dinâmica do diretório raiz do projeto ao `sys.path`.
- **FEITO:** Continuada a refatoração da arquitetura, separando os builders que estavam aglomerados em `remaining_builders.py` para seus arquivos individuais, conforme o plano. Foram criados e preenchidos: `tools_builder.py`, `marketing_builder.py`, e `cogs_builder.py`.
- **PRÓXIMO PASSO:** Finalizar a separação dos builders restantes (`revenue`, `capital`, `risk`, `tax`) e remover o arquivo `remaining_builders.py`.

**14/11/2025 - Sessão 1**
- **FEITO:** Definimos o plano de trabalho e criamos o arquivo `CONTEXTO_E_DIARIO.md` para garantir a continuidade e consistência entre as sessões.
- **PRÓXIMO PASSO:** Iniciar a Fase 1 do plano de implementação, começando pela criação da nova estrutura de diretórios.
