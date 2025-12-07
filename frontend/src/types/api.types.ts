// frontend/src/types/api.types.ts

// Based on Pydantic models from main.py

export type CategoriaFerramenta =
  | "Marketing"
  | "Vendas"
  | "Produtividade"
  | "Finanças"
  | "Dados & BI"
  | "Outra";

export interface FerramentaSaaSModel {
  nome: string;
  categoria: CategoriaFerramenta;
  custo_mensal: number;
  provider?: string;
  descricao?: string;
  essencial?: boolean;
  custo_por_usuario?: number;
  mes_inicio?: number;
  mes_fim?: number | null;
  ativa?: boolean;
}

export interface FuncionarioModel {
  nome: string;
  cargo: string;
  salario_bruto: number;
  mes_inicio: number;
  tipo?: string;
  encargos_percentual?: number;
  ativo?: boolean;
  mes_fim?: number | null;
}

export interface AtivoDepreciavelModel {
  nome: string;
  valor_aquisicao: number;
  meses_depreciacao: number;
  mes_aquisicao?: number;
  ativo?: boolean;
  mes_fim?: number | null;
}

export interface DespesaAnualModel {
  nome: string;
  valor_anual: number;
  mes_pagamento?: number;
  ativo?: boolean;
  mes_inicio?: number;
  mes_fim?: number | null;
}

export interface ComissaoAfiliadoModel {
  percentual_sobre_venda: number;
  mes_inicio_programa?: number;
  percentual_vendas_via_afiliados?: number;
}

export interface ProjecaoRequest {
  ativar_receita_por_usuario?: boolean;
  ativar_custo_ia?: boolean;
  ativar_impostos?: boolean;
  ativar_taxas_pgto?: boolean;
  ativar_fundador?: boolean;
  ativar_equipe_clt?: boolean;
  ativar_equipe_pj?: boolean;
  ativar_escritorio?: boolean;
  ativar_ferramentas?: boolean;
  ativar_servicos_profs?: boolean;
  ativar_marketing?: boolean;
  ativar_depreciacao?: boolean;
  ativar_despesas_anuais?: boolean;
  ativar_comissoes_afiliado?: boolean;
  ativar_infra_tier1?: boolean;
  ativar_infra_tier2?: boolean;
  ativar_infra_tier3?: boolean;
  capital_inicial_caixa?: number;
  aporte_mensal_fixo?: number;
  meses_aporte_fixo?: number;
  visitantes_mes_1?: number;
  taxa_crescimento_trafego_mensal?: number;
  taxa_conversao_visitante_trial?: number;
  taxa_conversao_trial_pagante?: number;
  churn_mensal?: number;
  preco_plano_lite?: number;
  preco_plano_trader?: number;
  preco_plano_pro?: number;
  mix_plano_lite?: number;
  mix_plano_trader?: number;
  mix_plano_pro?: number;
  arpu_medio_override?: number | null;
  custo_ia_por_usuario?: number;
  aliquota_impostos?: number;
  taxa_pagamento_percentual?: number;
  taxa_pagamento_fixa_por_transacao?: number;
  comissao_afiliados?: ComissaoAfiliadoModel | null;
  infra_tier1_custo_fixo?: number;
  infra_tier1_limite?: number;
  infra_tier1_detalhes?: Record<string, number>;
  infra_tier2_custo_fixo?: number;
  infra_tier2_limite?: number;
  infra_tier2_detalhes?: Record<string, number>;
  infra_tier3_custo_por_usuario?: number;
  cloud_custo_excedente_por_gb?: number;
  cloud_gb_inclusos_tier?: number;
  cloud_gb_estimado_por_usuario?: number;
  marketing_fase1_custo_fixo?: number;
  marketing_fase1_duracao_meses?: number;
  marketing_fase2_perc_lucro_bruto?: number;
  cac_pago_meta?: number;
  salario_fundador_valor?: number;
  salario_fundador_mes_inicio_ideal?: number;
  salario_fundador_caixa_minimo_seguranca?: number;
  equipe?: FuncionarioModel[];
  escritorio_aluguel_mensal?: number;
  escritorio_condominio_mensal?: number;
  escritorio_agua_luz_mensal?: number;
  escritorio_internet_mensal?: number;
  escritorio_outros_mensal?: number;
  escritorio_mes_inicio?: number;
  ferramentas_saas?: FerramentaSaaSModel[];
  contabilidade_mensal?: number;
  contabilidade_mes_inicio?: number;
  advogado_retainer_mensal?: number;
  advogado_mes_inicio?: number;
  consultorias_outras_mensal?: number;
  ativos_depreciaveis?: AtivoDepreciavelModel[];
  despesas_anuais?: DespesaAnualModel[];
}

export interface KPIs {
  [key: string]: any;
}

export interface Insight {
    id: string;
    priority: 'high' | 'medium' | 'low';
    title: string;
    description: string;
    details: string;
    category: 'performance' | 'risk' | 'opportunity' | 'efficiency';
    related_metrics: string[];
    action_item?: string;
    confidence_level: number;
}


export interface ProjectionData {
  [key: string]: any[];
}


export interface ProjectionResponse {
  kpis: KPIs;
  insights: Insight[];
  projecao_mensal: ProjectionData[];
  analise_cohorts: any; // Define this more accurately if needed
}