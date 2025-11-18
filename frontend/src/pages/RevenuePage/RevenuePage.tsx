// frontend/src/pages/RevenuePage/RevenuePage.tsx
import { useFilteredData } from '@/hooks/useFilteredData';
import React, { useMemo } from 'react';
import { WaterfallChart } from '@/components/charts/WaterfallChart';
import { DashboardSkeleton } from '@/components/loading/DashboardSkeleton';
import { ErrorState } from '@/components/loading/ErrorState';
import { FunnelChart } from '@/components/charts/FunnelChart';
import { StackedAreaChart } from '@/components/charts/StackedAreaChart';
import { CohortHeatmap } from '@/components/charts/CohortHeatmap';
import { MOCK_COHORT_DATA } from '@/lib/api/mockCohortData';
import { DataTable } from '@/components/tables/DataTable';
import { ColumnDef } from '@tanstack/react-table';
import { formatCurrency, formatNumber } from '@/lib/utils/formatters';
import { Button } from '@/components/ui/Button';
import { ArrowUpDown } from 'lucide-react';

// Define a type for our table data
type RevenueData = {
    mes: number;
    MRR: number;
    Novos_Pagantes: number;
    Usuarios_Perdidos: number;
    Usuarios_Finais: number;
    ARPU: number;
    Taxa_Conv_Geral: number;
};

// Define columns for the Revenue DataTable
const revenueColumns: ColumnDef<RevenueData>[] = [
    { accessorKey: 'mes', header: 'Mês' },
    { accessorKey: 'MRR', header: 'MRR', cell: ({row}) => formatCurrency(row.getValue('MRR')) },
    { accessorKey: 'Novos_Pagantes', header: 'Novos Clientes' },
    { accessorKey: 'Usuarios_Perdidos', header: 'Churn (Clientes)' },
    { accessorKey: 'Usuarios_Finais', header: 'Clientes Totais' },
    { accessorKey: 'ARPU', header: 'ARPU', cell: ({row}) => formatCurrency(row.getValue('ARPU')) },
    { accessorKey: 'Taxa_Conv_Geral', header: 'Conv. Geral (%)', cell: ({row}) => `${row.getValue('Taxa_Conv_Geral')}%` },
];


import { EmptyState } from '@/components/loading/EmptyState';

// ... (imports and column definitions)

export function RevenuePage() {
  const { data, kpis, isLoading, error } = useFilteredData();

  const waterfallData = useMemo(() => {
    if (!data || !kpis || !data.MRR || data.MRR.length < 12) return null;
    const monthIndex = 11;
    const prevMonthIndex = 10;
    const mrrInicio = (data.MRR || [])[prevMonthIndex] || 0;
    const mrrNovos = (data.MRR_Novos_Clientes || [])[monthIndex] || 0;
    const mrrChurn = (data.MRR_Churn || [])[monthIndex] || 0;
    const mrrExpansao = (data.MRR_Expansao || [])[monthIndex] || 0;
    const mrrContracao = (data.MRR_Contracao || [])[monthIndex] || 0;
    const mrrFim = (data.MRR || [])[monthIndex] || 0;
    return {
      labels: ["MRR Início", "+ Novos", "- Churn", "+ Expansão", "- Contração", "MRR Fim"],
      values: [mrrInicio, mrrNovos, -mrrChurn, mrrExpansao, -mrrContracao, mrrFim],
    };
  }, [data, kpis]);

  const funnelData = useMemo(() => {
    if (!data || !data.Visitantes || data.Visitantes.length < 12) return null;
    const monthIndex = 11;
    const visitantes = (data.Visitantes || [])[monthIndex] || 0;
    const trials = (data.Novos_Trials || [])[monthIndex] || 0;
    const pagantes = (data.Novos_Pagantes || [])[monthIndex] || 0;
    return {
        labels: ['Visitantes', 'Trials', 'Novos Pagantes'],
        values: [visitantes, trials, pagantes],
    }
  }, [data]);

  const areaChartData = useMemo(() => {
    if (!data || !data.mes) return [];
    return data.mes.map((m, index) => ({
      mes: m,
      MRR_Lite: (data.MRR_Lite || [])[index] || 0,
      MRR_Trader: (data.MRR_Trader || [])[index] || 0,
      MRR_Pro: (data.MRR_Pro || [])[index] || 0,
    }));
  }, [data]);

  const tableData: RevenueData[] = useMemo(() => {
    if (!data || !data.mes) return [];
    return data.mes.map((m, index) => ({
        mes: m,
        MRR: (data.MRR || [])[index] || 0,
        Novos_Pagantes: (data.Novos_Pagantes || [])[index] || 0,
        Usuarios_Perdidos: (data.Usuarios_Perdidos || [])[index] || 0,
        Usuarios_Finais: (data.Usuarios_Finais || [])[index] || 0,
        ARPU: (data.ARPU || [])[index] || 0,
        Taxa_Conv_Geral: (data.Taxa_Conv_Geral || [])[index] || 0,
    }));
  }, [data]);

  if (isLoading) {
    return <DashboardSkeleton />;
  }

  if (error || !data || !kpis) {
    return <ErrorState title="Erro ao carregar dados de receita" description={error || "Não foi possível carregar os dados."} />;
  }

  return (
    <div className="space-y-8">
      <div className="p-4 rounded-lg">
        <h1 className="text-3xl font-bold text-slate-900">💰 Dashboard de Receita</h1>
        <p className="text-slate-500">Análise detalhada da composição e projeção da receita.</p>
      </div>

      {areaChartData.length > 0 ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {waterfallData && <WaterfallChart
                title="Composição do MRR (Mês 12)"
                data={waterfallData}
            />}
            {funnelData && <FunnelChart
                title="Funil de Aquisição (Mês 12)"
                data={funnelData}
            />}
            <div className="lg:col-span-2">
                <StackedAreaChart 
                    title="MRR por Plano"
                    data={areaChartData}
                    xKey="mes"
                    yKeys={[
                        { key: 'MRR_Lite', color: '#60a5fa' },
                        { key: 'MRR_Trader', color: '#3b82f6' },
                        { key: 'MRR_Pro', color: '#1d4ed8' },
                    ]}
                />
            </div>
            <CohortHeatmap 
                title="Retenção por Cohort"
                data={MOCK_COHORT_DATA}
            />
            <div className="lg:col-span-2">
                <h3 className="text-lg font-semibold text-slate-800 mb-4">Análise Detalhada de Receita</h3>
                <DataTable columns={revenueColumns} data={tableData} exportable />
            </div>
        </div>
      ) : (
        <EmptyState 
            title="Nenhum dado para o período selecionado"
            description="Tente ajustar os filtros de período para visualizar os dados."
        />
      )}
    </div>
  );
}
