import { useFiltersStore } from '@/stores/filtersStore';
import { SimulatorTrigger } from '@/pages/ResultsPage/components/SimulatorTrigger';
import { ProjectButton } from './ProjectButton';

export function DashboardHeader() {
  const { periodEnd } = useFiltersStore();

  return (
    <div className="flex items-center justify-between border-b border-slate-200/80 pb-6 mb-8">
      {/* Left Side */}
      <div>
        <h1 className="text-3xl font-bold text-slate-900">
          📊 Visão Geral
        </h1>
        <p className="text-sm text-slate-600 mt-1">
          Projeção de <span className="font-semibold">{periodEnd}</span> meses • <span className="text-green-600 font-medium">✓ Dados atualizados</span>
        </p>
      </div>

      {/* Right Side */}
      <div className="flex items-center gap-2">
        <SimulatorTrigger />
        <ProjectButton />
      </div>
    </div>
  );
}
