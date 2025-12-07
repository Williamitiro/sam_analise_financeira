import { useMemo, useState } from 'react';
import { InteractiveChart } from '@/components/charts/InteractiveChart';
import { ChartControls } from '@/components/charts/ChartControls';
import { AlertHub } from '@/components/insights/AlertHub';
import { ChartSeries, ChartType } from '@/types/charts';
import { DataTable } from '@/components/tables/DataTable';
import { ColumnDef } from '@tanstack/react-table';
import { formatCurrency, formatNumber } from '@/lib/utils/formatters';
import { Button } from '@/components/ui/Button';
import { ArrowUpDown } from 'lucide-react';
import { EmptyState } from '@/components/loading/EmptyState';

// Define a type for our table data based on chartData
type MonthlyData = {
  mes: number;
  MRR: number;
  Caixa: number;
  Usuarios_Finais: number;
  OPEX: number;
  Lucro_Prejuizo: number;
  Receita_Total: number;
};

// Define columns for the DataTable
const columns: ColumnDef<MonthlyData>[] = [
  {
    accessorKey: 'mes',
    header: ({ column }) => (
      <Button
        variant="ghost"
        onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
      >
        Mês
        <ArrowUpDown className="ml-2 h-4 w-4" />
      </Button>
    ),
    cell: ({ row }) => <div className="text-center font-medium">{row.getValue('mes')}</div>,
  },
  {
    accessorKey: 'MRR',
    header: ({ column }) => (
      <Button
        variant="ghost"
        onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
      >
        MRR
        <ArrowUpDown className="ml-2 h-4 w-4" />
      </Button>
    ),
    cell: ({ row }) => <div className="text-right">{formatCurrency(row.getValue('MRR'))}</div>,
  },
  {
    accessorKey: 'Caixa',
    header: ({ column }) => (
      <Button
        variant="ghost"
        onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
      >
        Caixa
        <ArrowUpDown className="ml-2 h-4 w-4" />
      </Button>
    ),
    cell: ({ row }) => <div className="text-right">{formatCurrency(row.getValue('Caixa'))}</div>,
  },
  {
    accessorKey: 'Usuarios_Finais',
    header: 'Usuários',
    cell: ({ row }) => <div className="text-right">{formatNumber(row.getValue('Usuarios_Finais'))}</div>,
  },
  {
    accessorKey: 'OPEX',
    header: 'OPEX',
    cell: ({ row }) => <div className="text-right">{formatCurrency(row.getValue('OPEX'))}</div>,
  },
  {
    accessorKey: 'Lucro_Prejuizo',
    header: 'Lucro/Prejuízo',
    cell: ({ row }) => {
      const value = row.getValue('Lucro_Prejuizo') as number;
      return (
        <div className={`text-right font-semibold ${value < 0 ? 'text-red-600' : 'text-green-600'}`}>
          {formatCurrency(value)}
        </div>
      )
    }
  },
];

interface InteractiveChartSectionProps {
  data: ProjectionData;
  kpis: KPIs;
}

export const InteractiveChartSection = ({ data, kpis }: InteractiveChartSectionProps) => {
  const [visibleSeries, setVisibleSeries] = useState<Set<ChartSeries>>(
    new Set(['MRR', 'Caixa'])
  );
  const [chartType, setChartType] = useState<ChartType>('line');

  const handleSeriesVisibilityChange = (series: ChartSeries, visible: boolean) => {
    setVisibleSeries(prev => {
      const newSet = new Set(prev);
      if (visible) {
        newSet.add(series);
      } else {
        newSet.delete(series);
      }
      return newSet;
    });
  };

  const chartData: MonthlyData[] = useMemo(() => {
    if (!data || !data.mes) return [];
    return data.mes.map((m, index) => ({
      mes: m,
      MRR: (data.MRR || [])[index] || 0,
      Caixa: (data.Saldo_Caixa || [])[index] || 0,
      Usuarios_Finais: (data.Usuarios_Finais || [])[index] || 0,
      OPEX: (data.OPEX_Total || [])[index] || 0,
      Lucro_Prejuizo: (data.Lucro_Prejuizo_Acumulado || [])[index] || 0,
      Receita_Total: (data.Receita_Total || [])[index] || 0,
    }));
  }, [data]);

  return (
    <section className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
      <h2 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
        <span className="text-2xl">📈</span>
        Análise Temporal
      </h2>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        <div className="lg:col-span-2 flex flex-col gap-6">
          <ChartControls
            visibleSeries={visibleSeries}
            onSeriesVisibilityChange={handleSeriesVisibilityChange}
            chartType={chartType}
            onChartTypeChange={setChartType}
          />
          {chartData.length > 0 ? (
            <>
              <InteractiveChart
                data={chartData}
                visibleSeries={visibleSeries}
                chartType={chartType}
                breakEvenMonth={kpis?.Breakeven_Month}
                valeDaMorteMonth={kpis?.Vale_da_Morte_Month}
              />
              <div className="mt-4">
                <DataTable columns={columns} data={chartData} exportable />
              </div>
            </>
          ) : (
            <EmptyState
              title="Nenhum dado encontrado"
              description="Os filtros selecionados não retornaram nenhum resultado. Tente ajustar o período ou a granularidade."
            />
          )}
        </div>
        <div className="lg:col-span-1 bg-slate-50/50 p-5 rounded-lg border border-slate-200">
          <h3 className="text-base font-semibold text-slate-800 mb-4 flex items-center gap-2">
            <span>🚨</span>
            Alertas Inteligentes
          </h3>
          <AlertHub />
        </div>
      </div>
    </section>
  );
};
