# 🎯 ROADMAP ESTRATÉGICO E UNIFICADO DO FRONTEND

**ESTRATÉGIA CENTRAL:** Construir a **PÁGINA DE RESULTADOS (DASHBOARDS)** como prioridade máxima, utilizando uma abordagem de **desenvolvimento com Mock Data**.

**JUSTIFICATIVA:** Entregar o maior valor percebido pelo usuário no menor tempo possível, permitindo validação de UX, demonstrações a stakeholders e desenvolvimento paralelo ao backend.

---

## 🚀 FASE 1: FUNDAÇÃO (CONCLUÍDA) ✅
**Objetivo:** Ambiente de desenvolvimento pronto, layout base funcional e dados mock disponíveis para toda a aplicação.

### **Tarefas Principais:**
- **Setup do Projeto:**
  - [x] Criar projeto com Vite + React + TypeScript.
  - [x] Instalar e configurar Tailwind CSS com o tema do projeto (`tailwind.config.js`).
  - [x] Instalar todas as dependências principais (`package.json`): Zustand, TanStack Query, Recharts, Plotly, React Hook Form, Zod, Axios, etc.
  - [x] Configurar ESLint, Prettier e caminhos de importação (`@/`).
- **Mock Data & Tipos:**
  - [x] Criar `src/lib/api/mockData.ts` com uma simulação realista da resposta da API `/projecao`.
  - [x] Criar `src/types/api.types.ts` com todas as interfaces TypeScript que espelham a API.
  - [x] Implementar o hook `useMockProjection()` para carregar os dados mock com um delay simulado.
- **Layout Base:**
  - [x] Componente `AppLayout.tsx` contendo `Sidebar`, `Header` e a área de conteúdo principal.
  - [x] Componente `Sidebar.tsx` com a navegação principal entre os futuros dashboards.
  - [x] Componente `Header.tsx` para título da página, breadcrumbs e ações globais.
  - [x] Configurar o roteamento principal (`react-router-dom`) para as páginas de Resultados e Configuração.

**Entregável:** Aplicação funcional com layout, navegação e dados de exemplo, pronta para a construção dos dashboards.

---

## 🚀 FASE 2: DASHBOARD DE OVERVIEW (CONCLUÍDA) ✅
**Objetivo:** Implementar o dashboard principal, a primeira tela que o usuário vê, oferecendo uma visão geral e imediata da saúde do negócio.

### **Checklist de Features:**
- **Alertas e Insights:**
  - [x] Componente `AlertCard` para exibir alertas críticos, de aviso e informativos.
  - [x] Seção no topo do dashboard para listar os alertas mais importantes retornados pelo backend.
  - [x] Componente `InsightCard` para mostrar oportunidades e recomendações.
- **Grid de KPIs:**
  - [x] Componente `MetricCard` para exibir uma métrica individual com seu valor, delta de crescimento/queda e formatação.
  - [x] Grid com 6 a 8 dos KPIs mais importantes (MRR, Usuários, Saldo de Caixa, LTV/CAC, Churn, Runway, etc.).
- **Visualizações Gráficas:**
  - [x] **Gráfico de Linha:** Evolução do MRR ao longo do tempo.
  - [x] **Gráfico de Linha/Área:** Evolução do Saldo de Caixa, com zonas de cor para indicar segurança, atenção e perigo (Vale da Morte).
  - [x] **Gráfico Combo (Barras + Linhas):** Comparativo de Receita vs. Custos Totais vs. Lucro.
- **Timeline:**
  - [x] Componente `Timeline` para exibir os marcos importantes do projeto (ex: Break-even, contratações, etc.).

**Entregável:** Dashboard de "Visão Geral" 100% funcional e visualmente polido, consumindo os dados do `mockData`.

### **Ciclo de Refinamento Estratégico (CONCLUÍDO) ✅**
- **Novo Sistema de Alertas:** O painel de alertas foi substituído por um componente `AlertHub` no cabeçalho, otimizando espaço e hierarquia.
- **Refatoração dos KPI Cards:** Os cards foram simplificados para melhor escaneabilidade, removendo os sparklines e se tornando gatilhos para um painel de drill-down.
- **Implementação de Drill-Down:** Adicionado um painel `Sheet` que abre ao clicar nos cards, mostrando um gráfico detalhado da métrica (Progressive Disclosure).
- **Layout e Animações:** O layout da página foi aprimorado e microinterações foram adicionadas para uma experiência mais premium.
- Inclui todas as correções de bugs e polimentos visuais e de interação.

---

## 🚀 FASE 3: DASHBOARD DE RECEITA (EM ANDAMENTO) 🚧
**Objetivo:** Oferecer uma visão detalhada sobre a principal alavanca do negócio: a receita.

### **Checklist de Features:**
- **Visualizações Gráficas:**
  - [ ] **Gráfico de Waterfall:** Decomposição do MRR (Início → Novos Clientes → Expansão → Contração → Churn → Final).
  - [ ] **Gráfico de Funil:** Funil de conversão de usuários (Visitantes → Trials → Pagantes).
  - [ ] **Gráfico de Área Empilhado:** Composição do MRR por diferentes planos ou produtos.
- **Análise de Cohort:**
  - [ ] **Heatmap de Retenção:** Tabela visual mostrando a retenção de clientes por cohort ao longo dos meses.
- **Tabela Detalhada:**
  - [ ] Tabela com a análise completa de métricas de receita, mês a mês.

**Entregável:** Dashboard de "Receita" completo, com visualizações avançadas e interativas.

---

## 🚀 FASE 4: DASHBOARD DE CUSTOS (Estimativa: 2-3 dias) 💸
**Objetivo:** Permitir rastreabilidade completa dos custos e despesas.

### **Checklist de Features:**
- **Visualizações Gráficas:**
  - [ ] **Diagrama de Sankey:** Fluxo de dinheiro desde a Receita Bruta até o Lucro Líquido, passando por COGS e OPEX.
  - [ ] **Gráfico de Pizza com Drill-Down:** Visualização da composição do OPEX (Nível 1: Pessoal, Infra, Mkt...). Ao clicar em uma fatia (ex: "Pessoal"), um modal ou nova visão mostra o detalhamento (Nível 2: Salários, Benefícios...).
  - [ ] **Gráfico de Barras Empilhadas:** Comparativo de Custos Fixos vs. Custos Variáveis.
- **Tabela Detalhada:**
  - [ ] Tabela completa com o breakdown de todas as categorias de custos, permitindo filtros e ordenação.

**Entregável:** Dashboard de "Custos" com drill-down, a funcionalidade mais importante desta seção.

---

## 🚀 FASE 5: FUNCIONALIDADES GLOBAIS E POLIMENTO (Estimativa: 2-3 dias) 🎨
**Objetivo:** Unificar a experiência do usuário e garantir a qualidade da aplicação.

### **Checklist de Features:**
- **Filtros Globais:**
  - [ ] Componentes de filtro para Período (mês de início/fim) e Granularidade (mensal, trimestral, anual).
  - [ ] Store (Zustand) para gerenciar o estado dos filtros.
  - [ ] Lógica para que todos os dashboards reajam e se atualizem de acordo com os filtros aplicados.
- **Qualidade da Experiência (UX):**
  - [ ] **Loading States:** Implementar skeletons para gráficos, tabelas e métricas.
  - [ ] **Empty States:** Criar componentes para quando não há dados a serem exibidos.
  - [ ] **Error States:** Tratar e exibir erros de forma amigável.
  - [ ] **Responsividade:** Garantir que a aplicação seja utilizável em telas menores (tablet e mobile).
  - [ ] **Animações:** Adicionar transições suaves para uma experiência mais fluida.

**Entregável:** Aplicação coesa, interativa, robusta e com experiência de usuário refinada.

---

## 🚀 FASE 6: PÁGINA DE CONFIGURAÇÃO (Estimativa: 5-7 dias) ⚙️
**Objetivo:** Criar a interface para que o usuário possa inserir os dados e gerar suas próprias projeções.

### **Checklist de Features:**
- **Formulário Complexo:**
  - [ ] Utilizar `React Hook Form` para gerenciamento de estado e performance.
  - [ ] Utilizar `Zod` para validação de dados.
  - [ ] Dividir o formulário em seções lógicas (Capital, Receita, Custos, Equipe, etc.).
  - [ ] Criar componentes de input reutilizáveis e especializados (moeda, percentual, etc.).
- **Integração com API:**
  - [ ] Implementar o hook `useProjection` que chama a API real do backend.
  - [ ] Tratar o estado de loading e erro da chamada.
  - [ ] Ao receber a resposta, salvar os dados no `projectionStore` e redirecionar o usuário para a Página de Resultados.

**Entregável:** Formulário completo que permite ao usuário alimentar o modelo e gerar uma projeção.

---

## 🚀 FASE 7: DASHBOARDS AVANÇADOS E EXPORTAÇÃO (Pós-MVP) ✨
**Objetivo:** Adicionar funcionalidades de análise profunda e utilitários.

### **Checklist de Features:**
- [ ] **Dashboard de Caixa & Viabilidade:** Gráficos de fluxo de caixa, análise de runway.
- [ ] **Dashboard de Unit Economics:** Análise detalhada de LTV, CAC e Payback.
- [ ] **Dashboard de Análise de Sensibilidade:** Gráficos de Tornado e Spider.
- [ ] **Dashboard de Cenários:** Interface para criar, salvar, carregar e comparar cenários (Base, Otimista, Pessimista).
- [ ] **Funcionalidades de Exportação:** Botões para exportar dados e relatórios para CSV, Excel e PDF.