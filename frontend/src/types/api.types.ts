/**
 * Tipos da API - Alinhados com o backend FastAPI
 */

// Dados da projeção mês a mês
export interface ProjectionData {
  mes: number[];
  
  // Funil de Aquisição
  Usuarios_Iniciais: number[];
  Visitantes: number[];
  Novos_Trials: number[];
  Novos_Pagantes: number[];
  Usuarios_Perdidos: number[];
  Usuarios_Finais: number[];
  
  // Taxas de Conversão
  Taxa_Conv_Trial: number[];
  Taxa_Conv_Pagante: number[];
  Taxa_Conv_Geral: number[];
  
  // Receita
  MRR: number[];
  ARR: number[];
  ARPU: number[];
  Receita_Total: number[];
  
  // COGS Detalhado
  Custo_IA: number[];
  Impostos: number[];
  Taxas_Pagamento: number[];
  Comissoes_Afiliados: number[];
  COGS_Total: number[];
  
  // Margens
  Lucro_Bruto: number[];
  Margem_Bruta_Pct: number[];
  
  // OPEX Detalhado
  Custo_Infra: number[];
  Tier_Infra: number[];
  Custo_Marketing: number[];
  Fase_Marketing: number[];
  Salario_Fundador: number[];
  Custo_Pessoal_CLT: number[];
  Custo_Pessoal_PJ: number[];
  Custo_Escritorio: number[];
  Custo_Ferramentas: number[];
  Custo_Servicos_Profissionais: number[];
  Custo_Depreciacao: number[];
  Custo_Despesas_Anuais: number[];
  OPEX_Total: number[];
  
  // Resultado
  EBITDA: number[];
  Resultado_Operacional: number[];
  
  // Fluxo de Caixa
  Aportes: number[];
  Fluxo_Caixa: number[];
  Saldo_Caixa: number[];
  
  // Métricas de Análise
  CAC_Mensal: number[];
  LTV: number[];
  LTV_CAC_Ratio: number[];
  Payback_Meses: number[];
  Churn_Absoluto: number[];
}

// KPIs principais
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

// Insight automático
export interface Insight {
  level: 'CRITICAL' | 'WARNING' | 'INFO' | 'SUCCESS';
  category: 'caixa' | 'crescimento' | 'custos' | 'unit_economics';
  title: string;
  description: string;
  value?: number;
  action?: string;
  impact?: string;
}

// Evento no timeline
export interface Event {
  mes: number;
  tipo: string;
  descricao: string;
  valor: number;
}

// Response completa da API
export interface ProjectionResponse {
  projecao_df: ProjectionData;
  kpis: KPIs;
  insights?: Insight[];
  eventos?: Event[];
}

// Tipos auxiliares para charts
export interface ChartDataPoint {
  mes: number;
  [key: string]: number | string;
}

// Tipo para waterfall
export interface WaterfallItem {
  label: string;
  value: number;
  type: 'increase' | 'decrease' | 'total';
}

// Tipo para Sankey
export interface SankeyNode {
  label: string;
  color?: string;
}

export interface SankeyLink {
  source: number;
  target: number;
  value: number;
  color?: string;
}

export interface SankeyData {
  nodes: SankeyNode[];
  links: SankeyLink[];
}

// Tipo para cohorts
export interface CohortData {
  cohort: string;
  retention: Record<string, number>;
}
