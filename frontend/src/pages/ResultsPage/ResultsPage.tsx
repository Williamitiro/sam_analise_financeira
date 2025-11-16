import { useMockProjection } from '@/features/projection/hooks/useMockProjection';
import { DashboardSkeleton } from '@/components/loading/DashboardSkeleton';
import { ErrorState } from '@/components/loading/ErrorState';
import { KPIGrid } from '@/components/metrics/KPIGrid';
import { MRRRunwayChart } from '@/components/charts/MRRRunwayChart';
import { TornadoChart } from '@/components/charts/TornadoChart';

export function ResultsPage() {
  const { isLoading, error, data } = useMockProjection();

  if (isLoading) {
    return <DashboardSkeleton />;
  }

  if (error || !data) {
    return (
      <ErrorState
        title="Erro ao Carregar Projeção"
        description={error || 'Não foi possível encontrar os dados da projeção.'}
      />
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold mb-4 text-slate-800">Métricas Principais</h2>
        <KPIGrid />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        <div className="lg:col-span-2">
          <MRRRunwayChart />
        </div>
        <div className="lg:col-span-1">
          <TornadoChart />
        </div>
      </div>
    </div>
  );
}