# 🎯 ROADMAP DE IMPLEMENTAÇÃO DO SAM FINANCIAL MODEL

Este roadmap foi atualizado para refletir a nova arquitetura do frontend (React + TypeScript + Vite + Tailwind CSS) e o progresso do backend.

## Fase 1: Backend Core & API (CONCLUÍDO) ✅

### Objetivo: Motor de projeção financeiro desacoplado e acessível via API.

**Status:** Concluído. O backend FastAPI está funcional, expondo o endpoint `/projecao` para o frontend.

**Tarefas Principais Concluídas:**
- Desacoplamento completo do core (`core/`) do Streamlit.
- Centralização da lógica de análise (`core/analytics`).
- Centralização da lógica de visualização (`core/visualizations`).
- Implementação da API com FastAPI (`main.py`).
- Testes de integração do backend.

---

## Fase 2: Arquitetura e Setup do Novo Frontend (CONCLUÍDO) ✅

### Objetivo: Ambiente de desenvolvimento frontend configurado com a nova arquitetura.

**Status:** Concluído. O ambiente React foi configurado e a estrutura de pastas criada.

**Tarefas Principais Concluídas:**
- Definição da arquitetura de frontend (componentes, estado, API, gráficos).
- Reset e limpeza do ambiente frontend.
- Criação do projeto Vite + React + TypeScript.
- Configuração de dependências (`package.json`) para Tailwind CSS, Zustand, TanStack Query, React Hook Form, Zod, Recharts, Plotly.js.
- Criação da estrutura de diretórios detalhada (`src/app`, `src/pages`, `src/components`, `src/features`, `src/lib`).

---

## Fase 3: Fundação do Frontend - Layout e API Client (PRÓXIMO) 🚀

### Objetivo: Estrutura de layout básica e comunicação com o backend estabelecida.

**Estimativa:** 1 semana

**Tarefas:**

1.  **Implementar Cliente API (`src/lib/api/client.ts`)**
    -   Configurar `axios` com `baseURL` e `timeout`.
    -   Adicionar interceptors para logging e tratamento de erros (ex: `ValidationError`).
    -   Criar função `runProjection` para chamar o endpoint `/projecao`.
2.  **Configurar Provedores Globais (`src/app/providers.tsx`)**
    -   Configurar `QueryClientProvider` do TanStack Query.
    -   Configurar `Zustand` (se necessário um provedor).
3.  **Construir Componentes de Layout (`src/components/layout/`)**
    -   `AppLayout.tsx`: Layout principal da aplicação (sidebar + header + conteúdo).
    -   `Sidebar.tsx`: Componente de navegação lateral.
    -   `Header.tsx`: Componente do cabeçalho (título, breadcrumbs, ações globais).
4.  **Configurar Roteamento (`src/app/router.tsx`)**
    -   Configurar `react-router-dom` para as rotas principais (`/configuracao`, `/resultados`).
5.  **Componente Raiz (`src/app/App.tsx`)**
    -   Integrar `AppLayout` e o roteamento.

**Entregável:** Aplicação com layout básico e comunicação API funcional.

---

## Fase 4: Página de Configuração (Formulário Dinâmico) ⚙️

### Objetivo: Interface completa para entrada de dados do modelo financeiro.

**Estimativa:** 2-3 semanas

**Tarefas:**

1.  **Gerar Tipos Compartilhados (`src/lib/api/types.ts`)**
    -   Criar interfaces TypeScript para `ConfigFinanceira` e `ProjectionResponse` (espelhando o backend).
2.  **Desenvolver Componentes de Formulário Reutilizáveis (`src/components/forms/`)**
    -   `FormField.tsx`: Wrapper genérico para campos de formulário.
    -   `NumberInput.tsx`, `PercentageInput.tsx`, `CurrencyInput.tsx`: Inputs especializados.
    -   `FormSection.tsx`: Componente para agrupar campos em seções.
3.  **Implementar `configStore` (`src/features/configuration/stores/configStore.ts`)**
    -   Definir o estado para `ConfigFinanceira`, `isDirty`, `validationErrors`.
    -   Implementar ações para `setConfig`, `updateField`, `resetConfig`, `loadConfig`.
4.  **Criar `useConfigForm` Hook (`src/features/configuration/hooks/useConfigForm.ts`)**
    -   Integrar `React Hook Form` com `Zod` para validação.
    -   Sincronizar o estado do formulário com `configStore`.
5.  **Construir Seções da Página de Configuração (`src/pages/ConfigurationPage/sections/`)**
    -   `CapitalSection.tsx`, `RevenueSection.tsx`, `TeamSection.tsx`, `InfraSection.tsx`, `MarketingSection.tsx`, etc.
    -   Cada seção usará os componentes de formulário e o `useConfigForm` hook.
6.  **Página de Configuração (`src/pages/ConfigurationPage/ConfigurationPage.tsx`)**
    -   Montar todas as seções do formulário.
    -   Adicionar botões de "Salvar" e "Executar Projeção".
    -   Integrar `useProjection` hook para chamar a API.

**Entregável:** Formulário de configuração completo e funcional, enviando dados para o backend.

---

## Fase 5: Página de Resultados (Visualização de Dados) 📊

### Objetivo: Exibir os resultados da projeção de forma interativa e visual.

**Estimativa:** 3-4 semanas

**Tarefas:**

1.  **Implementar `projectionStore` (`src/features/projection/stores/projectionStore.ts`)**
    -   Armazenar `ProjectionData`, `KPIs`, `Insights`.
    -   Gerenciar filtros globais (período, granularidade).
2.  **Desenvolver Componentes de Métricas (`src/components/metrics/`)**
    -   `MetricCard.tsx`, `KPIGrid.tsx`.
3.  **Desenvolver Componentes de Gráficos (`src/components/charts/`)**
    -   `ChartContainer.tsx`: Wrapper base para gráficos.
    -   `LineChart.tsx`, `BarChart.tsx`, `ComboChart.tsx` (Recharts).
    -   `WaterfallChart.tsx`, `SankeyChart.tsx`, `CohortHeatmap.tsx` (Plotly.js).
4.  **Construir Dashboards Temáticos (`src/pages/ResultsPage/dashboards/`)**
    -   `OverviewDashboard.tsx`: KPIs principais, alertas, insights.
    -   `RevenueDashboard.tsx`: Gráficos de receita, funil, cohorts.
    -   `CostsDashboard.tsx`: Breakdown de custos, Sankey.
    -   `CashDashboard.tsx`: Fluxo de caixa, runway.
    -   `TeamDashboard.tsx`, `MarketingDashboard.tsx`, etc.
5.  **Página de Resultados (`src/pages/ResultsPage/ResultsPage.tsx`)**
    -   Integrar filtros globais.
    -   Exibir os dashboards em abas ou seções.

**Entregável:** Dashboards de resultados interativos e completos.

---

## Fase 6: Análises Avançadas e Cenários 🔬

### Objetivo: Implementar Monte Carlo, Sensibilidade e gerenciamento de cenários.

**Estimativa:** 2-3 semanas

**Tarefas:**

1.  **Implementar `scenarioStore` (`src/features/scenarios/stores/scenarioStore.ts`)**
    -   Gerenciar múltiplos cenários salvos.
    -   Funcionalidades de salvar, carregar, comparar cenários.
2.  **Hooks para Análises Avançadas (`src/features/analytics/hooks/`)**
    -   `useMonteCarlo.ts`, `useSensitivity.ts`, `useCohorts.ts` (chamando endpoints específicos do backend, se existirem, ou processando dados no frontend).
3.  **Componentes de Visualização Específicos**
    -   `FanChart.tsx` (Monte Carlo), `TornadoChart.tsx` (Sensibilidade).
4.  **Dashboard de Cenários (`src/pages/ResultsPage/dashboards/ScenariosDashboard.tsx`)**
    -   Interface para criar/gerenciar cenários.
    -   Visualização de comparação entre cenários.

**Entregável:** Ferramentas de análise avançada e gerenciamento de cenários.

---

## Fase 7: Polimento, UX e Exportação ✨

### Objetivo: Refinamento da experiência do usuário e funcionalidades de exportação.

**Estimativa:** 1-2 semanas

**Tarefas:**

1.  **Melhorias de UI/UX:**
    -   Loading states, empty states, error messages claros.
    -   Responsividade e acessibilidade.
    -   Tema customizado (cores, fontes).
2.  **Funcionalidades de Exportação:**
    -   Botões de exportação para CSV, Excel, PDF (integrando com backend ou bibliotecas frontend).
3.  **Documentação Interativa:**
    -   Tooltips, help buttons, tutorial de onboarding.

**Entregável:** Aplicação pronta para produção com UX refinada e recursos de exportação.

---

# 📝 CHECKLIST DE FEATURES (Atualizado)

Este checklist será atualizado e detalhado à medida que avançamos nas fases. As features listadas aqui são as mesmas do documento original, mas a priorização e a forma de implementação serão guiadas pelo novo roadmap de frontend.

## ✅ Configuração Avançada (Backend)
- [x] Múltiplos aportes programados
- [ ] Empréstimos com juros
- [ ] Impostos progressivos (Simples → Lucro Real)
- [ ] Reserva de contingência (% receita)
- [ ] Canais de aquisição separados
- [ ] Mix de planos evolutivo
- [ ] Upsell/Downsell configurável
- [ ] Add-ons e extras
- [ ] Taxas de pagamento completas
- [ ] Comissões de afiliados
- [ ] Comissões de parceiros
- [ ] Cashback/incentivos
- [ ] Infraestrutura em tiers configurável
- [ ] Transição automática entre tiers
- [ ] Marketing em 4 fases
- [ ] Orçamento por canal de marketing
- [ ] Salário fundador em fases
- [ ] Pró-labore condicional
- [ ] Múltiplos sócios/investidores
- [ ] Participação nos lucros
- [ ] Equipe com gatilhos de contratação
- [ ] Reajustes salariais programados
- [ ] Benefícios configuráveis (VR, VT, Plano)
- [ ] Decisão de escritório (Remoto/Híbrido/Presencial)
- [ ] Ferramentas SaaS por categoria
- [ ] Custos por usuário (ex: Notion)
- [ ] Upgrade automático de ferramentas
- [ ] Contabilidade escalável
- [ ] Consultorias específicas
- [ ] Depreciação com vida útil configurável
- [ ] Cenários de risco (recessão, churn spike)

## ✅ Inteligência e Insights (Backend)
- [ ] Alertas críticos automáticos
- [ ] Detecção de oportunidades
- [ ] Recomendações automatizadas
- [ ] Previsões de tendências
- [ ] Comparação vs. metas
- [ ] Timeline de marcos importantes
- [ ] "E se...?" interativo

## ✅ Dashboards (Frontend)
- [ ] Dashboard Principal (home)
- [ ] Dashboard de Receita
- [ ] Dashboard de Custos
- [ ] Dashboard de Caixa & Viabilidade
- [ ] Dashboard de Equipe
- [ ] Dashboard de Marketing
- [ ] Dashboard de Unit Economics
- [ ] Dashboard de Sensibilidade
- [ ] Dashboard de Cohorts
- [ ] Dashboard de Cenários & Monte Carlo

## ✅ Visualizações (Frontend)
- [ ] Gráficos de linha
- [ ] Gráficos de área
- [ ] Gráficos de barra
- [ ] Barras empilhadas
- [ ] Pizza/Donut
- [ ] Waterfall
- [ ] Sankey
- [ ] Funil
- [ ] Scatter plot
- [ ] Heatmap
- [ ] Gauge (velocímetro)
- [ ] Bullet chart
- [ ] Cohort table
- [ ] Fan chart (Monte Carlo)
- [ ] Tornado chart (sensibilidade)
- [ ] Spider chart
- [ ] Dual-axis charts
- [ ] Combo charts (barras + linhas)
- [ ] Mini sparklines em cards

## ✅ Drill-Down e Interatividade (Frontend)
- [ ] Clicar em métrica → ver breakdown
- [ ] Clicar em gráfico → drill-down
- [ ] Popup de decomposição
- [ ] Navegação breadcrumb
- [ ] Drill em múltiplos níveis
- [ ] Hover tooltips em tudo
- [ ] Filtros globais (período, cenário)
- [ ] Filtros específicos por dashboard

## ✅ Tabelas (Frontend)
- [ ] Tabela dinâmica master
- [ ] Filtros pré-programados
- [ ] DRE detalhado clicável
- [ ] Fluxo de caixa detalhado
- [ ] Breakdown de custos por categoria
- [ ] Análise de pessoal
- [ ] Análise de marketing
- [ ] Colunas personalizáveis
- [ ] Agrupamentos configuráveis
- [ ] Destacar células condicional
- [ ] Totalização (soma, média, mediana)
- [ ] Sorting multi-coluna
- [ ] Export individual de tabelas
- [ ] Comparação lado a lado (2 cenários)
- [ ] Granularidade ajustável (mensal/trimestral/anual)

## ✅ Análises Avançadas (Backend/Frontend)
- [ ] Monte Carlo com 500+ simulações
- [ ] Distribuições configuráveis por variável
- [ ] Correlação entre variáveis
- [ ] Fan chart visual
- [ ] Percentis (P5, P50, P95)
- [ ] Probabilidade de resultados
- [ ] Análise de sensibilidade univariada
- [ ] Análise de sensibilidade bivariada
- [ ] Tornado chart
- [ ] Heatmap 2D
- [ ] Spider chart
- [ ] Análise de cohorts
- [ ] Retention table
- [ ] Churn por cohort
- [ ] LTV por cohort
- [ ] Comparação entre cohorts

## ✅ Cenários (Frontend)
- [ ] Salvar cenários com nome
- [ ] Carregar cenários salvos
- [ ] Comparar 3 cenários lado a lado
- [ ] Base vs. Pessimista vs. Otimista
- [ ] Cenários de risco (recessão, etc.)
- [ ] Export/Import de cenários (JSON)
- [ ] Templates de cenários
- [ ] Duplicar e modificar cenário

## ✅ Exportação (Backend/Frontend)
- [ ] CSV simples
- [ ] Excel com múltiplas abas
- [ ] Excel com formatação rica
- [ ] PDF - Relatório Executivo
- [ ] PDF - Relatório Técnico
- [ ] PowerPoint com slides prontos
- [ ] JSON (backup completo)
- [ ] Agendamento de relatórios (futuro)

## ✅ UX/UI (Frontend)
- [ ] Tema customizado
- [ ] Modo escuro/claro
- [ ] Sidebar com navegação clara
- [ ] Breadcrumbs
- [ ] Loading states elegantes
- [ ] Empty states informativos
- [ ] Error messages claros
- [ ] Success feedbacks
- [ ] Tooltips em todos os campos
- [ ] Help buttons contextuais
- [ ] Tutorial interativo (primeira vez)
- [ ] Atalhos de teclado
- [ ] Responsive (mobile-friendly)

## ✅ Performance (Frontend)
- [ ] Cache agressivo
- [ ] Lazy loading de dashboards
- [ ] Debounce em inputs
- [ ] Otimização de gráficos
- [ ] Paginação em tabelas grandes
- [ ] Background processing (Monte Carlo)

---

# 🔄 MATRIZ DE PRIORIDADES (Atualizada para Frontend)

Esta matriz será refinada à medida que avançamos, mas serve como um guia inicial para as prioridades do frontend.

## Prioridade CRÍTICA (Fazer AGORA) 🔴

| Feature | Impacto | Esforço | Razão |
|---------|---------|---------|-------|
| **Fase 3: Fundação do Frontend - Layout e API Client** | 🔥🔥🔥 | 1 semana | Base para todo o resto do frontend |
| **Fase 4: Página de Configuração (Formulário Dinâmico)** | 🔥🔥🔥 | 2-3 semanas | Entrada de dados é o core da aplicação |

**Total estimado: 3-4 semanas**

---

## Prioridade ALTA (Logo em seguida) 🟡

| Feature | Impacto | Esforço | Razão |
|---------|---------|---------|-------|
| **Fase 5: Página de Resultados (Visualização de Dados)** | 🔥🔥🔥 | 3-4 semanas | Exibir resultados é o objetivo final |

**Total estimado: 3-4 semanas**

---

## Prioridade MÉDIA (Quando tiver tempo) 🟢

| Feature | Impacto | Esforço | Razão |
|---------|---------|---------|-------|
| **Fase 6: Análises Avançadas e Cenários** | 🔥🔥 | 2-3 semanas | Agrega valor analítico profundo |
| **Fase 7: Polimento, UX e Exportação** | 🔥🔥 | 1-2 semanas | Refinamento e funcionalidades essenciais |

**Total estimado: 3-5 semanas**

---

## Prioridade BAIXA (Futuro) ⚪

| Feature | Impacto | Esforço | Razão |
|---------|---------|---------|---|
| **Integrações externas (Stripe, GA, CRM)** | 🔥 | 5+ dias | Futuro: dados reais |
| **API REST** | 🔥 | 3+ dias | Futuro: integração com outros sistemas |
| **Multi-usuário** | 🔥 | 5+ dias | Futuro: colaboração |
| **Agendamento de relatórios** | 🔥 | 2 dias | Automação |

---

# 🎯 ROADMAP VISUAL (Atualizado)

```
MÊS 1: FUNDAÇÃO DO FRONTEND & CONFIGURAÇÃO
├─ Semana 1: Layout Básico + API Client
│  └─ Entregável: App com layout e comunicação API funcional
│
└─ Semanas 2-3: Página de Configuração
   └─ Entregável: Formulário de configuração completo e funcional

MÊS 2: VISUALIZAÇÃO DE DADOS & ANÁLISES AVANÇADAS
├─ Semanas 4-5: Página de Resultados (Dashboards)
│  └─ Entregável: Dashboards de resultados interativos
│
└─ Semanas 6-7: Análises Avançadas e Cenários
   └─ Entregável: Ferramentas de análise avançada e gerenciamento de cenários

MÊS 3: POLIMENTO & EXPORTAÇÃO
├─ Semanas 8-9: Polimento, UX e Exportação
│  └─ Entregável: Aplicação pronta para produção com UX refinada e recursos de exportação
```