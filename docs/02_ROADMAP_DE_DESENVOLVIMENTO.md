# Roadmap de Desenvolvimento

Este documento consolida o plano de desenvolvimento do projeto SAM, combinando os planos estratégicos de backend e frontend. Ele reflete o estado atual do projeto e define as próximas fases de implementação.

## Estratégia Geral

A estratégia de desenvolvimento foi dividida em duas frentes principais que convergem:

1.  **Desenvolvimento do Backend (Core):** Focado em construir um motor de projeção robusto, modular e desacoplado de qualquer interface, expondo sua funcionalidade através de uma API FastAPI.
2.  **Desenvolvimento do Frontend (React App):** Focado em entregar o maior valor percebido pelo usuário no menor tempo possível, utilizando uma abordagem de **desenvolvimento com Mock Data** para construir a interface dos dashboards em paralelo com o backend.

---

## 🗺️ Roadmap por Fases

### ✅ Fase 1: Fundação e Estrutura do Projeto
**Status:** Concluída

**Objetivo:** Estabelecer as bases técnicas para ambas as frentes do projeto.

**Entregáveis:**
- **Backend:**
    - Estrutura de pastas do `core` definida.
    - Dependências principais (FastAPI, Pandas, Pydantic) instaladas.
    - Objeto de configuração inicial (`ConfigFinanceira`) criado.
- **Frontend:**
    - Projeto criado com Vite + React + TypeScript.
    - Stack de tecnologias (Tailwind, Zustand, TanStack Query, Recharts, etc.) instalado e configurado.
    - Estrutura de pastas `frontend/src` definida.
    - Sistema de Mock Data (`useMockProjection`) e tipos da API (`api.types.ts`) implementados.
    - Layout principal da aplicação (`AppLayout` com `Sidebar` e `Header`) funcional.

---

### ✅ Fase 2: Implementação dos Dashboards (Frontend)
**Status:** Concluída

**Objetivo:** Construir as principais telas de visualização de dados usando os dados mockados.

**Entregáveis:**
- **Dashboard de Visão Geral:**
    - Implementação de todos os componentes visuais: `MetricCard`, `FinancialProjectionChart`, `TornadoChart`, etc.
    - Múltiplos ciclos de refinamento de UX/UI, resultando em um layout focado em simulação com um "Simulador Rápido" em modal.
- **Dashboard de Receita:**
    - Implementação dos gráficos de `WaterfallChart`, `FunnelChart`, `StackedAreaChart` e `CohortHeatmap`.
- **Dashboard de Custos:**
    - Implementação dos gráficos de `SankeyChart` e `PieChartWithDrilldown`.
- **Sistema de Filtros Globais:**
    - Implementação de um store global (`useFiltersStore`) para gerenciar filtros de data e granularidade.
    - Todos os dashboards foram refatorados para reagir a essas mudanças de filtro.

---

### 🚧 Fase 3: Refatoração do Backend e Criação da API
**Status:** Em Andamento

**Objetivo:** Desacoplar a lógica de negócio do antigo frontend (Streamlit), centralizá-la no `core` e expô-la através de uma API robusta.

**Tarefas Principais:**
- **Desacoplamento do Core:**
  - [ ] Remover todas as importações e dependências do Streamlit dos arquivos dentro da pasta `core/`.
- **Centralização da Lógica:**
  - [ ] Mover a lógica de análise (ex: `gerar_cohort_matrix`) das páginas do Streamlit para a pasta `core/analytics`.
  - [ ] Mover a lógica de criação de gráficos (ex: `criar_grafico_waterfall`) para o arquivo `core/visualizations.py`.
- **Construção da API:**
  - [ ] Instalar dependências da API (FastAPI, Uvicorn).
  - [ ] Criar o arquivo `main.py` com a aplicação FastAPI.
  - [ ] Definir o modelo Pydantic `ProjecaoRequest` para validar os dados de entrada.
  - [ ] Implementar o endpoint `/projecao` que recebe a configuração, executa o motor financeiro e retorna os resultados completos em JSON.

---

### ⏳ Fase 4: Conexão Backend-Frontend e Lógica do Simulador
**Status:** Próxima Fase

**Objetivo:** Substituir os dados mockados do frontend pelos dados reais da API e implementar a lógica de simulação.

**Tarefas Principais:**
- **Frontend:**
  - [ ] Implementar o hook `useProjection` que utiliza TanStack Query para chamar o endpoint `/projecao` da API real.
  - [ ] Substituir o uso do `useMockProjection` pelo novo `useProjection`.
  - [ ] Implementar a lógica no `QuickSimulatorModal` para que as alterações nos sliders disparem novas chamadas à API, atualizando os dashboards em tempo real.
- **Backend/API:**
  - [ ] Garantir que a API esteja performática e que os resultados sejam consistentes com o que o frontend espera.

---

### ⏳ Fase 5: Funcionalidades Avançadas e Polimento
**Status:** Futuro

**Objetivo:** Implementar os dashboards restantes e as funcionalidades de qualidade de vida.

**Tarefas Principais:**
- **Dashboards Avançados:**
  - [ ] Dashboard de Caixa & Viabilidade.
  - [ ] Dashboard de Unit Economics.
  - [ ] Dashboard de Análise de Sensibilidade.
  - [ ] Dashboard de Cenários (Comparação).
- **Página de Configuração:**
  - [ ] Construir a interface de formulário completa para que o usuário possa inserir todas as premissas do modelo.
- **Qualidade da Experiência (UX):**
  - [ ] Implementar a funcionalidade de granularidade (Trimestral, Anual) nos filtros.
  - [ ] Adicionar animações e transições (`Framer Motion`).
  - [ ] Implementar sistema de notificações (`Toasts`).
  - [ ] Garantir responsividade completa.
- **Funcionalidades de Exportação:**
  - [ ] Criar utilitários para exportar dados e relatórios para CSV, PDF ou Excel.
