// frontend/src/hooks/useFilteredData.ts
import { useMemo } from 'react';
import { useMockProjection } from '@/features/projection/hooks/useMockProjection';
import { useFiltersStore } from '@/stores/filtersStore';
import { ProjectionData } from '@/types/api.types';

// This is a placeholder for a more complex aggregation logic
const applyGranularity = (data: ProjectionData, granularity: 'monthly' | 'quarterly' | 'yearly'): ProjectionData => {
    if (granularity === 'monthly') {
        return data;
    }
    // TODO: Implement quarterly and yearly aggregation
    console.warn(`${granularity} granularity not yet implemented.`);
    return data;
}

export const useFilteredData = () => {
    const { data: rawData, kpis, insights, isLoading, error } = useMockProjection();
    const { periodStart, periodEnd, granularity } = useFiltersStore();

    const filteredData = useMemo(() => {
        if (!rawData || !rawData.mes) {
            return null;
        }

        const startIndex = rawData.mes.findIndex(m => m === periodStart);
        const endIndex = rawData.mes.findIndex(m => m === periodEnd);

        if (startIndex === -1 || endIndex === -1) {
            return rawData; // Return full data if period is invalid
        }

        const slicedData: Partial<ProjectionData> = {};
        for (const key in rawData) {
            if (Array.isArray((rawData as any)[key])) {
                (slicedData as any)[key] = (rawData as any)[key].slice(startIndex, endIndex + 1);
            }
        }

        // TODO: Apply granularity after slicing
        const granularData = applyGranularity(slicedData as ProjectionData, granularity);

        return granularData;

    }, [rawData, periodStart, periodEnd, granularity]);

    return {
        data: filteredData,
        kpis, // KPIs are generally for the full period, not sliced
        insights,
        isLoading,
        error,
    };
};
