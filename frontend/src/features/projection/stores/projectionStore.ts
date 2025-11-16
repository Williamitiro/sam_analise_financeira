import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import type { ProjectionData, KPIs, Insight } from '@/types/api.types';

/**
 * Store de Projeção - Zustand
 * Gerencia dados da projeção, KPIs e insights
 */

interface ProjectionState {
  // Dados
  data: ProjectionData | null;
  kpis: KPIs | null;
  insights: Insight[] | null;
  
  // Filtros globais
  filters: {
    periodStart: number;
    periodEnd: number;
    granularity: 'monthly' | 'quarterly' | 'yearly';
  };
  
  // UI State
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setProjectionData: (data: ProjectionData) => void;
  setKPIs: (kpis: KPIs) => void;
  setInsights: (insights: Insight[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  
  // Filtros
  updateFilters: (filters: Partial<ProjectionState['filters']>) => void;
  resetFilters: () => void;
  
  // Reset
  reset: () => void;
}

const initialState = {
  data: null,
  kpis: null,
  insights: null,
  filters: {
    periodStart: 1,
    periodEnd: 36,
    granularity: 'monthly' as const,
  },
  isLoading: false,
  error: null,
};

export const useProjectionStore = create<ProjectionState>()(
  devtools(
    (set) => ({
      ...initialState,
      
      setProjectionData: (data) => set({ data, error: null }),
      
      setKPIs: (kpis) => set({ kpis }),
      
      setInsights: (insights) => set({ insights }),
      
      setLoading: (isLoading) => set({ isLoading }),
      
      setError: (error) => set({ error, isLoading: false }),
      
      updateFilters: (newFilters) =>
        set((state) => ({
          filters: { ...state.filters, ...newFilters },
        })),
      
      resetFilters: () =>
        set({
          filters: initialState.filters,
        }),
      
      reset: () => set(initialState),
    }),
    { name: 'ProjectionStore' }
  )
);

// Seletores otimizados (evitam re-renders desnecessários)
export const selectProjectionData = (state: ProjectionState) => state.data;
export const selectKPIs = (state: ProjectionState) => state.kpis;
export const selectInsights = (state: ProjectionState) => state.insights;
export const selectFilters = (state: ProjectionState) => state.filters;
export const selectIsLoading = (state: ProjectionState) => state.isLoading;
export const selectError = (state: ProjectionState) => state.error;
