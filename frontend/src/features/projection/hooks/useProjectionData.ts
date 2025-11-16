import { useMemo } from 'react';
import { useProjectionStore, selectProjectionData, selectFilters } from '../stores/projectionStore';
import type { ProjectionData } from '@/types/api.types';

/**
 * Hook para obter dados filtrados
 * Aplica filtros de período e granularidade
 */
export function useFilteredData() {
  const data = useProjectionStore(selectProjectionData);
  const filters = useProjectionStore(selectFilters);

  const filteredData = useMemo(() => {
    if (!data) return null;

    // Aplica filtro de período
    const startIndex = filters.periodStart - 1;
    const endIndex = filters.periodEnd;

    const filtered: ProjectionData = {} as ProjectionData;

    // Filtra cada array
    Object.keys(data).forEach((key) => {
      const dataKey = key as keyof ProjectionData;
      if (Array.isArray(data[dataKey])) {
        filtered[dataKey] = data[dataKey].slice(startIndex, endIndex) as any;
      }
    });

    // Aplica granularidade (se necessário)
    if (filters.granularity !== 'monthly') {
      return applyGranularity(filtered, filters.granularity);
    }

    return filtered;
  }, [data, filters]);

  return filteredData;
}

/**
 * Aplica granularidade (trimestral ou anual)
 */
function applyGranularity(
  data: ProjectionData,
  granularity: 'quarterly' | 'yearly'
): ProjectionData {
  const groupSize = granularity === 'quarterly' ? 3 : 12;
  const aggregated: ProjectionData = {} as ProjectionData;

  Object.keys(data).forEach((key) => {
    const dataKey = key as keyof ProjectionData;
    const values = data[dataKey];
    
    if (!Array.isArray(values)) {
      aggregated[dataKey] = values;
      return;
    }

    const aggregatedValues: (number | string)[] = [];

    for (let i = 0; i < values.length; i += groupSize) {
      const chunk = values.slice(i, i + groupSize) as number[];

      // Para 'mes', 'Tier_Infra', 'Fase_Marketing', pega o primeiro valor do grupo
      if (key === 'mes' || key === 'Tier_Infra' || key === 'Fase_Marketing') {
        aggregatedValues.push(chunk[0]);
      }
      // Para percentuais e médias, calcula média
      else if (
        key.includes('Taxa_') ||
        key.includes('Margem_') ||
        key.includes('Pct') ||
        key === 'ARPU' ||
        key === 'LTV_CAC_Ratio' ||
        key === 'Payback_Meses'
      ) {
        const avg = chunk.reduce((sum, val) => sum + val, 0) / chunk.length;
        aggregatedValues.push(avg);
      }
      // Para LTV e Saldo_Caixa, pega o último valor do período
      else if (key === 'LTV' || key === 'Saldo_Caixa') {
        aggregatedValues.push(chunk[chunk.length - 1]);
      }
      // Para valores absolutos, soma
      else {
        const sum = chunk.reduce((sum, val) => sum + val, 0);
        aggregatedValues.push(sum);
      }
    }

    aggregated[dataKey] = aggregatedValues as any;
  });

  return aggregated;
}

/**
 * Hook para converter dados em formato de gráfico
 */
export function useChartData(keys: (keyof ProjectionData)[]) {
  const data = useFilteredData();

  const chartData = useMemo(() => {
    if (!data || !data.mes) return [];

    return data.mes.map((mes, index) => {
      const point: Record<string, number | string> = { mes };

      keys.forEach((key) => {
        const dataKey = key as keyof ProjectionData;
        if (data[dataKey] && typeof data[dataKey][index] !== 'undefined') {
          point[key] = data[dataKey][index];
        }
      });

      return point;
    });
  }, [data, keys]);

  return chartData;
}
