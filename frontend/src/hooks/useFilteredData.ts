// frontend/src/hooks/useFilteredData.ts
import { useMemo } from 'react';
import { useProjectionStore } from '@/stores/projectionStore'; // Changed import
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
    // Changed to use the projection store
    const { data: projectionData, kpis, insights, isLoading, error } = useProjectionStore();
    const { periodStart, periodEnd, granularity } = useFiltersStore();

    console.log('useFilteredData called. isLoading:', isLoading, 'error:', error, 'projectionData:', projectionData);

    const filteredData = useMemo(() => {
        if (!projectionData || projectionData.length === 0) {
            return null;
        }

        // 1. Filter by date range
        const startIndex = projectionData.findIndex(row => row.mes === periodStart);
        const endIndex = projectionData.findIndex(row => row.mes === periodEnd);

        const slicedData = (startIndex === -1 || endIndex === -1)
            ? projectionData // Return full data if period is invalid
            : projectionData.slice(startIndex, endIndex + 1);
        
        if (slicedData.length === 0) {
            return null;
        }

        // 2. Transform from Array-of-Objects to Object-of-Arrays
        const transformedData: ProjectionData = {};
        const keys = Object.keys(slicedData[0]); // Get keys from the first row (e.g., 'mes', 'mrr', 'usuarios')
        
        for (const key of keys) {
            // For each key, create an array by mapping over the sliced data
            (transformedData as any)[key] = slicedData.map(row => row[key]);
        }

        // 3. TODO: Apply granularity - this part is still a placeholder but the structure is now correct
        const granularData = applyGranularity(transformedData, granularity);

        return granularData;

    }, [projectionData, periodStart, periodEnd, granularity]);

    return {
        data: filteredData,
        kpis, // KPIs are generally for the full period, not sliced
        insights,
        isLoading,
        error,
    };
};
