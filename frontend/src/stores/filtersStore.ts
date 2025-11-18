// frontend/src/stores/filtersStore.ts
import { create } from 'zustand';

type Granularity = 'monthly' | 'quarterly' | 'yearly';

interface FiltersState {
  periodStart: number;
  periodEnd: number;
  granularity: Granularity;
  setPeriod: (start: number, end: number) => void;
  setGranularity: (granularity: Granularity) => void;
  resetFilters: () => void;
}

export const useFiltersStore = create<FiltersState>((set) => ({
  periodStart: 1,
  periodEnd: 24,
  granularity: 'monthly',
  setPeriod: (start, end) => set({ periodStart: start, periodEnd: end }),
  setGranularity: (granularity) => set({ granularity }),
  resetFilters: () => set({
    periodStart: 1,
    periodEnd: 36,
    granularity: 'monthly',
  }),
}));
