// frontend/src/stores/projectionStore.ts
import { create } from 'zustand';
import { ProjectionResponse, KPIs, Insight, ProjectionData } from '@/types/api.types';

interface ProjectionState {
  // Data
  data: ProjectionData | null;
  kpis: KPIs | null;
  insights: Insight[] | null;
  
  // State
  isLoading: boolean;
  error: string | null;
  
  // Actions
  runProjection: (config: any) => Promise<void>; // config should be ProjecaoRequest
  clearProjection: () => void;
}

export const useProjectionStore = create<ProjectionState>((set) => ({
  // Initial Data
  data: null,
  kpis: null,
  insights: null,
  
  // Initial State
  isLoading: false,
  error: null,

  // Actions
  runProjection: async (config) => {
    console.log("runProjection called with config:", config);
    set({ isLoading: true, error: null });

    const transformKpis = (rawKpis: Record<string, any>): KPIs => {
      const kpiMapping: Record<string, { newKey: string; label: string; format: 'currency' | 'number' | 'string' | 'months' }> = {
        MRR_Final: { newKey: 'mrr', label: 'MRR Final', format: 'currency' },
        LTV_Final: { newKey: 'ltv', label: 'LTV', format: 'currency' },
        CAC_Medio_Periodo: { newKey: 'cac', label: 'CAC Médio', format: 'currency' },
        LTV_CAC_Ratio_Final: { newKey: 'ltv_cac_ratio', label: 'LTV/CAC', format: 'number' },
        Break_Even_Mes: { newKey: 'break_even', label: 'Break Even (Mês)', format: 'months' },
        Payback_Investimento_Mes: { newKey: 'payback', label: 'Payback (Mês)', format: 'months' },
        Runway_Meses: { newKey: 'runway', label: 'Runway', format: 'string' },
        Saldo_Caixa_Final: { newKey: 'saldo_caixa', label: 'Caixa Final', format: 'currency' },
        Usuarios_Final: { newKey: 'usuarios', label: 'Usuários Ativos', format: 'number' },
      };

      const transformed: KPIs = {};
      for (const rawKey in rawKpis) {
        if (kpiMapping[rawKey]) {
          const { newKey, label, format } = kpiMapping[rawKey];
          transformed[newKey] = {
            value: rawKpis[rawKey],
            label,
            format,
          };
        } else {
             transformed[rawKey] = {
                value: rawKpis[rawKey],
                label: rawKey.replace(/_/g, ' '),
                format: typeof rawKpis[rawKey] === 'number' ? 'number' : 'string'
             }
        }
      }
      return transformed;
    };

    const transformInsights = (rawInsights: { alertas?: any[], oportunidades?: any[], recomendacoes?: any[] }): Insight[] => {
        const alertas = rawInsights.alertas || [];
        const oportunidades = rawInsights.oportunidades || [];
        const recomendacoes = rawInsights.recomendacoes || [];
        return [...alertas, ...oportunidades, ...recomendacoes];
    };

    try {
      const api = await import('@/lib/api/projection');
      const response: ProjectionResponse = await api.runProjection(config);
      console.log("API response received:", response);
      
      const transformedKpis = transformKpis(response.kpis);
      const transformedInsights = transformInsights(response.insights);

      console.log("Transformed KPIs:", transformedKpis);
      console.log("Transformed Insights:", transformedInsights);

      set({
        data: response.projecao_mensal,
        kpis: transformedKpis,
        insights: transformedInsights,
        isLoading: false,
      });
    } catch (err: any) {
      console.error("Error in runProjection:", err);
      set({ error: err.message || 'An unknown error occurred.', isLoading: false });
      throw err;
    }
  },
  
  clearProjection: () => set({ data: null, kpis: null, insights: null, error: null }),
}));
