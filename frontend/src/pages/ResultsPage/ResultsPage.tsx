import { useFilteredData } from '@/hooks/useFilteredData';
import { DashboardSkeleton } from '@/components/loading/DashboardSkeleton';
import { ErrorState } from '@/components/loading/ErrorState';
import { useState } from 'react';
import { HeroSection } from './components/HeroSection';
import { MainMetricsGrid } from './components/MainMetricsGrid';
import { InteractiveChartSection } from './components/InteractiveChartSection';
import { EventsTimeline } from './components/EventsTimeline';
import { InsightsSection } from './components/InsightsSection';
import { GlossaryModal } from '@/components/glossary/GlossaryModal';
import { MainControls } from './components/MainControls';

type MetricId = 'mrr' | 'runway' | 'users' | 'ltv_cac' | 'break_even' | 'ltv' | 'cac' | 'arr' | 'ebitda' | 'churn' | 'gross_margin' | 'avg_cac';

export function ResultsPage() {
  const { isLoading, error, data, kpis, insights } = useFilteredData();
  const [isGlossaryOpen, setIsGlossaryOpen] = useState(false);
  const [selectedTerm, setSelectedTerm] = useState<MetricId | null>(null);

  const handleOpenGlossary = (term: MetricId) => {
    setSelectedTerm(term);
    setIsGlossaryOpen(true);
  };

  const handleCloseGlossary = () => {
    setIsGlossaryOpen(false);
    setSelectedTerm(null);
  };

  if (isLoading) {
    return <DashboardSkeleton />;
  }

  if (error || !data || !kpis || !insights) {
    return (
      <ErrorState
        title="Erro ao Carregar Projeção"
        description={error || "Não foi possível encontrar os dados da projeção."}
      />
    );
  }

  return (
    <>
      <MainControls />
      <div className="space-y-8">
        <HeroSection kpis={kpis} />
        <MainMetricsGrid onInfoClick={handleOpenGlossary} kpis={kpis} data={data} />
        <InteractiveChartSection data={data} kpis={kpis} />
        <InsightsSection insights={insights} />
        <EventsTimeline data={data} kpis={kpis} />
      </div>
      <GlossaryModal term={selectedTerm} isOpen={isGlossaryOpen} onClose={handleCloseGlossary} kpis={kpis} />
    </>
  );
}
