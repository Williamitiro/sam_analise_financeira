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

// Gera array com valores constantes
const generateConstantArray = (value: number, months: number = 36): number[] => {
  return Array.from({ length: months }, () => value);
};

const projecao_df_base = {
    mes: Array.from({ length: 36 }, (_, i) => i + 1),
    Usuarios_Iniciais: generateGrowthArray(0, 0.12, 36),
    Visitantes: generateGrowthArray(1000, 0.15, 36),
    Novos_Trials: generateGrowthArray(50, 0.15, 36),
    Novos_Pagantes: generateGrowthArray(8, 0.15, 36),
    Usuarios_Perdidos: generateGrowthArray(0, 0.12, 36).map((v) => Math.round(v * 0.04)),
    Usuarios_Finais: generateGrowthArray(8, 0.12, 36),
    Taxa_Conv_Trial: generateConstantArray(5.0),
    Taxa_Conv_Pagante: generateConstantArray(15.0),
    Taxa_Conv_Geral: generateConstantArray(0.75),
    MRR: generateGrowthArray(776, 0.12, 36),
    MRR_Novos_Clientes: generateGrowthArray(776, 0.12, 36).map(v => v * 0.1), // Placeholder
    MRR_Churn: generateGrowthArray(776, 0.12, 36).map(v => v * 0.04), // Placeholder
    MRR_Expansao: generateGrowthArray(776, 0.12, 36).map(v => v * 0.02), // Placeholder
    MRR_Contracao: generateGrowthArray(776, 0.12, 36).map(v => v * 0.01), // Placeholder
    MRR_Lite: generateGrowthArray(776, 0.12, 36).map(v => v * 0.2),
    MRR_Trader: generateGrowthArray(776, 0.12, 36).map(v => v * 0.5),
    MRR_Pro: generateGrowthArray(776, 0.12, 36).map(v => v * 0.3),
    ARR: generateGrowthArray(9312, 0.12, 36),
    ARPU: generateConstantArray(97),
    Receita_Total: generateGrowthArray(776, 0.12, 36),
    Custo_IA: generateGrowthArray(40, 0.12, 36),
    Impostos: generateGrowthArray(47, 0.12, 36),
    Taxas_Pagamento: generateGrowthArray(35, 0.12, 36),
    Comissoes_Afiliados: generateConstantArray(0),
    COGS_Total: generateGrowthArray(122, 0.12, 36),
    Lucro_Bruto: generateGrowthArray(654, 0.12, 36),
    Margem_Bruta_Pct: generateConstantArray(84.3),
    Custo_Infra: [...generateConstantArray(209, 12), ...generateConstantArray(5559, 12), ...generateConstantArray(5859, 12)],
    Tier_Infra: [...generateConstantArray(1, 12), ...generateConstantArray(2, 24)],
    Custo_Marketing: [...generateConstantArray(500, 3), ...generateConstantArray(150, 9), ...generateConstantArray(400, 12), ...generateConstantArray(800, 12)],
    Fase_Marketing: [...generateConstantArray(1, 3), ...generateConstantArray(2, 33)],
    Salario_Fundador: [...generateConstantArray(0, 6), ...generateConstantArray(3000, 6), ...generateConstantArray(5000, 24)],
    Custo_Pessoal_CLT: [...generateConstantArray(0, 12), ...generateConstantArray(13440, 12), ...generateConstantArray(22240, 12)],
    Custo_Pessoal_PJ: [...generateConstantArray(0, 6), ...generateConstantArray(3000, 30)],
    Custo_Escritorio: generateConstantArray(0),
    Custo_Ferramentas: generateConstantArray(400),
    Custo_Servicos_Profissionais: generateConstantArray(500),
    Custo_Depreciacao: generateConstantArray(333),
    Custo_Despesas_Anuais: generateConstantArray(3.33),
    OPEX_Total: [...generateConstantArray(1442, 6), ...generateConstantArray(4442, 6), ...generateConstantArray(19876, 12), ...generateConstantArray(29876, 12)],
    Lucro_Prejuizo_Acumulado: generateGrowthArray(-1121, 0.15, 36).map((v, i) => i < 6 ? -1121* (i+1) : v), // Placeholder
    EBITDA: generateGrowthArray(-788, 0.15, 36).map((v, i) => i < 6 ? -788 : i < 12 ? -1500 : i < 24 ? 200 : 1500),
    Resultado_Operacional: generateGrowthArray(-1121, 0.15, 36).map((v, i) => i < 6 ? -1121 : i < 12 ? -1833 : i < 24 ? -133 : 1167),
    Aportes: [...generateConstantArray(1800, 12), ...generateConstantArray(0, 24)],
    Fluxo_Caixa: generateGrowthArray(679, 0.10, 36).map((v, i) => i < 12 ? 679 - (i * 50) : v),
    Saldo_Caixa: [-8000, -7321, -6642, -5963, -5284, -4605, -3926, -3247, -2568, -1889, -1210, -531, 148, 827, 1506, 2185, 2864, 3543, 4222, 4901, 5580, 6259, 6938, 7617, 8296, 8975, 9654, 10333, 11012, 11691, 12370, 13049, 13728, 14407, 15086, 15765],
    CAC: generateGrowthArray(62.5, 0.02, 36),
    LTV: generateConstantArray(2425),
    LTV_CAC_Ratio: generateConstantArray(4.6),
    Taxa_Churn: generateConstantArray(0.04),
    Payback_Meses: generateConstantArray(5.8),
    Churn_Absoluto: generateGrowthArray(0, 0.12, 36).map((v) => Math.round(v * 0.04)),
};

const Custos_Fixos = Array.from({ length: 36 }, (_, i) => 
    (projecao_df_base.Custo_Pessoal_CLT[i] || 0) + 
    (projecao_df_base.Custo_Pessoal_PJ[i] || 0) + 
    (projecao_df_base.Salario_Fundador[i] || 0) +
    (projecao_df_base.Custo_Infra[i] || 0) +
    (projecao_df_base.Custo_Ferramentas[i] || 0) +
    (projecao_df_base.Custo_Servicos_Profissionais[i] || 0)
);

const Custos_Variaveis = Array.from({ length: 36 }, (_, i) =>
    (projecao_df_base.COGS_Total[i] || 0) +
    (projecao_df_base.Custo_Marketing[i] || 0)
);

export const MOCK_PROJECTION_DATA: ProjectionResponse = {
  projecao_df: {
    ...projecao_df_base,
    Custos_Fixos,
    Custos_Variaveis,
  },
  kpis: {
    Breakeven_Month: 13,
    Payback_Investimento_Mes: 13,
    Vale_da_Morte_Valor: -8000,
    Vale_da_Morte_Month: 1,
    Runway_Meses: 36,
    LTV_Final: 2425,
    CAC_Medio_Periodo: 450,
    LTV_CAC_Ratio_Final: 5.4,
    Taxa_Churn_Media: 0.04,
    Lucro_Prejuizo_Mes_12: -531,
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
    Breakeven_MRR: 8700, // Placeholder
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
      level: 'OPPORTUNITY',
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
  ],
};
