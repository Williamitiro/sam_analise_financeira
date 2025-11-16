import { useEffect } from 'react';
import { useProjectionStore } from '../stores/projectionStore';
import { MOCK_PROJECTION_DATA } from '@/lib/api/mockData';

/**
 * Hook para carregar mock data
 * Simula chamada de API com delay
 */
export function useMockProjection() {
  const {
    data,
    kpis,
    insights,
    isLoading,
    error,
    setProjectionData,
    setKPIs,
    setInsights,
    setLoading,
    setError,
  } = useProjectionStore();

  useEffect(() => {
    // Se já tem dados, não recarrega
    if (data) return;

    // Simula loading
    setLoading(true);

    // Simula delay de rede (1 segundo)
    const timer = setTimeout(() => {
      try {
        setProjectionData(MOCK_PROJECTION_DATA.projecao_df);
        setKPIs(MOCK_PROJECTION_DATA.kpis);
        setInsights(MOCK_PROJECTION_DATA.insights || []);
        setLoading(false);
      } catch (err) {
        setError('Erro ao carregar dados mock');
        setLoading(false);
      }
    }, 1000);

    return () => clearTimeout(timer);
  }, [data, setProjectionData, setKPIs, setInsights, setLoading, setError]);

  return {
    data,
    kpis,
    insights,
    isLoading,
    error,
  };
}
