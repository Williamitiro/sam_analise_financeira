🎯 RESPOSTAS E ESCLARECIMENTOS

1️⃣ Sobre as Tabelas Complexas - Arquitetura Recomendada
❌ NÃO - Tudo em uma única página seria caótico
✅ SIM - Estrutura Organizada em Abas/Dashboards
┌─────────────────────────────────────────────────────────────┐
│                    PÁGINA DE RESULTADOS                     │
│                   (Container Principal)                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ├─ Sidebar Esquerda (Navegação)
                              ├─ Header Superior (Filtros Globais)
                              │
                              └─ Área Principal (Tabs/Dashboards)
                                  │
                                  ├─ 📊 Dashboard: Overview
                                  │   ├─ Alertas
                                  │   ├─ KPIs Grid
                                  │   ├─ Gráficos Principais
                                  │   └─ Timeline de Marcos
                                  │
                                  ├─ 💰 Dashboard: Receita
                                  │   ├─ Waterfall Chart
                                  │   ├─ Funil de Conversão
                                  │   ├─ MRR por Plano (gráfico)
                                  │   ├─ Cohort Table
                                  │   └─ 📋 **TABELA DETALHADA DE RECEITA**
                                  │
                                  ├─ 💸 Dashboard: Custos
                                  │   ├─ Sankey Diagram
                                  │   ├─ Breakdown Pizza (drill-down)
                                  │   ├─ Fixos vs Variáveis
                                  │   └─ 📋 **TABELA DETALHADA DE CUSTOS**
                                  │
                                  ├─ 💰 Dashboard: Caixa & Viabilidade
                                  │   ├─ Gráfico de Caixa
                                  │   ├─ Runway Panel
                                  │   ├─ Simulador "E se?"
                                  │   └─ 📋 **TABELA DE FLUXO DE CAIXA**
                                  │
                                  ├─ 👥 Dashboard: Equipe
                                  │   ├─ Timeline de Contratações
                                  │   ├─ Produtividade
                                  │   └─ 📋 **TABELA DE CUSTOS DE PESSOAL**
                                  │
                                  ├─ 📢 Dashboard: Marketing
                                  │   ├─ ROI por Canal
                                  │   ├─ CAC Evolution
                                  │   └─ 📋 **TABELA DE ANÁLISE DE CANAIS**
                                  │
                                  ├─ 🎯 Dashboard: Unit Economics
                                  │   ├─ LTV Breakdown
                                  │   ├─ CAC Payback
                                  │   └─ 📋 **TABELA COMPARATIVA POR PLANO**
                                  │
                                  ├─ 📊 Dashboard: Análise de Sensibilidade
                                  │   ├─ Tornado Chart
                                  │   ├─ Heatmap 2D
                                  │   └─ 📋 **TABELA DE CENÁRIOS**
                                  │
                                  ├─ 🔄 Dashboard: Cohorts
                                  │   ├─ Retention Heatmap
                                  │   ├─ Curvas de Retenção
                                  │   └─ 📋 **TABELA COMPLETA DE COHORTS**
                                  │
                                  └─ 📋 **DASHBOARD ESPECIAL: EXPLORADOR DE DADOS**
                                      │
                                      └─ TABELA DINÂMICA MASTER
                                          ├─ TODAS as colunas disponíveis
                                          ├─ Filtros avançados (multi-coluna)
                                          ├─ Agrupamentos customizáveis
                                          ├─ Comparação de cenários
                                          ├─ Exportação (CSV/Excel/PDF)
                                          └─ Visualizações rápidas
                                              ├─ DRE Completo
                                              ├─ Fluxo de Caixa
                                              ├─ Breakdown de Receita
                                              ├─ Breakdown de COGS
                                              ├─ Breakdown de OPEX
                                              └─ Métricas de Unit Economics

Estrutura Visual (como o usuário navega):
┌──────────────────────────────────────────────────────────────┐
│ 🏠 SAM Financial Model          👤 Usuário    🌙 Dark Mode   │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│ ┌────────────┐ ┌──────────────────────────────────────────┐ │
│ │ NAVEGAÇÃO  │ │  📊 VISÃO GERAL                          │ │
│ ├────────────┤ │                                           │ │
│ │            │ │  🔴 ALERTAS CRÍTICOS                      │ │
│ │ 📊 Overview│ │  • Vale da Morte em 3 meses               │ │
│ │ 💰 Receita │ │  • CAC subiu 25%                          │ │
│ │ 💸 Custos  │ │                                           │ │
│ │ 💰 Caixa   │ │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │ │
│ │ 👥 Equipe  │ │  │ MRR  │ │Users │ │Caixa │ │LTV/  │   │ │
│ │ 📢 Mkt     │ │  │ 45k  │ │ 450  │ │ 38k  │ │CAC   │   │ │
│ │ 🎯 Unit Ec │ │  │+12%↑ │ │+50↑  │ │-5k↓  │ │4.2x↑ │   │ │
│ │ 📊 Sensib. │ │  └──────┘ └──────┘ └──────┘ └──────┘   │ │
│ │ 🔄 Cohorts │ │                                           │ │
│ │ 📋 Tabelas │ │  [Gráfico MRR]      [Gráfico Caixa]     │ │
│ │            │ │  [Gráfico Receita vs Custos]             │ │
│ └────────────┘ └──────────────────────────────────────────┘ │
│                                                               │
│ ┌─ FILTROS GLOBAIS ──────────────────────────────────────┐  │
│ │ Período: [Mês 1] a [Mês 36]  Granular: [Mensal ▼]     │  │
│ │ Cenário: [Base ▼]             [Aplicar Filtros]        │  │
│ └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘

Dashboard Especial: "EXPLORADOR DE DADOS" (Tabela Master)
Este dashboard resolve sua preocupação sobre "tabelas complexas":
┌─ 📋 EXPLORADOR DE DADOS ─────────────────────────────────────┐
│                                                               │
│ [VISUALIZAÇÕES RÁPIDAS - Sidebar]                            │
│ ├─ 📊 DRE Completo                                           │
│ ├─ 💰 Fluxo de Caixa                                         │
│ ├─ 📈 Breakdown de Receita                                   │
│ ├─ 💸 Breakdown de COGS                                      │
│ ├─ 🏗️ Breakdown de OPEX                                     │
│ ├─ 🎯 Métricas de Unit Economics                            │
│ └─ 🔧 Personalizada (criar nova)                            │
│                                                               │
│ [FILTROS AVANÇADOS]                                          │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Período: [1] a [36]  Granular: [Mensal ▼]             │  │
│ │ Colunas: [☑ MRR] [☑ Usuarios] [☑ OPEX] [+ Mais...]    │  │
│ │ Filtro: MRR > [10000]  AND  Usuarios > [100]           │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                               │
│ [TABELA DINÂMICA]                                            │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Mês │ MRR     │ Usuarios │ OPEX    │ Lucro   │ Caixa  │  │
│ ├─────┼─────────┼──────────┼─────────┼─────────┼────────┤  │
│ │ 1   │ R$ 10k  │ 100      │ R$ 8k   │ R$ 2k   │ R$ 5k  │  │
│ │ 2   │ R$ 12k  │ 120      │ R$ 9k   │ R$ 3k   │ R$ 8k  │  │
│ │ ... │ ...     │ ...      │ ...     │ ...     │ ...    │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                               │
│ [AÇÕES]                                                       │
│ [Exportar CSV] [Exportar Excel] [Criar Gráfico] [Salvar]    │
│                                                               │
│ [COMPARAÇÃO DE CENÁRIOS - Opcional]                          │
│ ☑ Base   ☐ Otimista   ☐ Pessimista   [Comparar]             │
└───────────────────────────────────────────────────────────────┘

Resumindo a Estrutura:
✅ 1 Página de Resultados com:

Navegação Lateral (sidebar com tabs)
9-10 Dashboards Temáticos (cada um focado em um aspecto)
1 Dashboard Especial "Explorador de Dados" (tabela master com tudo)

✅ Cada Dashboard Temático tem:

Visualizações (gráficos) - 60% da tela
Tabela Específica - 40% da tela (scrollável)

✅ Filtros Globais aplicam em TODOS os dashboards

2️⃣ Sobre Mock Data - Para que serve?
🎯 Mock Data é ESSENCIAL - Aqui está o porquê:
Problema sem Mock Data:
Desenvolvedor: "Preciso desenvolver o dashboard"
Backend: "Mas a API ainda não está pronta"
Desenvolvedor: "Então não posso começar"
⏱️ RESULTADO: Tempo perdido esperando
Solução com Mock Data:
Desenvolvedor: "Vou usar dados de exemplo"
[Desenvolve toda a UI/UX em 2 semanas]
Backend: "API pronta!"
Desenvolvedor: "Perfeito, só trocar a fonte de dados"
⏱️ RESULTADO: 2 semanas de trabalho produtivo

O que é Mock Data na prática?
É um arquivo JSON que simula a resposta da API:
json// mockProjectionData.json
{
  "projecao_df": {
    "mes": [1, 2, 3, 4, 5, 6, ..., 36],
    "MRR": [10000, 12000, 14400, 17280, ...],
    "Usuarios_Finais": [100, 120, 144, 173, ...],
    "Saldo_Caixa": [5000, 8000, 12000, 15000, ...],
    "OPEX_Total": [8000, 8500, 9000, 9500, ...],
    // ... todas as outras colunas
  },
  "kpis": {
    "Break_Even_Mes": 15,
    "LTV_Final": 2069,
    "CAC_Medio_Periodo": 450,
    "LTV_CAC_Ratio_Final": 4.6,
    "Vale_da_Morte_Mes": 8,
    "Vale_da_Morte_Minimo_Caixa": -12000,
    "Runway_Meses": 24,
    // ... outros KPIs
  },
  "insights": [
    {
      "level": "CRITICAL",
      "category": "caixa",
      "title": "Vale da Morte em 3 meses",
      "description": "Caixa ficará negativo no mês 8",
      "value": -12000,
      "action": "Captar R$20k URGENTE"
    },
    // ... outros insights
  ]
}

Benefícios do Mock Data:
✅ 1. Desenvolvimento Paralelo

Frontend desenvolve enquanto backend finaliza
Equipes trabalham independentemente

✅ 2. Testes de UX

Podemos testar layouts com dados realistas
Validar se visualizações fazem sentido

✅ 3. Demonstrações Antecipadas

Mostrar para stakeholders sem backend pronto
Validar conceito antes de investir muito tempo

✅ 4. Desenvolvimento Mais Rápido

Não precisa rodar backend local
Não precisa reconfigurar cenários toda hora
Dados sempre consistentes para testes

✅ 5. Facilita Implementação
typescript// Sem API real - usa mock
const { data } = useMockProjection();

// Com API real - só trocar o hook
const { data } = useProjection();

// Componentes permanecem IGUAIS! 🎉

Como vamos usar na prática:
typescript// src/lib/api/mockData.ts
export const MOCK_PROJECTION_DATA = {
  // ... dados de exemplo
};

// src/hooks/useMockProjection.ts
export function useMockProjection() {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    // Simula delay de rede
    setTimeout(() => {
      setData(MOCK_PROJECTION_DATA);
      setIsLoading(false);
    }, 1000);
  }, []);
  
  return { data, isLoading };
}

// src/pages/ResultsPage/dashboards/OverviewDashboard.tsx
function OverviewDashboard() {
  // FASE 1: Usa mock
  const { data, isLoading } = useMockProjection();
  
  // FASE 2: Quando API estiver pronta, só trocar para:
  // const { data, isLoading } = useProjection();
  
  // Resto do código permanece IGUAL!
  if (isLoading) return <Loading />;
  return <KPIGrid data={data} />;
}

Quando trocar de Mock para API Real?
Opção 1 (Recomendada): Flag de ambiente
typescript// .env
VITE_USE_MOCK_DATA=true  # Desenvolvimento
VITE_USE_MOCK_DATA=false # Produção

// Hook inteligente
export function useProjectionData() {
  const useMock = import.meta.env.VITE_USE_MOCK_DATA === 'true';
  
  if (useMock) {
    return useMockProjection();
  } else {
    return useRealProjection(); // Chama API
  }
}
Opção 2: Trocar manualmente quando backend estiver pronto

3️⃣ PLANO COMPLETO: Overview + Receita + Custos
🎯 ETAPAS DETALHADAS

SPRINT 1: FUNDAÇÃO (3 dias) 🏗️
Dia 1: Setup Completo
bash# 1. Criar projeto
npm create vite@latest sam-financial-frontend -- --template react-ts

# 2. Instalar dependências
npm install zustand @tanstack/react-query recharts plotly.js-basic-dist
npm install react-hook-form @hookform/resolvers zod
npm install axios date-fns clsx tailwind-merge
npm install lucide-react sonner

# 3. Instalar Shadcn/ui
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card input select tabs dialog

# 4. Configurar Tailwind + Theme
Entregáveis:

 Projeto rodando em localhost:5173
 Tailwind configurado com paleta de cores
 Estrutura de pastas completa
 ESLint + Prettier funcionando


Dia 2-3: Mock Data + Layout Base
2.1 Criar Mock Data
typescript// src/lib/api/mockData.ts
export const MOCK_PROJECTION_DATA = {
  projecao_df: {
    mes: [1,2,3,...,36],
    MRR: [10000, 12000, 14400, ...], // 36 valores
    Usuarios_Finais: [100, 120, 144, ...],
    Saldo_Caixa: [5000, 8000, 12000, ...],
    // ... TODAS as 40+ colunas do backend
  },
  kpis: { /* ... */ },
  insights: [ /* ... */ ]
};
2.2 Criar Tipos TypeScript
typescript// src/types/api.types.ts
export interface ProjectionData {
  mes: number[];
  MRR: number[];
  Usuarios_Finais: number[];
  // ... todos os campos
}

export interface KPIs {
  Break_Even_Mes: number | null;
  LTV_Final: number;
  // ... todos os KPIs
}
2.3 Criar Layout Base
typescript// src/components/layout/AppLayout.tsx
// - Header com logo + user menu
// - Sidebar com navegação
// - Main content area
// - Footer
Entregáveis:

 Mock data completo (baseado em projeção real do backend)
 Tipos TypeScript 100% alinhados com API
 Layout base renderizando
 Navegação entre dashboards funcionando (vazio ainda)


SPRINT 2: DASHBOARD OVERVIEW (4 dias) 🎯
Dia 4: Seção de Alertas + KPIs
4.1 Componentes Base
typescript// src/components/ui/Alert.tsx (Shadcn)
// src/components/insights/AlertCard.tsx (customizado)
// src/components/metrics/MetricCard.tsx
4.2 Seção de Alertas
tsx// src/pages/ResultsPage/dashboards/OverviewDashboard.tsx

<AlertsSection>
  {insights
    .filter(i => i.level === 'CRITICAL')
    .map(insight => (
      <AlertCard
        key={insight.title}
        level={insight.level}
        title={insight.title}
        description={insight.description}
        action={insight.action}
        value={insight.value}
      />
    ))}
</AlertsSection>
4.3 Grid de KPIs
tsx<KPIGrid>
  <MetricCard
    label="MRR Atual"
    value={kpis.MRR_Final}
    delta={calculateDelta(data.MRR)}
    format="currency"
  />
  <MetricCard
    label="Usuários Ativos"
    value={kpis.Usuarios_Final}
    delta={calculateDelta(data.Usuarios_Finais)}
    format="number"
  />
  {/* ... 6-8 métricas principais */}
</KPIGrid>
Entregáveis:

 Alertas renderizando com cores e ícones corretos
 Grid de 8 KPIs principais
 Cálculo de deltas (% de variação)
 Formatação de valores (R$, %, números)


Dia 5-6: Gráficos Principais
5.1 LineChart: MRR ao Longo do Tempo
tsx<LineChart
  title="MRR ao Longo do Tempo"
  data={chartData}
  xKey="mes"
  yKeys={["MRR"]}
  formatValue={(v) => formatCurrency(v)}
/>
5.2 LineChart: Saldo de Caixa com Zonas
tsx<LineChart
  title="Saldo de Caixa"
  data={chartData}
  xKey="mes"
  yKeys={["Saldo_Caixa"]}
  zones={[
    { min: 20000, max: Infinity, color: 'success' },
    { min: 10000, max: 20000, color: 'warning' },
    { min: -Infinity, max: 10000, color: 'danger' },
  ]}
  markers={[
    { mes: kpis.Vale_da_Morte_Mes, label: 'Vale da Morte' }
  ]}
/>
5.3 ComboChart: Receita vs Custos vs Lucro
tsx<ComboChart
  title="Receita, Custos e Lucro"
  data={chartData}
  xKey="mes"
  barKeys={["MRR", "OPEX_Total"]}
  lineKeys={["Lucro_Bruto"]}
/>
5.4 Timeline de Marcos
tsx<InsightsTimeline
  milestones={[
    { mes: kpis.Break_Even_Mes, label: 'Break-even', icon: '🎯' },
    { mes: 12, label: 'Contratar Dev Backend', icon: '👨‍💻' },
    { mes: 18, label: 'Mudar para Tier 2', icon: '🏗️' },
  ]}
/>
Entregáveis:

 3-4 gráficos principais funcionando
 Gráficos responsivos
 Tooltips ricos
 Legends claras
 Timeline de marcos visual


Dia 7: Seção de Insights + Polish
7.1 Insights Positivos
tsx<InsightsSection title="💡 Oportunidades">
  {insights
    .filter(i => i.level === 'SUCCESS')
    .map(insight => (
      <InsightCard
        icon="🚀"
        title={insight.title}
        description={insight.description}
        impact={insight.impact}
      />
    ))}
</InsightsSection>
7.2 Polish

 Animações suaves (Framer Motion)
 Loading skeletons
 Empty states
 Responsividade mobile

Entregável Final: ✅ Dashboard Overview 100% funcional

SPRINT 3: DASHBOARD DE RECEITA (3 dias) 💰
Dia 8: Waterfall + Funil
8.1 Waterfall Chart
tsxconst waterfallData = generateWaterfallData(
  data.MRR[mesAnterior],
  [
    { label: 'Novos Clientes', value: data.Novos_Pagantes[mes] * arpu },
    { label: 'Churn', value: -data.Usuarios_Perdidos[mes] * arpu },
    { label: 'Upsell', value: data.Upsell[mes] || 0 },
  ],
  'MRR Final'
);

<WaterfallChart
  title="Composição do MRR (Mês Atual)"
  data={waterfallData}
/>
8.2 Funil de Conversão
tsx<FunnelChart
  title="Funil de Aquisição"
  stages={[
    { label: 'Visitantes', value: data.Visitantes[mes] },
    { label: 'Trials', value: data.Novos_Trials[mes] },
    { label: 'Pagantes', value: data.Novos_Pagantes[mes] },
  ]}
  showConversionRates
/>
Entregáveis:

 Waterfall mostrando composição do MRR
 Funil visual com taxas de conversão
 Valores formatados corretamente


Dia 9: MRR por Plano + Cohorts
9.1 AreaChart Empilhado
tsx<AreaChart
  title="MRR por Plano"
  data={chartData}
  xKey="mes"
  yKeys={["MRR_Lite", "MRR_Trader", "MRR_Pro"]}
  stacked
  colors={[COLORS.info[300], COLORS.primary[500], COLORS.success[500]]}
/>
9.2 Cohort Heatmap
tsxconst cohortData = generateCohortData(data);

<CohortHeatmap
  title="Retenção por Cohort"
  data={cohortData}
  maxMonths={12}
/>
Entregáveis:

 Gráfico de área empilhado
 Cohort table com cores
 Hover mostrando valores exatos


Dia 10: Tabela Detalhada de Receita
tsx<DataTable
  title="Análise Detalhada de Receita"
  data={tableData}
  columns={[
    { key: 'mes', label: 'Mês', format: 'month' },
    { key: 'MRR', label: 'MRR', format: 'currency' },
    { key: 'Novos_Pagantes', label: 'Novos', format: 'number' },
    { key: 'Usuarios_Perdidos', label: 'Churn', format: 'number' },
    { key: 'Usuarios_Finais', label: 'Total', format: 'number' },
    { key: 'ARPU', label: 'ARPU', format: 'currency' },
    { key: 'Taxa_Conv_Geral', label: 'Conv. %', format: 'percentage' },
  ]}
  filterable
  sortable
  exportable
/>
Entregável Final: ✅ Dashboard de Receita completo

SPRINT 4: DASHBOARD DE CUSTOS (3 dias) 💸
Dia 11: Sankey + Breakdown Pizza
11.1 Sankey Diagram
tsxconst sankeyData = generateSankeyData([
  { from: 'Receita', to: 'COGS', value: data.COGS_Total[mes] },
  { from: 'Receita', to: 'OPEX', value: data.OPEX_Total[mes] },
  { from: 'Receita', to: 'Lucro', value: data.Lucro_Bruto[mes] },
  { from: 'OPEX', to: 'Pessoal', value: data.Custo_Pessoal_CLT[mes] + data.Custo_Pessoal_PJ[mes] },
  { from: 'OPEX', to: 'Infra', value: data.Custo_Infra[mes] },
  { from: 'OPEX', to: 'Marketing', value: data.Custo_Marketing[mes] },
  { from: 'OPEX', to: 'Ferramentas', value: data.Custo_Ferramentas[mes] },
]);

<SankeyChart
  title="Fluxo de Dinheiro"
  data={sankeyData}
/>
11.2 Pizza com Drill-Down (ESSENCIAL)
tsx<PieChartWithDrilldown
  title="Composição de OPEX"
  data={{
    'Pessoal': data.Custo_Pessoal_CLT[mes] + data.Custo_Pessoal_PJ[mes],
    'Infra': data.Custo_Infra[mes],
    'Marketing': data.Custo_Marketing[mes],
    'Ferramentas': data.Custo_Ferramentas[mes],
  }}
  breakdown={{
    'Pessoal': {
      'Dev Backend': 13440,
      'Fundador': 5000,
      'Designer PJ': 3000,
    },
    'Infra': {
      'VPS Principal': 55,
      'VPS MT5': 150,
      'Cedro API': 5000,
    },
    // ... outros breakdowns
  }}
/>
Entregáveis:

 Sankey mostrando fluxo completo
 Pizza com drill-down funcional
 Modal de drill-down com sub-gráfico + tabela


Dia 12: Fixos vs Variáveis + Tabela
12.1 Comparação Fixos vs Variáveis
tsx<BarChart
  title="Custos Fixos vs Variáveis"
  data={chartData}
  xKey="mes"
  yKeys={["Custos_Fixos", "Custos_Variaveis"]}
  stacked
/>
12.2 Tabela Detalhada de Custos
tsx<DataTable
  title="Rastreador de Custos"
  data={tableData}
  columns={[
    { key: 'mes', label:Tentar novamenteWIContinuartsx    { key: 'mes', label: 'Mês', format: 'month' },
    { key: 'OPEX_Total', label: 'OPEX Total', format: 'currency' },
    { key: 'Custo_Pessoal', label: 'Pessoal', format: 'currency', drilldown: true },
    { key: 'Custo_Infra', label: 'Infra', format: 'currency', drilldown: true },
    { key: 'Custo_Marketing', label: 'Marketing', format: 'currency', drilldown: true },
    { key: 'Custo_Ferramentas', label: 'Ferramentas', format: 'currency', drilldown: true },
    { key: 'COGS_Total', label: 'COGS', format: 'currency', drilldown: true },
  ]}
  onCellClick={(row, col) => {
    if (col.drilldown) {
      openDrilldownModal(row, col);
    }
  }}
  filterable
  sortable
  exportable
/>
Entregáveis:

 Gráfico fixos vs variáveis
 Tabela com drill-down em células
 Click em célula abre modal com detalhes


Dia 13: Polish do Dashboard de Custos
13.1 Comparação vs Budget (se houver)
tsx<ComboChart
  title="Real vs Orçado"
  data={chartData}
  xKey="mes"
  barKeys={["OPEX_Real"]}
  lineKeys={["OPEX_Orcado"]}
/>
13.2 Insights de Custos
tsx<InsightsSection title="💡 Análise de Custos">
  <InsightCard
    title="OPEX representa 71% da receita"
    description="Meta: <60% para crescimento sustentável"
    action="Revisar custos fixos ou acelerar crescimento"
    priority="warning"
  />
</InsightsSection>
13.3 Tendências de Custos
tsx<LineChart
  title="Evolução de Categorias de Custo"
  data={chartData}
  xKey="mes"
  yKeys={["Custo_Pessoal", "Custo_Infra", "Custo_Marketing"]}
  showTrendlines
/>
Entregável Final: ✅ Dashboard de Custos completo com drill-down

SPRINT 5: FILTROS GLOBAIS & POLISH FINAL (2 dias) 🎨
Dia 14: Filtros Globais
14.1 Sidebar de Filtros
tsx// src/components/filters/GlobalFilters.tsx
<GlobalFiltersSidebar>
  <FilterSection title="Período">
    <RangeInput
      label="Mês Início"
      value={filters.periodStart}
      onChange={(v) => updateFilter('periodStart', v)}
      min={1}
      max={36}
    />
    <RangeInput
      label="Mês Fim"
      value={filters.periodEnd}
      onChange={(v) => updateFilter('periodEnd', v)}
      min={filters.periodStart}
      max={36}
    />
  </FilterSection>
  
  <FilterSection title="Granularidade">
    <Select
      value={filters.granularity}
      onChange={(v) => updateFilter('granularity', v)}
      options={[
        { value: 'monthly', label: 'Mensal' },
        { value: 'quarterly', label: 'Trimestral' },
        { value: 'yearly', label: 'Anual' },
      ]}
    />
  </FilterSection>
  
  <FilterSection title="Cenários" hint="Disponível na próxima fase">
    <Select
      value={filters.scenario}
      options={[
        { value: 'base', label: 'Base' },
        { value: 'optimistic', label: 'Otimista', disabled: true },
        { value: 'pessimistic', label: 'Pessimista', disabled: true },
      ]}
      disabled
    />
  </FilterSection>
  
  <Button onClick={applyFilters} fullWidth>
    Aplicar Filtros
  </Button>
  
  <Button onClick={resetFilters} variant="ghost" fullWidth>
    Resetar
  </Button>
</GlobalFiltersSidebar>
14.2 Store de Filtros (Zustand)
typescript// src/stores/filtersStore.ts
interface FiltersState {
  periodStart: number;
  periodEnd: number;
  granularity: 'monthly' | 'quarterly' | 'yearly';
  scenario: string;
  
  updateFilter: (key: string, value: any) => void;
  resetFilters: () => void;
  applyFilters: () => void;
}

export const useFiltersStore = create<FiltersState>((set) => ({
  periodStart: 1,
  periodEnd: 36,
  granularity: 'monthly',
  scenario: 'base',
  
  updateFilter: (key, value) => set({ [key]: value }),
  
  resetFilters: () => set({
    periodStart: 1,
    periodEnd: 36,
    granularity: 'monthly',
  }),
  
  applyFilters: () => {
    // Dispara re-render de todos os dashboards
    // que usam useFilteredData()
  },
}));
14.3 Hook de Dados Filtrados
typescript// src/hooks/useFilteredData.ts
export function useFilteredData() {
  const rawData = useProjectionStore(s => s.data);
  const filters = useFiltersStore();
  
  const filteredData = useMemo(() => {
    if (!rawData) return null;
    
    let result = rawData;
    
    // Aplica filtro de período
    result = filterByPeriod(result, filters.periodStart, filters.periodEnd);
    
    // Aplica granularidade
    result = applyGranularity(result, filters.granularity);
    
    return result;
  }, [rawData, filters]);
  
  return filteredData;
}

// Uso em qualquer dashboard:
function OverviewDashboard() {
  const data = useFilteredData(); // Dados já filtrados!
  
  return <LineChart data={data} />;
}
Entregáveis:

 Sidebar de filtros funcional
 Store sincronizado
 Todos os dashboards respondem aos filtros
 Persistência em localStorage (opcional)


Dia 15: Polish & Refinamento Final
15.1 Loading States Elegantes
tsx// src/components/loading/ChartSkeleton.tsx
export function ChartSkeleton() {
  return (
    <Card className="p-6 animate-pulse">
      <div className="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
      <div className="h-64 bg-gray-100 rounded"></div>
    </Card>
  );
}

// Uso:
function OverviewDashboard() {
  const { data, isLoading } = useMockProjection();
  
  if (isLoading) {
    return (
      <div className="grid grid-cols-2 gap-4">
        <ChartSkeleton />
        <ChartSkeleton />
        <ChartSkeleton />
        <ChartSkeleton />
      </div>
    );
  }
  
  return <ActualContent />;
}
15.2 Empty States
tsx// src/components/ui/EmptyState.tsx
export function EmptyState({ 
  icon = "📊", 
  title, 
  description, 
  action 
}) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="text-6xl mb-4">{icon}</div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-gray-500 mb-4 max-w-sm">{description}</p>
      {action && <Button onClick={action.onClick}>{action.label}</Button>}
    </div>
  );
}

// Uso:
if (!data || data.length === 0) {
  return (
    <EmptyState
      icon="📉"
      title="Sem dados disponíveis"
      description="Execute uma projeção para visualizar os resultados"
      action={{
        label: "Ir para Configuração",
        onClick: () => navigate('/config')
      }}
    />
  );
}
15.3 Animações Suaves (Framer Motion)
tsximport { motion } from 'framer-motion';

// Animação de fade-in para dashboards
export function DashboardContainer({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
}

// Animação de stagger para KPI Grid
export function KPIGrid({ kpis }) {
  return (
    <motion.div 
      className="grid grid-cols-4 gap-4"
      initial="hidden"
      animate="visible"
      variants={{
        hidden: { opacity: 0 },
        visible: {
          opacity: 1,
          transition: {
            staggerChildren: 0.1
          }
        }
      }}
    >
      {kpis.map((kpi, i) => (
        <motion.div
          key={i}
          variants={{
            hidden: { opacity: 0, y: 20 },
            visible: { opacity: 1, y: 0 }
          }}
        >
          <MetricCard {...kpi} />
        </motion.div>
      ))}
    </motion.div>
  );
}
15.4 Responsividade Final
tsx// Breakpoints Tailwind:
// sm: 640px
// md: 768px
// lg: 1024px
// xl: 1280px
// 2xl: 1536px

// Grid adaptativo
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  {/* KPIs */}
</div>

// Sidebar colapsável em mobile
<div className="flex">
  <Sidebar className="hidden lg:block" />
  <MobileSidebar className="lg:hidden" />
  <main className="flex-1">
    {/* Content */}
  </main>
</div>

// Gráficos ajustam altura em mobile
<ChartContainer height={{ base: 300, md: 400, lg: 500 }}>
  {/* Chart */}
</ChartContainer>
15.5 Toasts de Feedback
tsximport { toast } from 'sonner';

// Sucesso
toast.success('Filtros aplicados com sucesso!');

// Erro
toast.error('Erro ao carregar dados');

// Loading
toast.loading('Aplicando filtros...', { id: 'filters' });
// ... depois
toast.success('Filtros aplicados!', { id: 'filters' });

// Com ação
toast('Dados exportados!', {
  action: {
    label: 'Abrir',
    onClick: () => window.open('/downloads/export.xlsx')
  }
});
15.6 Error Boundaries
tsx// src/components/ErrorBoundary.tsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };
  
  static getDerivedStateFromError() {
    return { hasError: true };
  }
  
  componentDidCatch(error, info) {
    console.error('Dashboard Error:', error, info);
  }
  
  render() {
    if (this.state.hasError) {
      return (
        <EmptyState
          icon="⚠️"
          title="Algo deu errado"
          description="Ocorreu um erro ao renderizar este dashboard"
          action={{
            label: "Recarregar",
            onClick: () => window.location.reload()
          }}
        />
      );
    }
    
    return this.props.children;
  }
}

// Uso:
<ErrorBoundary>
  <OverviewDashboard />
</ErrorBoundary>
15.7 Acessibilidade Final
tsx// ARIA labels
<button aria-label="Exportar gráfico como PNG">
  <Download />
</button>

// Keyboard navigation
<MetricCard
  tabIndex={0}
  onKeyPress={(e) => {
    if (e.key === 'Enter') handleDrilldown();
  }}
/>

// Focus visible
<Button className="focus:ring-2 focus:ring-primary-500 focus:ring-offset-2">
  Aplicar
</Button>

// Screen reader only text
<span className="sr-only">Carregando gráfico de MRR</span>
```

**Entregável Final:** ✅ **Aplicação polida e profissional**

---

# 📦 RESUMO DOS ENTREGÁVEIS

## **Após 15 dias de desenvolvimento:**
```
✅ PÁGINA DE RESULTADOS COMPLETA
├── 📊 Dashboard: Visão Geral (Overview) ✅ (Completamente Polido)
│   ├── Seção de Alertas Críticos (via AlertHub no Header) ✅
│   ├── Grid de 8 KPIs Principais ✅
│   ├── Gráfico: MRR ao Longo do Tempo (Integrado no Gráfico Financeiro Detalhado) ✅
│   ├── Gráfico: Saldo de Caixa com Zonas (Integrado no Gráfico Financeiro Detalhado) ✅
│   ├── Gráfico: Receita vs Custos vs Lucro (Gráfico Financeiro Detalhado) ✅
│   ├── Timeline de Marcos Importantes (Parte do refinamento visual) ✅
│   └── Seção de Insights (Detalhada no Dashboard) ✅
│
├── 💰 Dashboard: Receita (PRÓXIMO)
│   ├── Waterfall Chart (Composição MRR)
│   ├── Funil de Conversão
│   ├── AreaChart: MRR por Plano
│   ├── Cohort Retention Heatmap
│   └── Tabela Detalhada de Receita
│
├── 💸 Dashboard: Custos
│   ├── Sankey Diagram (Fluxo de Dinheiro)
│   ├── Pizza com Drill-down (OPEX)
│   ├── Gráfico: Fixos vs Variáveis
│   ├── Comparação: Real vs Orçado
│   └── Tabela Detalhada de Custos
│
└── 🎨 Features Globais
    ├── Filtros Globais (Período, Granularidade)
    ├── Loading States (Skeletons)
    ├── Empty States
    ├── Animações (Framer Motion)
    ├── Responsividade Mobile
    ├── Toasts de Feedback
    ├── Error Boundaries
    └── Acessibilidade (ARIA, Keyboard)

🎯 CHECKLIST DE QUALIDADE
Antes de considerar "pronto", verificar:
Funcionalidade

 Todos os gráficos renderizam corretamente
 Drill-down funciona em custos
 Filtros aplicam em todos os dashboards
 Dados formatados corretamente (R$, %, números)
 Navegação entre dashboards suave
 Mock data carrega sem erros

UX/UI

 Layout consistente em todos os dashboards
 Cores seguem paleta definida
 Tipografia hierarquizada
 Espaçamentos consistentes
 Ícones apropriados
 Feedback visual em todas as ações

Performance

 Dashboards carregam em <2s
 Re-renders otimizados (React.memo, useMemo)
 Gráficos responsivos (não travam)
 Navegação instantânea
 Bundle size <500KB gzipped

Responsividade

 Funciona em desktop (1920x1080)
 Funciona em laptop (1366x768)
 Funciona em tablet (768x1024)
 Funciona em mobile (375x667)
 Sidebar colapsável em mobile
 Gráficos ajustam em telas pequenas

Acessibilidade

 Navegação por teclado funciona
 ARIA labels em elementos interativos
 Contraste de cores adequado (WCAG AA)
 Screen readers conseguem ler conteúdo
 Focus visible em elementos

Código

 TypeScript sem erros
 ESLint sem warnings
 Componentes documentados (JSDoc)
 Código formatado (Prettier)
 Sem console.logs em produção
 Tratamento de erros adequado


🚀 PRÓXIMOS PASSOS APÓS CONCLUSÃO
Opção A: Conectar com Backend Real

Trocar useMockProjection() por useRealProjection()
Testar integração com API
Ajustar tipos se necessário
Tratar erros de rede

Opção B: Construir Página de Configuração

Formulário com React Hook Form
Validação com Zod
Submissão para API
Redirecionamento para Resultados

Opção C: Dashboards Adicionais

Dashboard de Caixa & Viabilidade
Dashboard de Equipe
Dashboard de Marketing
Dashboard de Sensibilidade
Dashboard "Explorador de Dados"


📋 TECNOLOGIAS CONFIRMADAS
json{
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.20.0",
    "typescript": "^5.3.0",
    
    "zustand": "^4.5.0",
    "react-hook-form": "^7.49.0",
    "@hookform/resolvers": "^3.3.0",
    "zod": "^3.22.0",
    
    "@tanstack/react-query": "^5.17.0",
    "axios": "^1.6.0",
    
    "recharts": "^2.10.0",
    "plotly.js-basic-dist": "^2.27.0",
    "react-plotly.js": "^2.6.0",
    
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-tabs": "^1.0.4",
    "@radix-ui/react-select": "^2.0.0",
    
    "tailwindcss": "^3.4.0",
    "@tailwindcss/forms": "^0.5.7",
    
    "framer-motion": "^10.18.0",
    "lucide-react": "^0.303.0",
    "sonner": "^1.3.0",
    "date-fns": "^3.0.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0"
  },
  
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "eslint": "^8.56.0",
    "prettier": "^3.1.0",
    "@types/react": "^18.2.0",
    "@types/node": "^20.10.0"
  }
}

✅ APROVAÇÃO NECESSÁRIA
Antes de começar a implementação, confirme:

Estrutura de navegação está OK?

1 Página com múltiplos dashboards em tabs ✅
Sidebar para navegação ✅
Filtros globais no header ✅


Prioridade dos dashboards está OK?

Overview (Dia 4-7) ✅
Receita (Dia 8-10) ✅
Custos (Dia 11-13) ✅


Drill-down é prioridade?

Sim, especialmente em custos ✅


Mock data inicial está OK?

Sim, facilita desenvolvimento ✅


Timeline de 15 dias está OK?

Ou prefere mais/menos tempo?