// frontend/src/components/charts/ChartControls.tsx
import { Checkbox } from '@/components/ui/checkbox';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { ChartSeries, ChartType } from '@/types/charts';

interface ChartControlsProps {
  visibleSeries: Set<ChartSeries>;
  onSeriesVisibilityChange: (series: ChartSeries, visible: boolean) => void;
  chartType: ChartType;
  onChartTypeChange: (type: ChartType) => void;
}

const seriesOptions: { id: ChartSeries; label: string }[] = [
  { id: 'MRR', label: 'MRR' },
  { id: 'Caixa', label: 'Caixa' },
  { id: 'Usuarios_Finais', label: 'Usuários' },
  { id: 'OPEX', label: 'OPEX' },
  { id: 'Lucro_Prejuizo', label: 'Lucro' },
  { id: 'Receita_Total', label: 'Receita' },
];

export function ChartControls({
  visibleSeries,
  onSeriesVisibilityChange,
  chartType,
  onChartTypeChange,
}: ChartControlsProps) {
  return (
    <div className="flex flex-col sm:flex-row gap-4 justify-between items-center p-4 bg-slate-50 rounded-lg border border-slate-200">
      <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
        <p className="text-sm font-medium text-slate-700">Visualizar:</p>
        {seriesOptions.map(({ id, label }) => (
          <div key={id} className="flex items-center gap-2">
            <Checkbox
              id={`series-${id}`}
              checked={visibleSeries.has(id)}
              onCheckedChange={(checked) => onSeriesVisibilityChange(id, !!checked)}
            />
            <label htmlFor={`series-${id}`} className="text-sm font-medium text-slate-800 cursor-pointer">
              {label}
            </label>
          </div>
        ))}
      </div>
      <div className="flex items-center gap-2">
        <label className="text-sm font-medium text-slate-700">Tipo:</label>
        <Select value={chartType} onValueChange={(value) => onChartTypeChange(value as ChartType)}>
          <SelectTrigger className="w-[120px] bg-white">
            <SelectValue placeholder="Selecione" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="line">Linha</SelectItem>
            <SelectItem value="bar">Barras</SelectItem>
            <SelectItem value="area">Área</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}
