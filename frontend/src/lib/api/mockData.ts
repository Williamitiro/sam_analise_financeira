import type { ProjectionResponse } from '@/types/api.types';

/**
 * Mock Data - Simula resposta da API /projecao/
 * Baseado em projeção real do SAM Financial Model
 */

// Gera array de 36 meses com crescimento exponencial
const generateGrowthArray = (initial: number, growthRate: number, months: number = 36): number[] => {
  return Array.from({ length: months }, (_, i) => 
    Math.round(initial * Math.pow(1 + growthRate, i))
  );
};

// Gera array com valores decrescentes (churn)
const generateDecayArray = (rate: number, months: number = 36): number[] => {
  return Array.from({ length: months }, () => rate);
};

export const MOCK_PROJECTION_DATA: ProjectionResponse = {
  projecao_df: {
    mes: Array.from({ length: 36 }, (_, i) => i + 1),
    
    // Funil de Aquisição
    Usuarios_Iniciais: generateGrowthArray(0, 0.12, 36),
    Visitantes: generateGrowthArray(1000, 0.15, 36),
    Novos_Trials: generateGrowthArray(50, 0.15, 36),
    Novos_Pagantes: generateGrowthArray(8, 0.15, 36),
    Usuarios_Perdidos: generateGrowthArray(0, 0.12, 36).map((v, i) => Math.round(v * 0.04)),
    Usuarios_Finais: generateGrowthArray(8, 0.12, 36),
    
    // Taxas de Conversão (%)
    Taxa_Conv_Trial: Array(36).fill(5.0),
    Taxa_Conv_Pagante: Array(36).fill(15.0),
    Taxa_Conv_Geral: Array(36).fill(0.75),
    
    // Receita
    MRR: generateGrowthArray(776, 0.12, 36),
    ARR: generateGrowthArray(9312, 0.12, 36),
    ARPU: Array(36).fill(97),
    Receita_Total: generateGrowthArray(776, 0.12, 36),
    
    // COGS Detalhado
    Custo_IA: generateGrowthArray(40, 0.12, 36),
    Impostos: generateGrowthArray(47, 0.12, 36),
    Taxas_Pagamento: generateGrowthArray(35, 0.12, 36),
    Comissoes_Afiliados: Array(36).fill(0),
    COGS_Total: generateGrowthArray(122, 0.12, 36),
    
    // Margens
    Lucro_Bruto: generateGrowthArray(654, 0.12, 36),
    Margem_Bruta_Pct: Array(36).fill(84.3),
    
    // OPEX Detalhado
    Custo_Infra: [
      ...Array(6).fill(209),    // Tier 1 meses 1-6
      ...Array(6).fill(209),    // Tier 1 meses 7-12
      ...Array(12).fill(5559),  // Tier 2 meses 13-24
      ...Array(12).fill(5859),  // Tier 2+ meses 25-36
    ],
    Tier_Infra: [
      ...Array(12).fill(1),     // Tier 1
      ...Array(12).fill(2),     // Tier 2
      ...Array(12).fill(2),     // Tier 2
    ],
    Custo_Marketing: [
      ...Array(3).fill(500),    // Fase 1: validação
      ...Array(9).fill(150),    // Fase 2: % lucro
      ...Array(12).fill(400),   // Fase 2: crescendo
      ...Array(12).fill(800),   // Fase 2: escala
    ],
    Fase_Marketing: [
      ...Array(3).fill(1),
      ...Array(33).fill(2),
    ],
    Salario_Fundador: [
      ...Array(6).fill(0),      // Sem salário
      ...Array(6).fill(3000),   // Salário mínimo
      ...Array(24).fill(5000),  // Salário pleno
    ],
    Custo_Pessoal_CLT: [
      ...Array(12).fill(0),     // Sem contratações
      ...Array(12).fill(13440), // Dev Backend
      ...Array(12).fill(22240), // Dev + CS Manager
    ],
    Custo_Pessoal_PJ: [
      ...Array(6).fill(0),
      ...Array(30).fill(3000),  // Designer
    ],
    Custo_Escritorio: Array(36).fill(0), // Remoto
    Custo_Ferramentas: Array(36).fill(400),
    Custo_Servicos_Profissionais: Array(36).fill(500),
    Custo_Depreciacao: Array(36).fill(333),
    Custo_Despesas_Anuais: Array(36).fill(3.33),
    OPEX_Total: [
      ...Array(6).fill(1442),
      ...Array(6).fill(4442),
      ...Array(12).fill(19876),
      ...Array(12).fill(29876),
    ],
    
    // Resultado
    EBITDA: generateGrowthArray(-788, 0.15, 36).map((v, i) => 
      i < 6 ? -788 : i < 12 ? -1500 : i < 24 ? 200 : 1500
    ),
    Resultado_Operacional: generateGrowthArray(-1121, 0.15, 36).map((v, i) => 
      i < 6 ? -1121 : i < 12 ? -1833 : i < 24 ? -133 : 1167
    ),
    
    // Fluxo de Caixa
    Aportes: [
      ...Array(12).fill(1800),  // Aportes primeiros 12 meses
      ...Array(24).fill(0),
    ],
    Fluxo_Caixa: generateGrowthArray(679, 0.10, 36).map((v, i) => 
      i < 12 ? 679 - (i * 50) : v
    ),
    Saldo_Caixa: [
      -8000, -7321, -6642, -5963, -5284, -4605, // Vale da morte
      -3926, -3247, -2568, -1889, -1210, -531,
      148, 827, 1506, 2185, 2864, 3543,         // Recuperação
      4222, 4901, 5580, 6259, 6938, 7617,
      8296, 8975, 9654, 10333, 11012, 11691,
      12370, 13049, 13728, 14407, 15086, 15765,
    ],
    
    // Métricas de Análise
    CAC_Mensal: generateGrowthArray(62.5, 0.02, 36),
    LTV: Array(36).fill(2425),
    LTV_CAC_Ratio: Array(36).fill(4.6),
    Payback_Meses: Array(36).fill(5.8),
    Churn_Absoluto: generateGrowthArray(0, 0.12, 36).map((v, i) => Math.round(v * 0.04)),
  },
  
  kpis: {
    Break_Even_Mes: 13,
    Payback_Investimento_Mes: 13,
    Vale_da_Morte_Minimo_Caixa: -8000,
    Vale_da_Morte_Mes: 1,
    Runway_Meses: '>= 36',
    LTV_Final: 2425,
    CAC_Medio_Periodo: 450,
    LTV_CAC_Ratio_Final: 5.4,
    CAC_Payback_Meses_Config: 5.8,
    MRR_Ano1: 7760,
    MRR_Ano2: 24320,
    MRR_Ano3: 76160,
    Usuarios_Ano1: 80,
    Usuarios_Ano2: 251,
    Usuarios_Ano3: 785,
    Saldo_Caixa_Final: 15765,
    MRR_Final: 76160,
    Usuarios_Final: 785,
    eventos: [
      { mes: 1, tipo: 'INICIO', descricao: 'Início da operação', valor: -8000 },
      { mes: 6, tipo: 'CONTRATACAO', descricao: 'Designer PJ contratado', valor: 3000 },
      { mes: 7, tipo: 'SALARIO', descricao: 'Fundador começa salário mínimo', valor: 3000 },
      { mes: 12, tipo: 'TRANSICAO', descricao: 'Fim dos aportes mensais', valor: 0 },
      { mes: 13, tipo: 'MILESTONE', descricao: 'Break-even atingido', valor: 148 },
      { mes: 13, tipo: 'CONTRATACAO', descricao: 'Dev Backend contratado', valor: 13440 },
      { mes: 13, tipo: 'INFRA', descricao: 'Migração para Tier 2', valor: 5559 },
      { mes: 18, tipo: 'CONTRATACAO', descricao: 'Community Manager contratado', valor: 8800 },
      { mes: 24, tipo: 'MILESTONE', descricao: 'MRR passa de R$50k', valor: 50000 },
    ],
  },
  
  insights: [
    {
      level: 'CRITICAL',
      category: 'caixa',
      title: 'Caixa inicial negativo',
      description: 'Investimento inicial de R$8.000 (CAPEX). Runway de 12 meses com aportes.',
      value: -8000,
      action: 'Monitorar fluxo de caixa mensalmente',
      impact: 'Break-even previsto para mês 13',
    },
    {
      level: 'SUCCESS',
      category: 'crescimento',
      title: 'Crescimento consistente',
      description: 'MRR crescendo 12% ao mês em média',
      value: 0.12,
      action: 'Manter estratégia de marketing atual',
      impact: 'Atingirá R$50k MRR no mês 24',
    },
    {
      level: 'SUCCESS',
      category: 'unit_economics',
      title: 'Unit Economics saudável',
      description: 'LTV/CAC de 5.4x (acima do mínimo de 3x)',
      value: 5.4,
      action: 'Considerar aumentar investimento em marketing',
      impact: 'Margem para acelerar crescimento',
    },
    {
      level: 'WARNING',
      category: 'custos',
      title: 'OPEX sobe significativamente no mês 13',
      description: 'Contratação de Dev Backend + migração para Tier 2',
      value: 19876,
      action: 'Garantir que MRR suporte o aumento de custos',
      impact: 'OPEX passa de R$4k para R$20k',
    },
    {
      level: 'INFO',
      category: 'caixa',
      title: 'Runway estendido',
      description: 'Com aportes mensais, runway > 36 meses',
      action: 'Planejamento de captação pode ser postergado',
      impact: 'Maior flexibilidade operacional',
    },
  ],
};
