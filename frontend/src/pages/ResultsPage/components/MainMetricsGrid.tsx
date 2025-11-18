// frontend/src/pages/ResultsPage/components/MainMetricsGrid.tsx
import { KPIGrid } from '@/components/metrics/KPIGrid';
import { KPIs, ProjectionData } from '@/types/api.types';
import React from 'react';

type MetricId = 'mrr' | 'runway' | 'users' | 'ltv_cac' | 'break_even' | 'ltv' | 'cac' | 'arr' | 'ebitda' | 'churn' | 'gross_margin' | 'avg_cac';

interface MainMetricsGridProps {
  onInfoClick: (term: MetricId) => void;
  kpis: KPIs;
  data: ProjectionData;
}

export const MainMetricsGrid = ({ onInfoClick, kpis, data }: MainMetricsGridProps) => {
  return (
    <div className="p-4 rounded-lg">
      <h2 className="text-lg font-semibold text-slate-800 mb-4">📈 Métricas Principais</h2>
      {/* The existing KPIGrid will be rendered here */}
      <KPIGrid onInfoClick={onInfoClick} kpis={kpis} data={data} />
    </div>
  );
};
