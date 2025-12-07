import { useFilteredData } from '@/hooks/useFilteredData';
import { DashboardSkeleton } from '@/components/loading/DashboardSkeleton';
import { ErrorState } from '@/components/loading/ErrorState';
import { useEffect, useState } from 'react';
import { DashboardOverview } from './components/DashboardOverview';
import { InteractiveChartSection } from './components/InteractiveChartSection';
import { EventsTimeline } from './components/EventsTimeline';
import { InsightsSection } from './components/InsightsSection';
import { GlossaryModal } from '@/components/glossary/GlossaryModal';
import { useProjectionStore } from '@/stores/projectionStore';
import { defaultConfig } from '@/lib/api/projection';

type MetricId = 'mrr' | 'runway' | 'users' | 'ltv_cac' | 'break_even' | 'ltv' | 'cac' | 'arr' | 'ebitda' | 'churn' | 'gross_margin' | 'avg_cac';

export function ResultsPage() {
  const { isLoading, error, data, kpis, insights } = useFilteredData();
  const [isGlossaryOpen, setIsGlossaryOpen] = useState(false);
  const [selectedTerm, setSelectedTerm] = useState<MetricId | null>(null);

  useEffect(() => {
    // Run initial projection only once if there's no data
    const { data, isLoading, error, runProjection } = useProjectionStore.getState();
    if (!data && !isLoading && !error) {
      runProjection(defaultConfig);
    }
  }, []);

  const handleOpenGlossary = (term: MetricId) => {
    setSelectedTerm(term);
    setIsGlossaryOpen(true);
  };

  const handleCloseGlossary = () => {
    setIsGlossaryOpen(false);
    setSelectedTerm(null);
  };

  if (isLoading || (!data && !error)) {
    return <DashboardSkeleton />;
  }

  if (error || !data || !kpis || !insights) {
    return (
      <ErrorState
        title="Erro ao Carregar Projeção"
        description={error || "Não foi possível encontrar os dados da projeção. Tente recalcular."}
      />
    );
  }

  return (
    <>
      <div className="space-y-8">
        <DashboardOverview kpis={kpis} data={data} onInfoClick={handleOpenGlossary} />
        <InteractiveChartSection data={data} kpis={kpis} />
        <InsightsSection insights={insights} />
        <EventsTimeline data={data} kpis={kpis} />
      </div>
      <GlossaryModal term={selectedTerm} isOpen={isGlossaryOpen} onClose={handleCloseGlossary} kpis={kpis} />
    </>
  );
}