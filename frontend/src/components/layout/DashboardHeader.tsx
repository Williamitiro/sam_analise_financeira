import { useFiltersStore } from '@/stores/filtersStore';
import { Button } from '@/components/ui/Button';
import { AlertHub } from '../insights/AlertHub';

export function DashboardHeader() {
  const { periodEnd } = useFiltersStore();

  return (
    <div className="flex items-center justify-between border-b border-slate-200/80 pb-5 mb-4">
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
      <div className="flex items-center gap-4">
        <h3 className="text-sm font-medium text-slate-600">Configuração Rápida:</h3>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">Realista</Button>
          <Button variant="outline" size="sm">Otimista</Button>
          <Button variant="outline" size="sm">Pessimista</Button>
        </div>
        <Button size="sm">Projetar</Button>
        <AlertHub />
      </div>
    </div>
  );
}
