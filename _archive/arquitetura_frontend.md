<thinking>
Perfeito! Agora vou criar uma proposta de arquitetura de frontend extremamente detalhada e profissional. Vou focar em:

Arquitetura de Componentes React
Estratégia de Gerenciamento de Estado
Estratégia de Comunicação com API
Biblioteca de Gráficos

Vou criar um documento completo, visual e prático, que pode ser usado como blueprint para implementação.
</thinking>
🎨 PROPOSTA DE ARQUITETURA DE FRONTEND
SAM Financial Model v4.0 - React + TypeScript + Vite + Tailwind CSS

📋 ÍNDICE

Visão Geral da Arquitetura
Estrutura de Pastas Completa
Arquitetura de Componentes
Gerenciamento de Estado
Comunicação com API
Biblioteca de Gráficos
Sistema de Design
Fluxo de Dados
Padrões de Código
Performance e Otimizações


1. VISÃO GERAL DA ARQUITETURA {#1-visão-geral}
1.1 Stack Tecnológico Recomendado
┌─────────────────────────────────────────────────────────────┐
│                    STACK TECNOLÓGICO                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ ⚛️  React 18.3+         │ Framework UI                      │
│ 📘 TypeScript 5.3+      │ Type Safety                       │
│ ⚡ Vite 5.0+            │ Build Tool                        │
│ 🎨 Tailwind CSS 3.4+    │ Styling                          │
│                                                              │
│ 🗂️  Zustand 4.5+        │ Estado Global (RECOMENDADO)      │
│ 📝 React Hook Form 7.5+ │ Formulários (RECOMENDADO)        │
│ 🔄 TanStack Query 5.0+  │ Data Fetching (RECOMENDADO)      │
│ 📊 Recharts 2.10+       │ Gráficos Base (RECOMENDADO)      │
│ 📈 Plotly.js 2.27+      │ Gráficos Avançados (COMPLEMENTAR)│
│                                                              │
│ 🎭 Framer Motion 11+    │ Animações                        │
│ 🧩 Radix UI / Shadcn    │ Componentes Base                 │
│ 📅 date-fns 3.0+        │ Manipulação de Datas             │
│ 🎯 Zod 3.22+            │ Validação                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
1.2 Princípios Arquiteturais
✅ 1. Component-Driven Development

Componentes atômicos e reutilizáveis
Separation of Concerns (apresentação vs. lógica)
Composição sobre herança

✅ 2. Performance-First

Code splitting por rota
Lazy loading de dashboards
Memoização estratégica
Virtual scrolling em tabelas grandes

✅ 3. Type Safety

Tipos compartilhados com backend (gerados via OpenAPI)
Validação em tempo de compilação
IntelliSense completo

✅ 4. Accessibility & UX

ARIA labels em todos os componentes
Keyboard navigation
Loading states progressivos
Error boundaries


2. ESTRUTURA DE PASTAS COMPLETA {#2-estrutura-de-pastas}
sam-frontend/
│
├── public/
│   ├── favicon.ico
│   └── logo.svg
│
├── src/
│   │
│   ├── app/                          # Configuração da aplicação
│   │   ├── App.tsx                   # Componente raiz
│   │   ├── router.tsx                # Configuração de rotas
│   │   └── providers.tsx             # Providers globais (Query, Theme)
│   │
│   ├── pages/                        # Páginas (rotas principais)
│   │   ├── ConfigurationPage/
│   │   │   ├── index.tsx
│   │   │   ├── ConfigurationPage.tsx
│   │   │   └── sections/
│   │   │       ├── CapitalSection.tsx
│   │   │       ├── RevenueSection.tsx
│   │   │       ├── TeamSection.tsx
│   │   │       ├── InfraSection.tsx
│   │   │       ├── MarketingSection.tsx
│   │   │       └── index.ts
│   │   │
│   │   └── ResultsPage/
│   │       ├── index.tsx
│   │       ├── ResultsPage.tsx
│   │       └── dashboards/
│   │           ├── OverviewDashboard.tsx
│   │           ├── RevenueDashboard.tsx
│   │           ├── CostsDashboard.tsx
│   │           ├── CashDashboard.tsx
│   │           ├── TeamDashboard.tsx
│   │           ├── MarketingDashboard.tsx
│   │           ├── UnitEconomicsDashboard.tsx
│   │           ├── SensitivityDashboard.tsx
│   │           ├── CohortsDashboard.tsx
│   │           └── ScenariosDashboard.tsx
│   │
│   ├── components/                   # Componentes reutilizáveis
│   │   │
│   │   ├── ui/                       # Componentes base (Shadcn-style)
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Select.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Tabs.tsx
│   │   │   ├── Tooltip.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── Alert.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── layout/                   # Componentes de layout
│   │   │   ├── AppLayout.tsx         # Layout principal
│   │   │   ├── Sidebar.tsx           # Navegação lateral
│   │   │   ├── Header.tsx            # Header superior
│   │   │   ├── Breadcrumbs.tsx       # Navegação breadcrumb
│   │   │   └── Footer.tsx
│   │   │
│   │   ├── forms/                    # Componentes de formulário
│   │   │   ├── FormField.tsx         # Campo genérico
│   │   │   ├── FormSection.tsx       # Seção de formulário
│   │   │   ├── NumberInput.tsx       # Input numérico
│   │   │   ├── PercentageInput.tsx   # Input de porcentagem
│   │   │   ├── CurrencyInput.tsx     # Input de moeda
│   │   │   ├── DateInput.tsx         # Input de data
│   │   │   ├── TriggerBuilder.tsx    # Builder de gatilhos
│   │   │   └── index.ts
│   │   │
│   │   ├── metrics/                  # Componentes de métricas
│   │   │   ├── MetricCard.tsx        # Card de métrica principal
│   │   │   ├── MetricCardWithSparkline.tsx
│   │   │   ├── MetricCardWithProgress.tsx
│   │   │   ├── MetricComparison.tsx  # Comparação de métricas
│   │   │   ├── MetricTrend.tsx       # Indicador de tendência
│   │   │   ├── KPIGrid.tsx           # Grid de KPIs
│   │   │   └── index.ts
│   │   │
│   │   ├── charts/                   # Componentes de gráficos
│   │   │   ├── ChartContainer.tsx    # Container base
│   │   │   ├── LineChart.tsx
│   │   │   ├── AreaChart.tsx
│   │   │   ├── BarChart.tsx
│   │   │   ├── ComboChart.tsx        # Barras + Linhas
│   │   │   ├── WaterfallChart.tsx
│   │   │   ├── SankeyChart.tsx
│   │   │   ├── FunnelChart.tsx
│   │   │   ├── GaugeChart.tsx
│   │   │   ├── CohortHeatmap.tsx
│   │   │   ├── TornadoChart.tsx
│   │   │   ├── FanChart.tsx          # Monte Carlo
│   │   │   └── index.ts
│   │   │
│   │   ├── tables/                   # Componentes de tabelas
│   │   │   ├── DataTable.tsx         # Tabela base (TanStack Table)
│   │   │   ├── TableFilters.tsx
│   │   │   ├── TablePagination.tsx
│   │   │   ├── TableExport.tsx
│   │   │   ├── CohortTable.tsx       # Tabela de cohorts específica
│   │   │   └── index.ts
│   │   │
│   │   ├── drill-down/               # Sistema de drill-down
│   │   │   ├── DrillDownModal.tsx    # Modal de drill-down
│   │   │   ├── DrillDownButton.tsx   # Botão de drill
│   │   │   ├── DrillDownBreadcrumb.tsx
│   │   │   ├── BreakdownPieChart.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── insights/                 # Componentes de insights
│   │   │   ├── AlertCard.tsx         # Card de alerta
│   │   │   ├── InsightCard.tsx       # Card de insight
│   │   │   ├── AlertsSection.tsx     # Seção de alertas
│   │   │   ├── InsightsTimeline.tsx  # Timeline de eventos
│   │   │   └── index.ts
│   │   │
│   │   ├── filters/                  # Componentes de filtro
│   │   │   ├── GlobalFilters.tsx     # Filtros globais
│   │   │   ├── PeriodFilter.tsx
│   │   │   ├── ScenarioFilter.tsx
│   │   │   ├── GranularityFilter.tsx
│   │   │   └── index.ts
│   │   │
│   │   └── loading/                  # Estados de loading
│   │       ├── LoadingSpinner.tsx
│   │       ├── ChartSkeleton.tsx
│   │       ├── TableSkeleton.tsx
│   │       ├── MetricSkeleton.tsx
│   │       └── index.ts
│   │
│   ├── features/                     # Features modulares
│   │   │
│   │   ├── configuration/            # Feature de configuração
│   │   │   ├── hooks/
│   │   │   │   ├── useConfigForm.ts
│   │   │   │   ├── useConfigValidation.ts
│   │   │   │   └── useConfigSubmit.ts
│   │   │   ├── stores/
│   │   │   │   └── configStore.ts    # Zustand store
│   │   │   ├── types/
│   │   │   │   └── config.types.ts
│   │   │   └── utils/
│   │   │       ├── configValidators.ts
│   │   │       └── configDefaults.ts
│   │   │
│   │   ├── projection/               # Feature de projeção
│   │   │   ├── hooks/
│   │   │   │   ├── useProjection.ts
│   │   │   │   ├── useKPIs.ts
│   │   │   │   └── useInsights.ts
│   │   │   ├── stores/
│   │   │   │   └── projectionStore.ts
│   │   │   ├── types/
│   │   │   │   ├── projection.types.ts
│   │   │   │   └── kpi.types.ts
│   │   │   └── utils/
│   │   │       ├── kpiCalculators.ts
│   │   │       └── dataTransformers.ts
│   │   │
│   │   ├── scenarios/                # Feature de cenários
│   │   │   ├── hooks/
│   │   │   │   ├── useScenarios.ts
│   │   │   │   └── useScenarioComparison.ts
│   │   │   ├── stores/
│   │   │   │   └── scenarioStore.ts
│   │   │   └── types/
│   │   │       └── scenario.types.ts
│   │   │
│   │   └── analytics/                # Feature de analytics
│   │       ├── hooks/
│   │       │   ├── useMonteCarlo.ts
│   │       │   ├── useSensitivity.ts
│   │       │   └── useCohorts.ts
│   │       └── types/
│   │           └── analytics.types.ts
│   │
│   ├── hooks/                        # Hooks globais
│   │   ├── useDebounce.ts
│   │   ├── useLocalStorage.ts
│   │   ├── useMediaQuery.ts
│   │   ├── useClickOutside.ts
│   │   └── index.ts
│   │
│   ├── lib/                          # Bibliotecas e utilitários
│   │   ├── api/
│   │   │   ├── client.ts             # Axios/Fetch client
│   │   │   ├── endpoints.ts          # Definição de endpoints
│   │   │   └── types.ts              # Tipos da API
│   │   │
│   │   ├── utils/
│   │   │   ├── formatters.ts         # Formatação de valores
│   │   │   ├── validators.ts         # Validadores
│   │   │   ├── calculations.ts       # Cálculos auxiliares
│   │   │   └── constants.ts          # Constantes
│   │   │
│   │   └── theme/
│   │       ├── colors.ts             # Paleta de cores
│   │       ├── tokens.ts             # Design tokens
│   │       └── tailwind.config.ts    # Config do Tailwind
│   │
│   ├── types/                        # Tipos globais
│   │   ├── index.ts
│   │   ├── api.types.ts
│   │   ├── config.types.ts
│   │   └── shared.types.ts
│   │
│   ├── styles/                       # Estilos globais
│   │   ├── globals.css
│   │   └── animations.css
│   │
│   ├── main.tsx                      # Entry point
│   └── vite-env.d.ts
│
├── .env.example                      # Exemplo de variáveis de ambiente
├── .eslintrc.cjs                     # ESLint config
├── .prettierrc                       # Prettier config
├── tsconfig.json                     # TypeScript config
├── vite.config.ts                    # Vite config
├── tailwind.config.js                # Tailwind config
├── package.json
└── README.md

3. ARQUITETURA DE COMPONENTES {#3-arquitetura-de-componentes}
3.1 Hierarquia de Componentes Visual
┌─────────────────────────────────────────────────────────────┐
│                         App.tsx                              │
│                    (Root Component)                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ├─ Providers (Query, Theme, Store)
                       │
                       └─ AppLayout
                           │
                           ├─ Sidebar (navegação)
                           ├─ Header (breadcrumbs, user)
                           │
                           └─ Main Content (Router)
                               │
                               ├─ ConfigurationPage
                               │   │
                               │   ├─ FormSection (Capital)
                               │   │   └─ FormFields (inputs)
                               │   │
                               │   ├─ FormSection (Revenue)
                               │   │   └─ PlanMixBuilder
                               │   │
                               │   ├─ FormSection (Team)
                               │   │   └─ TriggerBuilder
                               │   │
                               │   └─ FormActions (Submit/Reset)
                               │
                               └─ ResultsPage
                                   │
                                   ├─ GlobalFilters (sidebar)
                                   │
                                   ├─ Tabs (dashboards)
                                   │   │
                                   │   ├─ OverviewDashboard
                                   │   │   ├─ AlertsSection
                                   │   │   ├─ KPIGrid
                                   │   │   │   └─ MetricCard (com drill-down)
                                   │   │   ├─ InsightsTimeline
                                   │   │   └─ MilestonesChart
                                   │   │
                                   │   ├─ RevenueDashboard
                                   │   │   ├─ WaterfallChart
                                   │   │   ├─ ComboChart (MRR por plano)
                                   │   │   ├─ FunnelChart
                                   │   │   └─ CohortTable
                                   │   │
                                   │   ├─ CostsDashboard
                                   │   │   ├─ SankeyChart (fluxo)
                                   │   │   ├─ BreakdownPieChart (com drill)
                                   │   │   └─ DataTable (detalhado)
                                   │   │
                                   │   └─ ... (outros dashboards)
                                   │
                                   └─ DrillDownModal (global)
3.2 Componentes Atômicos (Atomic Design)
Nível 1: Atoms (Componentes Base)
typescript// src/components/ui/Button.tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  loading?: boolean;
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

// src/components/ui/Input.tsx
interface InputProps {
  type?: 'text' | 'number' | 'email';
  label?: string;
  placeholder?: string;
  error?: string;
  helperText?: string;
  leftAddon?: string;
  rightAddon?: string;
  value: string | number;
  onChange: (value: string | number) => void;
}
Nível 2: Molecules (Composições Simples)
typescript// src/components/metrics/MetricCard.tsx
interface MetricCardProps {
  label: string;
  value: number | string;
  formatValue?: (v: number | string) => string;
  delta?: number;
  deltaLabel?: string;
  trend?: 'up' | 'down' | 'neutral';
  icon?: React.ReactNode;
  loading?: boolean;
  
  // Drill-down
  breakdown?: Record<string, number>;
  onDrillDown?: () => void;
  
  // Target
  target?: number;
  targetLabel?: string;
  
  // Sparkline
  sparklineData?: number[];
}
Nível 3: Organisms (Composições Complexas)
typescript// src/components/metrics/KPIGrid.tsx
interface KPIGridProps {
  kpis: KPI[];
  layout?: 'grid' | 'list';
  columns?: 2 | 3 | 4;
  loading?: boolean;
  onKPIClick?: (kpi: KPI) => void;
}

// src/components/charts/ChartContainer.tsx
interface ChartContainerProps {
  title: string;
  subtitle?: string;
  actions?: React.ReactNode; // Export, fullscreen, etc.
  loading?: boolean;
  error?: string;
  isEmpty?: boolean;
  emptyMessage?: string;
  height?: number | string;
  children: React.ReactNode;
}
Nível 4: Templates (Layouts de Página)
typescript// src/pages/ResultsPage/dashboards/BaseDashboard.tsx
interface BaseDashboardProps {
  title: string;
  description?: string;
  filters?: React.ReactNode;
  children: React.ReactNode;
}

4. GERENCIAMENTO DE ESTADO {#4-gerenciamento-de-estado}
4.1 Recomendação: Zustand 🏆
Por que Zustand?
✅ Simplicidade: API minimalista, curva de aprendizado baixa
✅ Performance: Re-renders otimizados por padrão
✅ TypeScript: Suporte nativo e excelente
✅ Sem boilerplate: Menos código que Redux
✅ DevTools: Integração com Redux DevTools
✅ Middleware: Persist, immer, devtools out-of-the-box
✅ Tamanho: ~1KB gzipped (vs. Redux 8KB)
Comparação com Alternativas:
BibliotecaPrósContrasRecomendaçãoZustand✅ Simples<br>✅ Performance<br>✅ TypeScript❌ Menos maduroRECOMENDADORedux Toolkit✅ Maduro<br>✅ Ecossistema❌ Boilerplate<br>❌ ComplexoAlternativaJotai✅ Atômico<br>✅ Leve❌ Diferente mental modelNão recomendadoRecoil✅ Atômico❌ Facebook<br>❌ ExperimentalNão recomendado
4.2 Arquitetura de Stores Zustand
Store Principal: ConfigStore
typescript// src/features/configuration/stores/configStore.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface ConfigState {
  // Estado
  config: ConfigFinanceira | null;
  isDirty: boolean;
  validationErrors: Record<string, string>;
  
  // Ações
  setConfig: (config: Partial<ConfigFinanceira>) => void;
  updateField: (path: string, value: any) => void;
  resetConfig: () => void;
  loadConfig: (config: ConfigFinanceira) => void;
  
  // Builders
  addAporte: (aporte: Aporte) => void;
  addFuncionario: (funcionario: Funcionario) => void;
  addFerramenta: (ferramenta: Ferramenta) => void;
  
  // Validação
  validate: () => boolean;
  clearErrors: () => void;
}

export const useConfigStore = create<ConfigState>()(
  devtools(
    persist(
      immer((set, get) => ({
        // Estado inicial
        config: null,
        isDirty: false,
        validationErrors: {},
        
        // Implementação das ações
        setConfig: (newConfig) => set((state) => {
          state.config = { ...state.config, ...newConfig };
          state.isDirty = true;
        }),
        
        updateField: (path, value) => set((state) => {
          // Atualiza campo aninhado (ex: "capital.inicial")
          const keys = path.split('.');
          let current: any = state.config;
          for (let i = 0; i < keys.length - 1; i++) {
            current = current[keys[i]];
          }
          current[keys[keys.length - 1]] = value;
          state.isDirty = true;
        }),
        
        resetConfig: () => set((state) => {
          state.config = getDefaultConfig();
          state.isDirty = false;
          state.validationErrors = {};
        }),
        
        loadConfig: (config) => set((state) => {
          state.config = config;
          state.isDirty = false;
          state.validationErrors = {};
        }),
        
        // Builders
        addAporte: (aporte) => set((state) => {
          if (!state.config) return;
          state.config.aportes = [...(state.config.aportes || []), aporte];
          state.isDirty = true;
        }),
        
        // ... outros métodos
        
        validate: () => {
          const config = get().config;
          if (!config) return false;
          
          const errors = validateConfig(config);
          set({ validationErrors: errors });
          return Object.keys(errors).length === 0;
        },
        
        clearErrors: () => set({ validationErrors: {} }),
      })),
      {
        name: 'sam-config-storage',
        partialize: (state) => ({ config: state.config }), // Persiste só config
      }
    ),
    { name: 'ConfigStore' }
  )
);
Store Secundário: ProjectionStore
typescript// src/features/projection/stores/projectionStore.ts
interface ProjectionState {
  // Dados da projeção
  data: ProjectionData | null;
  kpis: KPIs | null;
  insights: Insight[] | null;
  
  // Filtros globais
  filters: {
    periodStart: number;
    periodEnd: number;
    granularity: 'monthly' | 'quarterly' | 'yearly';
    scenarioName: string;
  };
  
  // UI State
  activeDashboard: string;
  drillDownStack: DrillDownLevel[];
  
  // Ações
  setProjectionData: (data: ProjectionData) => void;
  setKPIs: (kpis: KPIs) => void;
  setInsights: (insights: Insight[]) => void;
  
  updateFilters: (filters: Partial<ProjectionState['filters']>) => void;
  
  drillDown: (level: DrillDownLevel) => void;
  drillUp: () => void;
  clearDrillDown: () => void;
  
  setActiveDashboard: (name: string) => void;
}

export const useProjectionStore = create<ProjectionState>()(
  devtools((set) => ({
    // Estado inicial
    data: null,
    kpis: null,
    insights: null,
    filters: {
      periodStart: 1,
      periodEnd: 36,
      granularity: 'monthly',
      scenarioName: 'base',
    },
    activeDashboard: 'overview',
    drillDownStack: [],
    
    // Implementação
    setProjectionData: (data) => set({ data }),
    setKPIs: (kpis) => set({ kpis }),
    setInsights: (insights) => set({ insights }),
    
    updateFilters: (newFilters) => set((state) => ({
      filters: { ...state.filters, ...newFilters },
    })),
    
    drillDown: (level) => set((state) => ({
      drillDownStack: [...state.drillDownStack, level],
    })),
    
    drillUp: () => set((state) => ({
      drillDownStack: state.drillDownStack.slice(0, -1),
    })),
    
    clearDrillDown: () => set({ drillDownStack: [] }),
    
    setActiveDashboard: (name) => set({ activeDashboard: name }),
  }), { name: 'ProjectionStore' })
);
Store de Cenários
typescript// src/features/scenarios/stores/scenarioStore.ts
interface ScenarioState {
  scenarios: Record<string, ConfigFinanceira>;
  activeScenario: string;
  comparisonScenarios: string[];
  
  saveScenario: (name: string, config: ConfigFinanceira) => void;
  loadScenario: (name: string) => ConfigFinanceira | null;
  deleteScenario: (name: string) => void;
  setActiveScenario: (name: string) => void;
  addToComparison: (name: string) => void;
  removeFromComparison: (name: string) => void;
  clearComparison: () => void;
}

export const useScenarioStore = create<ScenarioState>()(
  persist(
    (set, get) => ({
      scenarios: {
        base: getDefaultConfig(),
      },
      activeScenario: 'base',
      comparisonScenarios: [],
      
      saveScenario: (name, config) => set((state) => ({
        scenarios: { ...state.scenarios, [name]: config },
      })),
      
      loadScenario: (name) => {
        return get().scenarios[name] || null;
      },
      
      deleteScenario: (name) => set((state) => {
        const { [name]: _, ...rest } = state.scenarios;
        return { scenarios: rest };
      }),
      
      setActiveScenario: (name) => set({ activeScenario: name }),
      
      addToComparison: (name) => set((state) => ({
        comparisonScenarios: [...state.comparisonScenarios, name],
      })),
      
      removeFromComparison: (name) => set((state) => ({
        comparisonScenarios: state.comparisonScenarios.filter(s => s !== name),
      })),
      
      clearComparison: () => set({ comparisonScenarios: [] }),Tentar novamenteWIContinuar})),
{ name: 'sam-scenarios-storage' }
)
);

## 4.3 Gerenciamento de Formulários: **React Hook Form** 🏆

### **Por que React Hook Form?**

✅ **Performance:** Re-renders mínimos (uncontrolled components)  
✅ **TypeScript:** Inferência automática de tipos  
✅ **Validação:** Integração nativa com Zod  
✅ **API Simples:** Menos código que Formik  
✅ **Tamanho:** ~9KB gzipped  
✅ **DevTools:** React Hook Form DevTools  

### **Comparação com Alternativas:**

| Biblioteca | Prós | Contras | Recomendação |
|------------|------|---------|--------------|
| **React Hook Form** | ✅ Performance<br>✅ TypeScript<br>✅ Validação | ❌ Curva inicial | **RECOMENDADO** |
| Formik | ✅ Maduro<br>✅ Popular | ❌ Re-renders<br>❌ Pesado | Não recomendado |
| Final Form | ✅ Flexível | ❌ Complexo<br>❌ Menos usado | Não recomendado |

### **Implementação do Formulário de Configuração**
```typescript
// src/features/configuration/hooks/useConfigForm.ts
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Schema de validação Zod
const configSchema = z.object({
  // Capital
  capital: z.object({
    inicial: z.number().min(-1000000, "Valor mínimo: -R$1M"),
    aportes: z.array(z.object({
      mes: z.number().min(1).max(60),
      valor: z.number().min(0),
      tipo: z.enum(['equity', 'divida']),
      diluicao: z.number().min(0).max(100).optional(),
    })),
  }),
  
  // Funil de Aquisição
  funil: z.object({
    visitantesMes1: z.number().min(0),
    taxaCrescimentoMensal: z.number().min(0).max(1),
    canais: z.array(z.object({
      nome: z.string().min(1, "Nome obrigatório"),
      percentualTrafego: z.number().min(0).max(1),
      taxaConversaoTrial: z.number().min(0).max(1),
      taxaConversaoPagante: z.number().min(0).max(1),
      cacMedio: z.number().min(0),
    })),
  }),
  
  // Receita
  receita: z.object({
    planos: z.array(z.object({
      nome: z.string().min(1),
      preco: z.number().min(0),
      mixInicial: z.number().min(0).max(1),
      mixAno2: z.number().min(0).max(1).optional(),
      mixAno3: z.number().min(0).max(1).optional(),
    })),
    upsellMensal: z.number().min(0).max(1).optional(),
    churnMensal: z.number().min(0).max(1),
  }),
  
  // COGS
  cogs: z.object({
    custoIAPorUsuario: z.number().min(0),
    aliquotaImpostos: z.number().min(0).max(1),
    taxaPagamentoPercentual: z.number().min(0).max(1),
    taxaPagamentoFixa: z.number().min(0),
    comissaoAfiliados: z.object({
      percentual: z.number().min(0).max(1),
      percentualVendasViaAfiliados: z.number().min(0).max(1),
    }).optional(),
  }),
  
  // Infraestrutura
  infra: z.object({
    tiers: z.array(z.object({
      numero: z.number().min(1),
      limitMin: z.number().min(0),
      limitMax: z.number().min(0),
      custoFixo: z.number().min(0),
      custoPorUsuario: z.number().min(0).optional(),
      detalhes: z.record(z.string(), z.number()).optional(),
    })),
  }),
  
  // Marketing
  marketing: z.object({
    fases: z.array(z.object({
      numero: z.number().min(1),
      nome: z.string(),
      duracaoMeses: z.number().min(1).optional(),
      orcamentoFixo: z.number().min(0).optional(),
      orcamentoPercentualLucro: z.number().min(0).max(1).optional(),
      orcamentoPercentualReceita: z.number().min(0).max(1).optional(),
      gatilhos: z.array(z.object({
        tipo: z.enum(['mrr', 'usuarios', 'mes', 'lucro']),
        valor: z.number(),
      })).optional(),
    })),
  }),
  
  // Equipe
  equipe: z.object({
    fundador: z.object({
      fases: z.array(z.object({
        mesInicio: z.number().min(1),
        mesFim: z.number().nullable(),
        salario: z.number().min(0),
        gatilhos: z.array(z.object({
          tipo: z.enum(['mrr', 'lucro', 'caixa']),
          valor: z.number(),
        })).optional(),
      })),
      proLabore: z.object({
        percentualLucro: z.number().min(0).max(1),
        minimo: z.number().min(0),
        maximo: z.number().optional(),
      }).optional(),
    }),
    cargos: z.array(z.object({
      nome: z.string().min(1),
      cargo: z.string().min(1),
      tipo: z.enum(['CLT', 'PJ']),
      salario: z.number().min(0),
      encargos: z.number().min(0).max(1).optional(),
      gatilhos: z.array(z.object({
        tipo: z.enum(['mrr', 'usuarios', 'mes', 'lucro']),
        valor: z.number(),
      })),
      beneficios: z.object({
        vr: z.number().min(0).optional(),
        vt: z.number().min(0).optional(),
        planoSaude: z.number().min(0).optional(),
      }).optional(),
      reajusteAnual: z.number().min(0).max(1).optional(),
    })),
  }),
  
  // Ferramentas
  ferramentas: z.object({
    categorias: z.record(z.string(), z.array(z.object({
      nome: z.string().min(1),
      custoMensal: z.number().min(0),
      mesInicio: z.number().min(1),
      essencial: z.boolean(),
      custoPorUsuario: z.number().min(0).optional(),
    }))),
  }),
});

type ConfigFormData = z.infer<typeof configSchema>;

export function useConfigForm() {
  const { config, setConfig, isDirty, validate } = useConfigStore();
  
  const form = useForm<ConfigFormData>({
    resolver: zodResolver(configSchema),
    defaultValues: config || getDefaultConfig(),
    mode: 'onChange', // Valida enquanto digita
  });
  
  const { handleSubmit, watch, formState: { errors, isSubmitting } } = form;
  
  // Sincroniza formulário com store
  const watchedValues = watch();
  useEffect(() => {
    setConfig(watchedValues);
  }, [watchedValues, setConfig]);
  
  return {
    form,
    errors,
    isSubmitting,
    isDirty,
    onSubmit: handleSubmit(async (data) => {
      // Lógica de submissão (chamada à API)
    }),
  };
}
```

### **Exemplo de Componente de Formulário**
```typescript
// src/pages/ConfigurationPage/sections/CapitalSection.tsx
import { useFormContext } from 'react-hook-form';
import { FormField } from '@/components/forms/FormField';
import { CurrencyInput } from '@/components/forms/CurrencyInput';
import { Button } from '@/components/ui/Button';

export function CapitalSection() {
  const { control, watch } = useFormContext();
  const aportes = watch('capital.aportes') || [];
  
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Capital e Financiamento</h2>
      
      {/* Capital Inicial */}
      <FormField
        name="capital.inicial"
        control={control}
        label="Capital Inicial (CAPEX)"
        helperText="Valor negativo = saída de caixa"
        render={({ field }) => (
          <CurrencyInput
            {...field}
            placeholder="-8.000,00"
            allowNegative
          />
        )}
      />
      
      {/* Aportes Programados */}
      <div className="border rounded-lg p-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Aportes Programados</h3>
          <Button
            type="button"
            variant="secondary"
            onClick={() => {
              // Adiciona novo aporte
            }}
          >
            + Adicionar Aporte
          </Button>
        </div>
        
        {aportes.map((aporte, index) => (
          <AporteRow key={index} index={index} />
        ))}
      </div>
    </div>
  );
}
```

---

# 5. COMUNICAÇÃO COM API {#5-comunicação-com-api}

## 5.1 Recomendação: **TanStack Query (React Query)** 🏆

### **Por que TanStack Query?**

✅ **Cache Inteligente:** Evita requisições redundantes  
✅ **Background Sync:** Atualiza dados automaticamente  
✅ **Loading/Error States:** Gerenciamento automático  
✅ **Mutations:** POST/PUT/DELETE simplificados  
✅ **Optimistic Updates:** UI responsiva  
✅ **Retry Logic:** Tentativas automáticas  
✅ **DevTools:** Excelente ferramenta de debug  
✅ **TypeScript:** Inferência automática  

### **Comparação com Alternativas:**

| Biblioteca | Prós | Contras | Recomendação |
|------------|------|---------|--------------|
| **TanStack Query** | ✅ Cache<br>✅ Features<br>✅ TypeScript | ❌ Curva inicial | **RECOMENDADO** |
| SWR | ✅ Simples<br>✅ Leve | ❌ Menos features | Alternativa |
| RTK Query | ✅ Redux integrado | ❌ Boilerplate<br>❌ Depende Redux | Não recomendado |
| Fetch + useEffect | ✅ Nativo | ❌ Muito manual<br>❌ Boilerplate | Não recomendado |

## 5.2 Configuração da API Client
```typescript
// src/lib/api/client.ts
import axios, { AxiosInstance, AxiosError } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

class APIClient {
  private client: AxiosInstance;
  
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000, // 30 segundos (projeção pode demorar)
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    this.setupInterceptors();
  }
  
  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Adiciona token de autenticação (futuro)
        // const token = getAuthToken();
        // if (token) {
        //   config.headers.Authorization = `Bearer ${token}`;
        // }
        
        console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => Promise.reject(error)
    );
    
    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        console.log(`[API] Response:`, response.status);
        return response;
      },
      (error: AxiosError) => {
        console.error(`[API] Error:`, error.response?.status, error.message);
        
        // Tratamento de erros comuns
        if (error.response?.status === 401) {
          // Redireciona para login (futuro)
        }
        
        if (error.response?.status === 422) {
          // Erros de validação do FastAPI
          const detail = error.response.data;
          throw new ValidationError(detail);
        }
        
        throw error;
      }
    );
  }
  
  // POST: Executar projeção
  async runProjection(config: ConfigFinanceira): Promise<ProjectionResponse> {
    const response = await this.client.post<ProjectionResponse>(
      '/projecao/',
      config
    );
    return response.data;
  }
  
  // GET: Health check (futuro)
  async healthCheck(): Promise<{ status: string }> {
    const response = await this.client.get('/health');
    return response.data;
  }
}

export const apiClient = new APIClient();

// Custom error class
export class ValidationError extends Error {
  constructor(public details: any) {
    super('Validation Error');
    this.name = 'ValidationError';
  }
}
```

## 5.3 Hooks de API com TanStack Query
```typescript
// src/features/projection/hooks/useProjection.ts
import { useMutation, useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import { useConfigStore } from '@/features/configuration/stores/configStore';
import { useProjectionStore } from '@/features/projection/stores/projectionStore';
import { toast } from 'sonner'; // Para notificações

export function useProjection() {
  const config = useConfigStore((state) => state.config);
  const { setProjectionData, setKPIs, setInsights } = useProjectionStore();
  
  const mutation = useMutation({
    mutationFn: (config: ConfigFinanceira) => apiClient.runProjection(config),
    
    onMutate: async () => {
      // Feedback imediato ao usuário
      toast.loading('Executando projeção...', { id: 'projection' });
    },
    
    onSuccess: (data) => {
      // Salva dados no store
      setProjectionData(data.projecao_df);
      setKPIs(data.kpis);
      setInsights(data.insights);
      
      toast.success('Projeção concluída!', { id: 'projection' });
    },
    
    onError: (error) => {
      console.error('Erro na projeção:', error);
      
      if (error instanceof ValidationError) {
        toast.error('Erro de validação nos dados', { id: 'projection' });
      } else {
        toast.error('Erro ao executar projeção', { id: 'projection' });
      }
    },
  });
  
  return {
    runProjection: mutation.mutate,
    isLoading: mutation.isPending,
    isError: mutation.isError,
    error: mutation.error,
    data: mutation.data,
  };
}
```

### **Hook para Monte Carlo (exemplo de operação longa)**
```typescript
// src/features/analytics/hooks/useMonteCarlo.ts
import { useMutation } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';

export function useMonteCarlo() {
  const mutation = useMutation({
    mutationFn: async (params: MonteCarloParams) => {
      const response = await apiClient.runMonteCarlo(params);
      return response;
    },
    
    onMutate: () => {
      toast.loading('Executando simulação Monte Carlo (1000 cenários)...', {
        id: 'montecarlo',
        duration: Infinity, // Não fecha automaticamente
      });
    },
    
    onSuccess: (data) => {
      toast.success(`Monte Carlo concluído! ${data.simulations} simulações`, {
        id: 'montecarlo',
      });
    },
    
    onError: () => {
      toast.error('Erro na simulação Monte Carlo', { id: 'montecarlo' });
    },
  });
  
  return {
    runMonteCarlo: mutation.mutate,
    isLoading: mutation.isPending,
    progress: mutation.data?.progress, // Se API retornar progresso
    results: mutation.data,
  };
}
```

## 5.4 Query Client Configuration
```typescript
// src/app/providers.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutos
      gcTime: 10 * 60 * 1000, // 10 minutos (antes cacheTime)
      retry: 1, // Tenta 1 vez em caso de erro
      refetchOnWindowFocus: false, // Não refetch ao focar janela
      refetchOnReconnect: false,
    },
    mutations: {
      retry: 0, // Não tenta novamente mutations
    },
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

## 5.5 Tipos da API (compartilhados)
```typescript
// src/lib/api/types.ts

// Request
export interface ConfigFinanceira {
  // ... (mesma estrutura do backend)
}

// Response
export interface ProjectionResponse {
  projecao_df: ProjectionData;
  kpis: KPIs;
  insights?: Insight[];
  eventos?: Event[];
}

export interface ProjectionData {
  mes: number[];
  Usuarios_Iniciais: number[];
  Visitantes: number[];
  Novos_Trials: number[];
  Novos_Pagantes: number[];
  Usuarios_Perdidos: number[];
  Usuarios_Finais: number[];
  MRR: number[];
  ARR: number[];
  ARPU: number[];
  Custo_IA: number[];
  Impostos: number[];
  Taxas_Pagamento: number[];
  COGS_Total: number[];
  Lucro_Bruto: number[];
  Margem_Bruta_Pct: number[];
  Custo_Infra: number[];
  Tier_Infra: number[];
  Custo_Marketing: number[];
  Fase_Marketing: number[];
  Salario_Fundador: number[];
  Custo_Pessoal_CLT: number[];
  Custo_Pessoal_PJ: number[];
  Custo_Ferramentas: number[];
  OPEX_Total: number[];
  EBITDA: number[];
  Resultado_Operacional: number[];
  Aportes: number[];
  Fluxo_Caixa: number[];
  Saldo_Caixa: number[];
  CAC_Mensal: number[];
  LTV: number[];
  LTV_CAC_Ratio: number[];
  Payback_Meses: number[];
  Receita_Total: number[];
  Churn_Absoluto: number[];
  // ... outros campos
}

export interface KPIs {
  Break_Even_Mes: number | null;
  Payback_Investimento_Mes: number | null;
  Vale_da_Morte_Minimo_Caixa: number;
  Vale_da_Morte_Mes: number;
  Runway_Meses: number | string;
  LTV_Final: number;
  CAC_Medio_Periodo: number;
  LTV_CAC_Ratio_Final: number;
  CAC_Payback_Meses_Config: number;
  MRR_Ano1: number;
  MRR_Ano2: number;
  MRR_Ano3: number;
  Usuarios_Ano1: number;
  Usuarios_Ano2: number;
  Usuarios_Ano3: number;
  Saldo_Caixa_Final: number;
  MRR_Final: number;
  Usuarios_Final: number;
  eventos: Event[];
}

export interface Insight {
  level: 'CRITICAL' | 'WARNING' | 'INFO' | 'SUCCESS';
  category: 'caixa' | 'crescimento' | 'custos' | 'unit_economics';
  title: string;
  description: string;
  value?: number;
  action?: string;
  impact?: string;
}

export interface Event {
  mes: number;
  tipo: string;
  descricao: string;
  valor: number;
}
```

---

# 6. BIBLIOTECA DE GRÁFICOS {#6-biblioteca-de-gráficos}

## 6.1 Recomendação: **Recharts + Plotly.js** 🏆

### **Estratégia Híbrida (Melhor dos 2 Mundos)**

**Recharts (Principal):** Para 80% dos gráficos  
**Plotly.js (Complementar):** Para 20% dos gráficos avançados  

### **Por que Recharts?**

✅ **React-First:** Componentes React nativos  
✅ **Composição:** API declarativa e intuitiva  
✅ **TypeScript:** Excelente suporte  
✅ **Responsivo:** Out-of-the-box  
✅ **Customização:** Fácil de estilizar  
✅ **Performance:** Bom para datasets médios  
✅ **Tamanho:** ~100KB gzipped  
✅ **Documentação:** Excelente  

### **Por que Plotly.js (complementar)?**

✅ **Gráficos Avançados:** Sankey, Waterfall, 3D, Heatmaps  
✅ **Interatividade:** Zoom, pan, hover rico  
✅ **Exportação:** PNG, SVG, PDF built-in  
✅ **Maduro:** Usado por Jupyter, Dash  
❌ **Tamanho:** ~3MB gzipped (usar bundle básico: ~800KB)  
❌ **React:** Precisa de wrapper  

### **Comparação Completa:**

| Biblioteca | Tipos de Gráfico | Performance | React Integration | Tamanho | Recomendação |
|------------|------------------|-------------|-------------------|---------|--------------|
| **Recharts** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **PRINCIPAL** |
| **Plotly.js** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | **COMPLEMENTAR** |
| Chart.js | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Alternativa |
| D3.js | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | Muito complexo |
| Victory | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Alternativa |
| Nivo | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Alternativa |

## 6.2 Distribuição de Responsabilidades

### **Use Recharts para:**
✅ Line Charts (MRR, usuários, caixa)  
✅ Area Charts (stacked ou não)  
✅ Bar Charts (comparações)  
✅ Combo Charts (barras + linhas)  
✅ Pie/Donut Charts (breakdowns)  
✅ Scatter Plots  
✅ Radial Charts  

### **Use Plotly.js para:**
✅ Waterfall Charts (receita → lucro)  
✅ Sankey Diagrams (fluxo de dinheiro)  
✅ Funnel Charts (conversão)  
✅ Heatmaps 2D (sensibilidade)  
✅ 3D Surface Plots (se necessário)  
✅ Box Plots (distribuições)  
✅ Cohort Heatmaps  
✅ Gauge Charts (velocímetros)  

## 6.3 Implementação dos Componentes de Gráfico

### **Container Base (Recharts)**
```typescript
// src/components/charts/ChartContainer.tsx
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Download, Maximize2 } from 'lucide-react';

interface ChartContainerProps {
  title: string;
  subtitle?: string;
  loading?: boolean;
  error?: string;
  isEmpty?: boolean;
  emptyMessage?: string;
  height?: number | string;
  onExport?: () => void;
  onFullscreen?: () => void;
  children: React.ReactNode;
}

export function ChartContainer({
  title,
  subtitle,
  loading,
  error,
  isEmpty,
  emptyMessage = 'Sem dados para exibir',
  height = 400,
  onExport,
  onFullscreen,
  children,
}: ChartContainerProps) {
  if (loading) {
    return (
      <Card className="p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold">{title}</h3>
            {subtitle && <p className="text-sm text-gray-500">{subtitle}</p>}
          </div>
        </div>
        <div className="flex items-center justify-center" style={{ height }}>
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      </Card>
    );
  }
  
  if (error) {
    return (
      <Card className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">{title}</h3>
        </div>
        <div className="flex items-center justify-center" style={{ height }}>
          <div className="text-center">
            <p className="text-red-600 font-semibold mb-2">Erro ao carregar gráfico</p>
            <p className="text-sm text-gray-500">{error}</p>
          </div>
        </div>
      </Card>
    );
  }
  
  if (isEmpty) {
    return (
      <Card className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">{title}</h3>
        </div>
        <div className="flex items-center justify-center" style={{ height }}>
          <div className="text-center">
            <p className="text-gray-500">{emptyMessage}</p>
          </div>
        </div>
      </Card>
    );
  }
  
  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold">{title}</h3>
          {subtitle && <p className="text-sm text-gray-500">{subtitle}</p>}
        </div>
        <div className="flex gap-2">
          {onExport && (
            <Button variant="ghost" size="sm" onClick={onExport}>
              <Download className="w-4 h-4" />
            </Button>
          )}
          {onFullscreen && (
            <Button variant="ghost" size="sm" onClick={onFullscreen}>
              <Maximize2 className="w-4 h-4" />
            </Button>
          )}
        </div>
      </div>
      <div style={{ height }}>
        {children}
      </div>
    </Card>
  );
}
```

### **Line Chart (Recharts)**
```typescript
// src/components/charts/LineChart.tsx
import { LineChart as RechartsLineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { ChartContainer } from './ChartContainer';
import { CHART_COLORS } from '@/lib/theme/colors';

interface LineChartProps {
  title: string;
  subtitle?: string;
  data: Array<Record<string, any>>;
  xKey: string;
  yKeys: string[];
  yLabels?: Record<string, string>;
  colors?: string[];
  formatValue?: (value: number) => string;
  formatXAxis?: (value: any) => string;
  height?: number;
  loading?: boolean;
}

export function LineChart({
  title,
  subtitle,
  data,
  xKey,
  yKeys,
  yLabels = {},
  colors = CHART_COLORS,
  formatValue = (v) => v.toLocaleString('pt-BR'),
  formatXAxis = (v) => `Mês ${v}`,
  height = 400,
  loading,
}: LineChartProps) {
  return (
    <ChartContainer
      title={title}
      subtitle={subtitle}
      height={height}
      loading={loading}Tentar novamenteWIContinuartypescript      isEmpty={!data || data.length === 0}
    >
      <ResponsiveContainer width="100%" height="100%">
        <RechartsLineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis
            dataKey={xKey}
            tickFormatter={formatXAxis}
            stroke="#666"
            style={{ fontSize: '12px' }}
          />
          <YAxis
            tickFormatter={formatValue}
            stroke="#666"
            style={{ fontSize: '12px' }}
          />
          <Tooltip
            formatter={(value: number) => formatValue(value)}
            labelFormatter={formatXAxis}
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e0e0e0',
              borderRadius: '8px',
              padding: '12px',
            }}
          />
          <Legend
            formatter={(value) => yLabels[value] || value}
            wrapperStyle={{ paddingTop: '20px' }}
          />
          {yKeys.map((key, index) => (
            <Line
              key={key}
              type="monotone"
              dataKey={key}
              stroke={colors[index % colors.length]}
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 6 }}
              name={yLabels[key] || key}
            />
          ))}
        </RechartsLineChart>
      </ResponsiveContainer>
    </ChartContainer>
  );
}
Combo Chart (Recharts)
typescript// src/components/charts/ComboChart.tsx
import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { ChartContainer } from './ChartContainer';
import { CHART_COLORS } from '@/lib/theme/colors';

interface ComboChartProps {
  title: string;
  subtitle?: string;
  data: Array<Record<string, any>>;
  xKey: string;
  barKeys: string[];
  lineKeys: string[];
  barLabels?: Record<string, string>;
  lineLabels?: Record<string, string>;
  formatValue?: (value: number) => string;
  height?: number;
  stacked?: boolean;
}

export function ComboChart({
  title,
  subtitle,
  data,
  xKey,
  barKeys,
  lineKeys,
  barLabels = {},
  lineLabels = {},
  formatValue = (v) => v.toLocaleString('pt-BR'),
  height = 400,
  stacked = false,
}: ComboChartProps) {
  return (
    <ChartContainer title={title} subtitle={subtitle} height={height}>
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis
            dataKey={xKey}
            tickFormatter={(v) => `Mês ${v}`}
            stroke="#666"
          />
          <YAxis tickFormatter={formatValue} stroke="#666" />
          <Tooltip
            formatter={(value: number) => formatValue(value)}
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e0e0e0',
              borderRadius: '8px',
            }}
          />
          <Legend />
          
          {/* Barras */}
          {barKeys.map((key, index) => (
            <Bar
              key={key}
              dataKey={key}
              fill={CHART_COLORS[index]}
              name={barLabels[key] || key}
              stackId={stacked ? 'stack' : undefined}
            />
          ))}
          
          {/* Linhas */}
          {lineKeys.map((key, index) => (
            <Line
              key={key}
              type="monotone"
              dataKey={key}
              stroke={CHART_COLORS[barKeys.length + index]}
              strokeWidth={2}
              dot={false}
              name={lineLabels[key] || key}
            />
          ))}
        </ComposedChart>
      </ResponsiveContainer>
    </ChartContainer>
  );
}
Waterfall Chart (Plotly.js)
typescript// src/components/charts/WaterfallChart.tsx
import { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-basic-dist';
import { ChartContainer } from './ChartContainer';

interface WaterfallItem {
  label: string;
  value: number;
  type: 'increase' | 'decrease' | 'total';
}

interface WaterfallChartProps {
  title: string;
  subtitle?: string;
  items: WaterfallItem[];
  formatValue?: (value: number) => string;
  height?: number;
}

export function WaterfallChart({
  title,
  subtitle,
  items,
  formatValue = (v) => `R$ ${v.toLocaleString('pt-BR')}`,
  height = 400,
}: WaterfallChartProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (!chartRef.current) return;
    
    const x = items.map(item => item.label);
    const y = items.map(item => item.value);
    const measure = items.map(item => {
      if (item.type === 'total') return 'total';
      return 'relative';
    });
    
    const colors = items.map(item => {
      if (item.type === 'total') return '#2E86AB';
      return item.type === 'increase' ? '#06A77D' : '#D62828';
    });
    
    const data = [{
      type: 'waterfall',
      x,
      y,
      measure,
      text: y.map(formatValue),
      textposition: 'outside',
      connector: {
        line: { color: '#999', width: 2, dash: 'dot' }
      },
      increasing: { marker: { color: '#06A77D' } },
      decreasing: { marker: { color: '#D62828' } },
      totals: { marker: { color: '#2E86AB' } },
    }];
    
    const layout = {
      showlegend: false,
      margin: { l: 60, r: 40, t: 20, b: 100 },
      xaxis: { tickangle: -45 },
      yaxis: { tickformat: ',.0f' },
      height,
    };
    
    const config = {
      responsive: true,
      displayModeBar: true,
      modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
      displaylogo: false,
    };
    
    Plotly.newPlot(chartRef.current, data as any, layout, config);
    
    return () => {
      if (chartRef.current) {
        Plotly.purge(chartRef.current);
      }
    };
  }, [items, formatValue, height]);
  
  return (
    <ChartContainer title={title} subtitle={subtitle} height={height}>
      <div ref={chartRef} style={{ width: '100%', height: '100%' }} />
    </ChartContainer>
  );
}
Sankey Diagram (Plotly.js)
typescript// src/components/charts/SankeyChart.tsx
import { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-basic-dist';
import { ChartContainer } from './ChartContainer';

interface SankeyNode {
  label: string;
  color?: string;
}

interface SankeyLink {
  source: number; // Índice do nó de origem
  target: number; // Índice do nó de destino
  value: number;
  color?: string;
}

interface SankeyChartProps {
  title: string;
  subtitle?: string;
  nodes: SankeyNode[];
  links: SankeyLink[];
  height?: number;
}

export function SankeyChart({
  title,
  subtitle,
  nodes,
  links,
  height = 500,
}: SankeyChartProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (!chartRef.current) return;
    
    const data = [{
      type: 'sankey',
      node: {
        pad: 15,
        thickness: 20,
        line: { color: 'white', width: 1 },
        label: nodes.map(n => n.label),
        color: nodes.map(n => n.color || '#2E86AB'),
      },
      link: {
        source: links.map(l => l.source),
        target: links.map(l => l.target),
        value: links.map(l => l.value),
        color: links.map(l => l.color || 'rgba(46, 134, 171, 0.3)'),
      },
    }];
    
    const layout = {
      font: { size: 12 },
      margin: { l: 20, r: 20, t: 20, b: 20 },
      height,
    };
    
    const config = {
      responsive: true,
      displayModeBar: true,
      modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
      displaylogo: false,
    };
    
    Plotly.newPlot(chartRef.current, data as any, layout, config);
    
    return () => {
      if (chartRef.current) {
        Plotly.purge(chartRef.current);
      }
    };
  }, [nodes, links, height]);
  
  return (
    <ChartContainer title={title} subtitle={subtitle} height={height}>
      <div ref={chartRef} style={{ width: '100%', height: '100%' }} />
    </ChartContainer>
  );
}
Gauge Chart (Plotly.js)
typescript// src/components/charts/GaugeChart.tsx
import { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-basic-dist';
import { ChartContainer } from './ChartContainer';

interface GaugeChartProps {
  title: string;
  value: number;
  min?: number;
  max?: number;
  target?: number;
  ranges?: Array<{
    range: [number, number];
    color: string;
    label: string;
  }>;
  height?: number;
}

export function GaugeChart({
  title,
  value,
  min = 0,
  max = 10,
  target,
  ranges = [
    { range: [0, 3], color: '#D62828', label: 'Crítico' },
    { range: [3, 5], color: '#F77F00', label: 'Atenção' },
    { range: [5, 10], color: '#06A77D', label: 'Saudável' },
  ],
  height = 300,
}: GaugeChartProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (!chartRef.current) return;
    
    const data = [{
      type: 'indicator',
      mode: 'gauge+number+delta',
      value,
      delta: target ? { reference: target } : undefined,
      gauge: {
        axis: { range: [min, max] },
        bar: { color: '#2E86AB' },
        steps: ranges.map(r => ({
          range: r.range,
          color: r.color,
        })),
        threshold: target ? {
          line: { color: 'black', width: 2 },
          thickness: 0.75,
          value: target,
        } : undefined,
      },
    }];
    
    const layout = {
      margin: { t: 20, b: 20, l: 40, r: 40 },
      height,
      font: { size: 14 },
    };
    
    const config = {
      responsive: true,
      displayModeBar: false,
    };
    
    Plotly.newPlot(chartRef.current, data as any, layout, config);
    
    return () => {
      if (chartRef.current) {
        Plotly.purge(chartRef.current);
      }
    };
  }, [value, min, max, target, ranges, height]);
  
  return (
    <ChartContainer title={title} height={height}>
      <div ref={chartRef} style={{ width: '100%', height: '100%' }} />
    </ChartContainer>
  );
}
Cohort Heatmap (Recharts)
typescript// src/components/charts/CohortHeatmap.tsx
import { ChartContainer } from './ChartContainer';

interface CohortData {
  cohort: string;
  retention: Record<string, number>; // { M0: 100, M1: 95, M2: 91, ... }
}

interface CohortHeatmapProps {
  title: string;
  data: CohortData[];
  maxMonths?: number;
}

export function CohortHeatmap({
  title,
  data,
  maxMonths = 12,
}: CohortHeatmapProps) {
  const getColor = (value: number) => {
    if (value >= 90) return 'bg-green-600';
    if (value >= 80) return 'bg-green-500';
    if (value >= 70) return 'bg-yellow-500';
    if (value >= 60) return 'bg-orange-500';
    return 'bg-red-500';
  };
  
  const months = Array.from({ length: maxMonths }, (_, i) => `M${i}`);
  
  return (
    <ChartContainer title={title} height="auto">
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr>
              <th className="border p-2 bg-gray-100 text-left font-semibold">
                Cohort
              </th>
              {months.map(month => (
                <th key={month} className="border p-2 bg-gray-100 text-center font-semibold">
                  {month}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((cohort) => (
              <tr key={cohort.cohort}>
                <td className="border p-2 font-medium">{cohort.cohort}</td>
                {months.map(month => {
                  const value = cohort.retention[month];
                  if (value === undefined) {
                    return <td key={month} className="border p-2 bg-gray-50"></td>;
                  }
                  return (
                    <td
                      key={month}
                      className={`border p-2 text-center text-white font-semibold ${getColor(value)}`}
                    >
                      {value.toFixed(0)}%
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </ChartContainer>
  );
}

7. SISTEMA DE DESIGN {#7-sistema-de-design}
7.1 Paleta de Cores
typescript// src/lib/theme/colors.ts

export const COLORS = {
  // Cores Primárias
  primary: {
    50: '#E6F2F7',
    100: '#CCE5EF',
    200: '#99CBD0',
    300: '#66B1C8',
    400: '#4A9DBD',
    500: '#2E86AB', // Cor principal
    600: '#256B8A',
    700: '#1C5068',
    800: '#133546',
    900: '#0A1A23',
  },
  
  // Sucesso (Receita, Lucro, Positivo)
  success: {
    50: '#E6F9F4',
    100: '#CCF3E9',
    200: '#99E7D3',
    300: '#66DBBD',
    400: '#36C3A2',
    500: '#06A77D', // Verde principal
    600: '#058664',
    700: '#04644B',
    800: '#034332',
    900: '#012119',
  },
  
  // Perigo (Custos, Perdas, Negativo)
  danger: {
    50: '#FBE9E9',
    100: '#F7D3D3',
    200: '#EFA7A7',
    300: '#E77B7B',
    400: '#E05050',
    500: '#D62828', // Vermelho principal
    600: '#AB2020',
    700: '#801818',
    800: '#551010',
    900: '#2B0808',
  },
  
  // Aviso (Alertas, Atenção)
  warning: {
    50: '#FFF4E6',
    100: '#FFE9CC',
    200: '#FFD399',
    300: '#FFBD66',
    400: '#FFA733',
    500: '#F77F00', // Laranja principal
    600: '#C66600',
    700: '#944C00',
    800: '#633300',
    900: '#311900',
  },
  
  // Info (Neutro, Informação)
  info: {
    50: '#EBF4FE',
    100: '#D7E9FD',
    200: '#AFD3FB',
    300: '#87BDF9',
    400: '#5FA7F7',
    500: '#4895EF', // Azul claro
    600: '#3A77BF',
    700: '#2B598F',
    800: '#1D3B60',
    900: '#0E1E30',
  },
  
  // Neutros
  gray: {
    50: '#F9FAFB',
    100: '#F3F4F6',
    200: '#E5E7EB',
    300: '#D1D5DB',
    400: '#9CA3AF',
    500: '#6B7280',
    600: '#4B5563',
    700: '#374151',
    800: '#1F2937',
    900: '#111827',
  },
};

// Cores específicas para gráficos
export const CHART_COLORS = [
  COLORS.primary[500],
  COLORS.success[500],
  COLORS.info[500],
  COLORS.warning[500],
  COLORS.danger[500],
  COLORS.primary[300],
  COLORS.success[300],
  COLORS.info[300],
  COLORS.warning[300],
  COLORS.danger[300],
];

// Cores para categorias de custo
export const COST_COLORS = {
  pessoal: '#8338EC',     // Roxo
  infra: '#3A86FF',       // Azul
  marketing: '#FB5607',   // Laranja
  ferramentas: '#FFBE0B', // Amarelo
  servicos: '#06A77D',    // Verde
  outros: '#6B7280',      // Cinza
};

// Cores para status
export const STATUS_COLORS = {
  critical: COLORS.danger[500],
  warning: COLORS.warning[500],
  success: COLORS.success[500],
  info: COLORS.info[500],
  neutral: COLORS.gray[400],
};
7.2 Design Tokens
typescript// src/lib/theme/tokens.ts

export const SPACING = {
  xs: '0.25rem',   // 4px
  sm: '0.5rem',    // 8px
  md: '1rem',      // 16px
  lg: '1.5rem',    // 24px
  xl: '2rem',      // 32px
  '2xl': '3rem',   // 48px
  '3xl': '4rem',   // 64px
};

export const FONT_SIZE = {
  xs: '0.75rem',   // 12px
  sm: '0.875rem',  // 14px
  base: '1rem',    // 16px
  lg: '1.125rem',  // 18px
  xl: '1.25rem',   // 20px
  '2xl': '1.5rem', // 24px
  '3xl': '1.875rem', // 30px
  '4xl': '2.25rem',  // 36px
};

export const FONT_WEIGHT = {
  normal: 400,
  medium: 500,
  semibold: 600,
  bold: 700,
};

export const BORDER_RADIUS = {
  none: '0',
  sm: '0.25rem',   // 4px
  md: '0.5rem',    // 8px
  lg: '0.75rem',   // 12px
  xl: '1rem',      // 16px
  full: '9999px',
};

export const SHADOW = {
  sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
  xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
};

export const TRANSITION = {
  fast: '150ms cubic-bezier(0.4, 0, 0.2, 1)',
  normal: '300ms cubic-bezier(0.4, 0, 0.2, 1)',
  slow: '500ms cubic-bezier(0.4, 0, 0.2, 1)',
};

export const Z_INDEX = {
  dropdown: 1000,
  sticky: 1020,
  fixed: 1030,
  modalBackdrop: 1040,
  modal: 1050,
  popover: 1060,
  tooltip: 1070,
};
7.3 Configuração do Tailwind
javascript// tailwind.config.js
import { COLORS, SPACING, FONT_SIZE, BORDER_RADIUS, SHADOW } from './src/lib/theme/tokens';

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: COLORS,
      spacing: SPACING,
      fontSize: FONT_SIZE,
      borderRadius: BORDER_RADIUS,
      boxShadow: SHADOW,
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-in': 'slideIn 0.3s ease-in-out',
        'scale-in': 'scaleIn 0.2s ease-in-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideIn: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

---

# 8. FLUXO DE DADOS {#8-fluxo-de-dados}

## 8.1 Fluxo Completo (Diagrama)
```
┌─────────────────────────────────────────────────────────────┐
│                    FLUXO DE DADOS COMPLETO                  │
└─────────────────────────────────────────────────────────────┘

1. CONFIGURAÇÃO (Input do Usuário)
   │
   ├─ User preenche formulário (ConfigurationPage)
   │   └─> React Hook Form captura inputs
   │       └─> Zod valida campos em tempo real
   │           └─> configStore.setConfig() atualiza estado
   │               └─> localStorage persiste (middleware)
   │
   └─> User clica "Executar Projeção"

2. SUBMISSÃO (API Call)
   │
   ├─> useProjection().runProjection()
   │   └─> TanStack Query: mutation.mutate()
   │       └─> apiClient.runProjection(config)
   │           └─> POST /projecao/ (FastAPI)
   │
   └─> Loading state (toast + skeleton)

3. PROCESSAMENTO (Backend)
   │
   ├─> FastAPI valida request
   ├─> MotorProjecaoFinanceira.executar_projecao()
   ├─> InsightsEngine.generate_all_insights()
   └─> Response: { projecao_df, kpis, insights }

4. RECEBIMENTO (Frontend)
   │
   ├─> TanStack Query: onSuccess()
   │   ├─> projectionStore.setProjectionData()
   │   ├─> projectionStore.setKPIs()
   │   └─> projectionStore.setInsights()
   │
   └─> Navegação automática para ResultsPage

5. VISUALIZAÇÃO (Dashboards)
   │
   ├─> ResultsPage renderiza
   │   ├─> GlobalFilters (sidebar)
   │   └─> Tabs (dashboards)
   │
   ├─> User seleciona "Overview Dashboard"
   │   ├─> useProjectionStore() lê dados
   │   ├─> Aplica filtros (período, granularidade)
   │   ├─> Renderiza componentes:
   │   │   ├─ AlertsSection (insights críticos)
   │   │   ├─ KPIGrid (métricas principais)
   │   │   ├─ LineChart (MRR, Caixa)
   │   │   └─ InsightsTimeline
   │   └─> Cada componente é memoizado (React.memo)
   │
   └─> User clica em MetricCard "OPEX"

6. DRILL-DOWN (Detalhamento)
   │
   ├─> MetricCard.onDrillDown()
   │   └─> projectionStore.drillDown(level)
   │       └─> DrillDownModal abre
   │           ├─ BreakdownPieChart (categorias)
   │           ├─ DataTable (detalhado)
   │           └─> User clica em "Pessoal"
   │
   ├─> Novo nível de drill-down
   │   └─> BreakdownPieChart (funcionários)
   │
   └─> Breadcrumb: Home → OPEX → Pessoal

7. EXPORTAÇÃO (Opcional)
   │
   └─> User clica "Exportar PDF"
       └─> Gera relatório completo
           └─> Download automático
8.2 Fluxo de Estado (React)
typescript// Exemplo de fluxo em um dashboard

// 1. Dashboard lê dados do store
function OverviewDashboard() {
  // Leitura do store (automático re-render se mudar)
  const data = useProjectionStore((s) => s.data);
  const kpis = useProjectionStore((s) => s.kpis);
  const filters = useProjectionStore((s) => s.filters);
  
  // 2. Aplica filtros aos dados
  const filteredData = useMemo(() => {
    if (!data) return null;
    return applyFilters(data, filters);
  }, [data, filters]);
  
  // 3. Calcula dados derivados
  const chartData = useMemo(() => {
    if (!filteredData) return [];
    return transformForChart(filteredData);
  }, [filteredData]);
  
  // 4. Renderiza componentes
  return (
    <div>
      <KPIGrid kpis={kpis} />
      <LineChart data={chartData} />
    </div>
  );
}

9. PADRÕES DE CÓDIGO {#9-padrões-de-código}
9.1 Padrão de Componente com Drill-Down
typescript// src/components/metrics/MetricCardWithDrilldown.tsx
import { useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { DrillDownModal } from '@/components/drill-down/DrillDownModal';
import { formatCurrency } from '@/lib/utils/formatters';

interface MetricCardWithDrilldownProps {
  label: string;
  value: number;
  delta?: number;
  breakdown: Record<string, number>;
  onBreakdownClick?: (category: string) => void;
}

export function MetricCardWithDrilldown({
  label,
  value,
  delta,
  breakdown,
  onBreakdownClick,
}: MetricCardWithDrilldownProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  return (
    <>
      <Card className="p-6 hover:shadow-lg transition-shadow cursor-pointer">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <p className="text-sm text-gray-500 font-medium">{label}</p>
            <p className="text-3xl font-bold mt-2">{formatCurrency(value)}</p>
            {delta !== undefined && (
              <p className={`text-sm mt-1 ${delta >= 0 ? 'text-success-500' : 'text-danger-500'}`}>
                {delta >= 0 ? '↑' : '↓'} {Math.abs(delta).toFixed(1)}%
              </p>
            )}
          </div>
          
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsModalOpen(true)}
            className="ml-4"
          >
            🔍
          </Button>
        </div>
      </Card>
      
      <DrillDownModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={`Composição: ${label}`}
        data={breakdown}
        onItemClick={onBreakdownClick}
      />
    </>
  );
}
9.2 Padrão de Custom Hook
typescript// src/features/projection/hooks/useFilteredData.ts
import {Tentar novamenteWIContinuartypescriptimport { useMemo } from 'react';
import { useProjectionStore } from '../stores/projectionStore';
import { applyPeriodFilter, applyGranularity } from '@/lib/utils/dataTransformers';

interface UseFilteredDataOptions {
  includeFilters?: boolean;
  customTransform?: (data: any) => any;
}

export function useFilteredData(options: UseFilteredDataOptions = {}) {
  const { includeFilters = true, customTransform } = options;
  
  const data = useProjectionStore((s) => s.data);
  const filters = useProjectionStore((s) => s.filters);
  
  const filteredData = useMemo(() => {
    if (!data) return null;
    
    let result = data;
    
    // Aplica filtros de período
    if (includeFilters) {
      result = applyPeriodFilter(result, filters.periodStart, filters.periodEnd);
      result = applyGranularity(result, filters.granularity);
    }
    
    // Aplica transformação customizada
    if (customTransform) {
      result = customTransform(result);
    }
    
    return result;
  }, [data, filters, includeFilters, customTransform]);
  
  return {
    data: filteredData,
    filters,
    isLoading: !data,
  };
}

// Uso em componente:
function SomeChart() {
  const { data, isLoading } = useFilteredData({
    customTransform: (d) => d.filter(row => row.MRR > 0)
  });
  
  if (isLoading) return <ChartSkeleton />;
  
  return <LineChart data={data} />;
}
9.3 Padrão de Formatação
typescript// src/lib/utils/formatters.ts

/**
 * Formata valor monetário em Real brasileiro
 */
export function formatCurrency(value: number, options?: {
  compact?: boolean;
  showSign?: boolean;
}): string {
  const { compact = false, showSign = false } = options || {};
  
  if (compact) {
    if (Math.abs(value) >= 1_000_000) {
      return `R$ ${(value / 1_000_000).toFixed(1)}M`;
    }
    if (Math.abs(value) >= 1_000) {
      return `R$ ${(value / 1_000).toFixed(1)}K`;
    }
  }
  
  const formatted = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
  
  if (showSign && value > 0) {
    return `+${formatted}`;
  }
  
  return formatted;
}

/**
 * Formata percentual
 */
export function formatPercentage(value: number, options?: {
  decimals?: number;
  showSign?: boolean;
}): string {
  const { decimals = 1, showSign = false } = options || {};
  
  const formatted = `${value.toFixed(decimals)}%`;
  
  if (showSign && value > 0) {
    return `+${formatted}`;
  }
  
  return formatted;
}

/**
 * Formata número genérico
 */
export function formatNumber(value: number, options?: {
  compact?: boolean;
  decimals?: number;
}): string {
  const { compact = false, decimals = 0 } = options || {};
  
  if (compact) {
    if (Math.abs(value) >= 1_000_000) {
      return `${(value / 1_000_000).toFixed(1)}M`;
    }
    if (Math.abs(value) >= 1_000) {
      return `${(value / 1_000).toFixed(1)}K`;
    }
  }
  
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

/**
 * Formata data/mês
 */
export function formatMonth(monthNumber: number, options?: {
  format?: 'short' | 'long';
}): string {
  const { format = 'short' } = options || {};
  
  if (format === 'short') {
    return `Mês ${monthNumber}`;
  }
  
  const year = Math.floor((monthNumber - 1) / 12) + 1;
  const month = ((monthNumber - 1) % 12) + 1;
  
  return `Ano ${year}, Mês ${month}`;
}

/**
 * Formata delta/variação
 */
export function formatDelta(value: number, type: 'currency' | 'percentage' = 'percentage'): {
  formatted: string;
  color: string;
  icon: string;
} {
  const isPositive = value >= 0;
  
  const formatted = type === 'currency' 
    ? formatCurrency(value, { showSign: true })
    : formatPercentage(value, { showSign: true });
  
  return {
    formatted,
    color: isPositive ? 'text-success-500' : 'text-danger-500',
    icon: isPositive ? '↑' : '↓',
  };
}
9.4 Padrão de Transformação de Dados
typescript// src/lib/utils/dataTransformers.ts

/**
 * Aplica filtro de período aos dados
 */
export function applyPeriodFilter<T extends { mes: number }>(
  data: T[],
  startMonth: number,
  endMonth: number
): T[] {
  return data.filter(row => row.mes >= startMonth && row.mes <= endMonth);
}

/**
 * Aplica granularidade (mensal/trimestral/anual)
 */
export function applyGranularity<T extends { mes: number }>(
  data: T[],
  granularity: 'monthly' | 'quarterly' | 'yearly'
): T[] {
  if (granularity === 'monthly') return data;
  
  const groupSize = granularity === 'quarterly' ? 3 : 12;
  const grouped: T[] = [];
  
  for (let i = 0; i < data.length; i += groupSize) {
    const chunk = data.slice(i, i + groupSize);
    
    if (chunk.length === 0) continue;
    
    // Agrega valores (soma para a maioria dos campos)
    const aggregated = chunk.reduce((acc, curr) => {
      Object.keys(curr).forEach(key => {
        if (key === 'mes') {
          acc[key] = curr[key]; // Usa o primeiro mês do período
        } else if (typeof curr[key] === 'number') {
          acc[key] = (acc[key] || 0) + curr[key];
        }
      });
      return acc;
    }, {} as T);
    
    grouped.push(aggregated);
  }
  
  return grouped;
}

/**
 * Transforma dados do backend para formato de gráfico
 */
export function transformToChartData(
  data: ProjectionData,
  keys: string[]
): Array<Record<string, any>> {
  if (!data.mes || data.mes.length === 0) return [];
  
  return data.mes.map((mes, index) => {
    const row: Record<string, any> = { mes };
    
    keys.forEach(key => {
      const value = (data as any)[key];
      row[key] = value ? value[index] : null;
    });
    
    return row;
  });
}

/**
 * Calcula breakdown de um valor
 */
export function calculateBreakdown(
  total: number,
  components: Record<string, number>
): Record<string, { value: number; percentage: number }> {
  const result: Record<string, { value: number; percentage: number }> = {};
  
  Object.entries(components).forEach(([key, value]) => {
    result[key] = {
      value,
      percentage: total > 0 ? (value / total) * 100 : 0,
    };
  });
  
  return result;
}

/**
 * Gera dados para Waterfall Chart
 */
export function generateWaterfallData(
  startValue: number,
  changes: Array<{ label: string; value: number }>,
  endLabel: string = 'Total'
): WaterfallItem[] {
  const items: WaterfallItem[] = [];
  
  // Valor inicial
  items.push({
    label: 'Início',
    value: startValue,
    type: 'total',
  });
  
  // Mudanças
  changes.forEach(change => {
    items.push({
      label: change.label,
      value: change.value,
      type: change.value >= 0 ? 'increase' : 'decrease',
    });
  });
  
  // Valor final
  const endValue = startValue + changes.reduce((sum, c) => sum + c.value, 0);
  items.push({
    label: endLabel,
    value: endValue,
    type: 'total',
  });
  
  return items;
}

/**
 * Gera dados para Sankey Diagram
 */
export function generateSankeyData(
  flows: Array<{
    from: string;
    to: string;
    value: number;
  }>
): { nodes: SankeyNode[]; links: SankeyLink[] } {
  // Extrai nós únicos
  const nodeSet = new Set<string>();
  flows.forEach(f => {
    nodeSet.add(f.from);
    nodeSet.add(f.to);
  });
  
  const nodes: SankeyNode[] = Array.from(nodeSet).map(label => ({
    label,
  }));
  
  // Mapeia índices
  const nodeIndex = new Map<string, number>();
  nodes.forEach((node, index) => {
    nodeIndex.set(node.label, index);
  });
  
  // Cria links
  const links: SankeyLink[] = flows.map(f => ({
    source: nodeIndex.get(f.from)!,
    target: nodeIndex.get(f.to)!,
    value: f.value,
  }));
  
  return { nodes, links };
}
9.5 Padrão de Validação
typescript// src/lib/utils/validators.ts
import { z } from 'zod';

/**
 * Validador de valor monetário
 */
export const currencyValidator = z.number()
  .refine((val) => !isNaN(val), 'Valor inválido')
  .refine((val) => isFinite(val), 'Valor deve ser finito');

/**
 * Validador de percentual (0-100)
 */
export const percentageValidator = z.number()
  .min(0, 'Percentual não pode ser negativo')
  .max(100, 'Percentual não pode exceder 100%');

/**
 * Validador de percentual decimal (0-1)
 */
export const decimalPercentageValidator = z.number()
  .min(0, 'Percentual não pode ser negativo')
  .max(1, 'Percentual não pode exceder 100%');

/**
 * Validador de mês (1-60)
 */
export const monthValidator = z.number()
  .int('Mês deve ser um número inteiro')
  .min(1, 'Mês mínimo: 1')
  .max(60, 'Mês máximo: 60');

/**
 * Validador customizado: soma de percentuais deve ser 100%
 */
export function validatePercentageSum(
  values: number[],
  tolerance: number = 0.01
): boolean {
  const sum = values.reduce((acc, val) => acc + val, 0);
  return Math.abs(sum - 1) <= tolerance;
}

/**
 * Validador customizado: gatilhos de contratação
 */
export function validateHiringTriggers(
  triggers: Array<{ tipo: string; valor: number }>
): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  
  if (triggers.length === 0) {
    errors.push('Pelo menos um gatilho é necessário');
  }
  
  triggers.forEach((trigger, index) => {
    if (trigger.valor <= 0) {
      errors.push(`Gatilho ${index + 1}: valor deve ser positivo`);
    }
    
    if (!['mrr', 'usuarios', 'mes', 'lucro', 'caixa'].includes(trigger.tipo)) {
      errors.push(`Gatilho ${index + 1}: tipo inválido`);
    }
  });
  
  return {
    valid: errors.length === 0,
    errors,
  };
}

10. PERFORMANCE E OTIMIZAÇÕES {#10-performance}
10.1 Estratégias de Otimização
1. Code Splitting por Rota
typescript// src/app/router.tsx
import { lazy, Suspense } from 'react';
import { createBrowserRouter } from 'react-router-dom';
import { LoadingSpinner } from '@/components/loading/LoadingSpinner';

// Lazy load de páginas
const ConfigurationPage = lazy(() => import('@/pages/ConfigurationPage'));
const ResultsPage = lazy(() => import('@/pages/ResultsPage'));

export const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <Suspense fallback={<LoadingSpinner fullScreen />}>
        <ConfigurationPage />
      </Suspense>
    ),
  },
  {
    path: '/results',
    element: (
      <Suspense fallback={<LoadingSpinner fullScreen />}>
        <ResultsPage />
      </Suspense>
    ),
  },
]);
2. Memoização de Componentes
typescript// src/components/charts/LineChart.tsx
import { memo } from 'react';

export const LineChart = memo(function LineChart({
  data,
  xKey,
  yKeys,
  // ... outras props
}: LineChartProps) {
  // Componente só re-renderiza se props mudarem
  return (
    // ... JSX
  );
}, (prevProps, nextProps) => {
  // Comparação customizada (opcional)
  return (
    prevProps.data === nextProps.data &&
    JSON.stringify(prevProps.yKeys) === JSON.stringify(nextProps.yKeys)
  );
});
3. useMemo para Cálculos Pesados
typescript// src/pages/ResultsPage/dashboards/OverviewDashboard.tsx
import { useMemo } from 'react';

function OverviewDashboard() {
  const data = useProjectionStore((s) => s.data);
  
  // Calcula apenas quando data muda
  const chartData = useMemo(() => {
    if (!data) return [];
    
    return data.mes.map((mes, index) => ({
      mes,
      MRR: data.MRR[index],
      Usuarios: data.Usuarios_Finais[index],
      Caixa: data.Saldo_Caixa[index],
    }));
  }, [data]);
  
  // Calcula KPIs derivados
  const derivedKPIs = useMemo(() => {
    if (!chartData.length) return {};
    
    return {
      mrrCrescimento: calculateGrowth(chartData.map(d => d.MRR)),
      usuariosCrescimento: calculateGrowth(chartData.map(d => d.Usuarios)),
      // ... outros cálculos pesados
    };
  }, [chartData]);
  
  return (
    // ... JSX
  );
}
4. Virtual Scrolling em Tabelas
typescript// src/components/tables/DataTable.tsx
import { useVirtualizer } from '@tanstack/react-virtual';
import { useRef } from 'react';

function DataTable({ data, columns }: DataTableProps) {
  const parentRef = useRef<HTMLDivElement>(null);
  
  const virtualizer = useVirtualizer({
    count: data.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // Altura estimada de cada linha
    overscan: 10, // Quantas linhas renderizar além do visível
  });
  
  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map(virtualRow => {
          const row = data[virtualRow.index];
          return (
            <div
              key={virtualRow.index}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: `${virtualRow.size}px`,
                transform: `translateY(${virtualRow.start}px)`,
              }}
            >
              {/* Renderiza linha */}
            </div>
          );
        })}
      </div>
    </div>
  );
}
5. Debounce em Inputs
typescript// src/hooks/useDebounce.ts
import { useEffect, useState } from 'react';

export function useDebounce<T>(value: T, delay: number = 500): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);
  
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);
  
  return debouncedValue;
}

// Uso em formulário:
function SearchInput() {
  const [search, setSearch] = useState('');
  const debouncedSearch = useDebounce(search, 300);
  
  useEffect(() => {
    // Só executa busca após 300ms sem digitação
    if (debouncedSearch) {
      performSearch(debouncedSearch);
    }
  }, [debouncedSearch]);
  
  return (
    <input
      value={search}
      onChange={(e) => setSearch(e.target.value)}
    />
  );
}
6. Lazy Loading de Dashboards
typescript// src/pages/ResultsPage/ResultsPage.tsx
import { lazy, Suspense } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs';
import { ChartSkeleton } from '@/components/loading/ChartSkeleton';

// Lazy load de cada dashboard
const OverviewDashboard = lazy(() => import('./dashboards/OverviewDashboard'));
const RevenueDashboard = lazy(() => import('./dashboards/RevenueDashboard'));
const CostsDashboard = lazy(() => import('./dashboards/CostsDashboard'));
// ... outros

export function ResultsPage() {
  return (
    <div>
      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Visão Geral</TabsTrigger>
          <TabsTrigger value="revenue">Receita</TabsTrigger>
          <TabsTrigger value="costs">Custos</TabsTrigger>
          {/* ... outros */}
        </TabsList>
        
        <TabsContent value="overview">
          <Suspense fallback={<ChartSkeleton count={4} />}>
            <OverviewDashboard />
          </Suspense>
        </TabsContent>
        
        <TabsContent value="revenue">
          <Suspense fallback={<ChartSkeleton count={3} />}>
            <RevenueDashboard />
          </Suspense>
        </TabsContent>
        
        {/* ... outros */}
      </Tabs>
    </div>
  );
}
7. Otimização de Bundle (Vite)
typescript// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    react(),
    visualizer({ open: true }), // Análise de bundle
  ],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Separa vendors grandes
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'chart-vendor': ['recharts', 'plotly.js-basic-dist'],
          'form-vendor': ['react-hook-form', '@hookform/resolvers', 'zod'],
          'query-vendor': ['@tanstack/react-query'],
          'ui-vendor': ['@radix-ui/react-dialog', '@radix-ui/react-tabs'],
        },
      },
    },
    chunkSizeWarningLimit: 1000, // Alerta se chunk > 1MB
  },
  optimizeDeps: {
    include: [
      'react',
      'react-dom',
      'recharts',
      'zustand',
      'react-hook-form',
      '@tanstack/react-query',
    ],
  },
});
10.2 Métricas de Performance
Targets de Performance:

✅ First Contentful Paint (FCP): < 1.5s
✅ Largest Contentful Paint (LCP): < 2.5s
✅ Time to Interactive (TTI): < 3.5s
✅ Total Blocking Time (TBT): < 300ms
✅ Cumulative Layout Shift (CLS): < 0.1
✅ Bundle Size Total: < 500KB (gzipped)
✅ Re-render de Dashboard: < 100ms


📝 RESUMO EXECUTIVO
✅ Decisões Arquiteturais Recomendadas
AspectoEscolhaJustificativaEstado GlobalZustandSimples, performático, TypeScript excelenteFormuláriosReact Hook Form + ZodPerformance, validação, TypeScriptData FetchingTanStack QueryCache, loading states, retry logicGráficos BaseRechartsReact-first, declarativo, responsivoGráficos AvançadosPlotly.jsWaterfall, Sankey, HeatmapsComponentes UIShadcn/ui + RadixAcessíveis, customizáveis, headlessEstilizaçãoTailwind CSSProdutividade, consistência, performanceBuild ToolViteRápido, moderno, HMR instantâneo
🎯 Próximos Passos (Fase 2)
Após aprovação desta arquitetura, irei elaborar:

Plano de Implementação Sequencial

Dividido em sprints de 3-4 dias
Prompts específicos para IA de codificação
Ordem de dependências clara


Wireframes de Alta Fidelidade

Mockups das 2 páginas principais
Detalhamento de cada dashboard
Fluxos de interação


Guia de Componentes Reutilizáveis

Biblioteca completa de componentes
Props e exemplos de uso
Storybook (opcional)


Documentação Técnica

Convenções de código
Padrões de commit
Guia de deploy




🚀 Benefícios desta Arquitetura
✅ Escalável: Fácil adicionar novos dashboards
✅ Manutenível: Código organizado e padronizado
✅ Performática: Otimizações desde o início
✅ Type-Safe: TypeScript em 100% do código
✅ Testável: Componentes isolados e puros
✅ Profissional: UI/UX de alto nível

Proposta de Arquitetura Completa! Aguardando sua aprovação para prosseguir com a Fase 2 (Plano de Implementação Detalhado). 🎯