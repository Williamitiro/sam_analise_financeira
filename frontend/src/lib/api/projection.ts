// frontend/src/lib/api/projection.ts
import { ProjecaoRequest, ProjectionResponse } from "@/types/api.types";

// This is a default configuration that matches the backend's Pydantic model defaults.
// In the future, this will be built from the configuration page.
export const defaultConfig: ProjecaoRequest = {
  ativar_receita_por_usuario: true,
  ativar_custo_ia: true,
  ativar_impostos: true,
  ativar_taxas_pgto: true,
  ativar_fundador: true,
  ativar_equipe_clt: true,
  ativar_equipe_pj: true,
  ativar_escritorio: false,
  ativar_ferramentas: true,
  ativar_servicos_profs: true,
  ativar_marketing: true,
  ativar_depreciacao: true,
  ativar_despesas_anuais: true,
  ativar_comissoes_afiliado: false,
  ativar_infra_tier1: true,
  ativar_infra_tier2: true,
  ativar_infra_tier3: true,
  capital_inicial_caixa: 10000.0,
  aporte_mensal_fixo: 1800.0,
  meses_aporte_fixo: 12,
  visitantes_mes_1: 1000,
  taxa_crescimento_trafego_mensal: 0.2,
  taxa_conversao_visitante_trial: 0.05,
  taxa_conversao_trial_pagante: 0.15,
  churn_mensal: 0.04,
  preco_plano_lite: 69.9,
  preco_plano_trader: 99.0,
  preco_plano_pro: 159.0,
  mix_plano_lite: 0.5,
  mix_plano_trader: 0.3,
  mix_plano_pro: 0.2,
  arpu_medio_override: null,
  custo_ia_por_usuario: 5.0,
  aliquota_impostos: 0.06,
  taxa_pagamento_percentual: 0.0349,
  taxa_pagamento_fixa_por_transacao: 0.39,
  comissao_afiliados: null,
  infra_tier1_custo_fixo: 209.0,
  infra_tier1_limite: 100,
  infra_tier1_detalhes: {
    vps_principal: 55.0,
    vps_coleta_mt5: 150.0,
    dominio: 4.0,
  },
  infra_tier2_custo_fixo: 5559.0,
  infra_tier2_limite: 500,
  infra_tier2_detalhes: {
    api_cedro: 5000.0,
    vps_robusta: 500.0,
    ferramentas_infra: 59.0,
  },
  infra_tier3_custo_por_usuario: 1.5,
  cloud_custo_excedente_por_gb: 0.1,
  cloud_gb_inclusos_tier: 1000,
  cloud_gb_estimado_por_usuario: 0.5,
  marketing_fase1_custo_fixo: 500.0,
  marketing_fase1_duracao_meses: 3,
  marketing_fase2_perc_lucro_bruto: 0.25,
  cac_pago_meta: 500.0,
  salario_fundador_valor: 5000.0,
  salario_fundador_mes_inicio_ideal: 6,
  salario_fundador_caixa_minimo_seguranca: 10000.0,
  equipe: [],
  escritorio_aluguel_mensal: 0.0,
  escritorio_condominio_mensal: 0.0,
  escritorio_agua_luz_mensal: 0.0,
  escritorio_internet_mensal: 0.0,
  escritorio_outros_mensal: 0.0,
  escritorio_mes_inicio: 999,
  ferramentas_saas: [],
  contabilidade_mensal: 0.0,
  contabilidade_mes_inicio: 1,
  advogado_retainer_mensal: 0.0,
  advogado_mes_inicio: 999,
  consultorias_outras_mensal: 0.0,
  ativos_depreciaveis: [],
  despesas_anuais: [],
};

export const runProjection = async (config: ProjecaoRequest): Promise<ProjectionResponse> => {
  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
  
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 seconds timeout

  try {
    const response = await fetch(`${API_URL}/projecao/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(config),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorBody = await response.text();
      console.error('API Error Response:', errorBody);
      throw new Error(`API returned status ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === 'AbortError') {
      console.error('Fetch aborted due to timeout');
      throw new Error('A requisição demorou muito para responder (timeout).');
    }
    console.error('Failed to run projection:', error);
    throw error;
  }
};
