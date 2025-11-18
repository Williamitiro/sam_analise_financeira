// frontend/src/pages/CostsPage/CostsPage.tsx
import { useFilteredData } from '@/hooks/useFilteredData';
import React, { useMemo } from 'react';
import { SankeyChart } from '@/components/charts/SankeyChart';
import { DashboardSkeleton } from '@/components/loading/DashboardSkeleton';
import { ErrorState } from '@/components/loading/ErrorState';
import { PieChartWithDrilldown } from '@/components/charts/PieChartWithDrilldown';
import { StackedBarChart } from '@/components/charts/StackedBarChart';
import { DataTable } from '@/components/tables/DataTable';
import { ColumnDef } from '@tanstack/react-table';
import { formatCurrency } from '@/lib/utils/formatters';

// Define a type for our table data
type CostData = {
    mes: number;
    OPEX_Total: number;
    Custo_Pessoal: number;
    Custo_Infra: number;
    Custo_Marketing: number;
    COGS_Total: number;
};

// Define columns for the Costs DataTable
const costsColumns: ColumnDef<CostData>[] = [
    { accessorKey: 'mes', header: 'Mês' },
    { accessorKey: 'OPEX_Total', header: 'OPEX Total', cell: ({row}) => formatCurrency(row.getValue('OPEX_Total')) },
    { accessorKey: 'Custo_Pessoal', header: 'Pessoal', cell: ({row}) => formatCurrency(row.getValue('Custo_Pessoal')) },
    { accessorKey: 'Custo_Infra', header: 'Infra', cell: ({row}) => formatCurrency(row.getValue('Custo_Infra')) },
    { accessorKey: 'Custo_Marketing', header: 'Marketing', cell: ({row}) => formatCurrency(row.getValue('Custo_Marketing')) },
    { accessorKey: 'COGS_Total', header: 'COGS', cell: ({row}) => formatCurrency(row.getValue('COGS_Total')) },
];

import { EmptyState } from '@/components/loading/EmptyState';

// ... (imports and column definitions)

export function CostsPage() {
    const { data, isLoading, error } = useFilteredData();

    const sankeyData = useMemo(() => {
        if (!data || !data.COGS_Total || data.COGS_Total.length < 12) return null;
        const monthIndex = 11; // Mês 12
        const links = [
            { from: 'Receita', to: 'COGS', value: (data.COGS_Total || [])[monthIndex] || 0 },
            { from: 'Receita', to: 'OPEX', value: (data.OPEX_Total || [])[monthIndex] || 0 },
            { from: 'Receita', to: 'Lucro Bruto', value: (data.Lucro_Bruto || [])[monthIndex] || 0 },
            { from: 'OPEX', to: 'Pessoal', value: ((data.Custo_Pessoal_CLT || [])[monthIndex] || 0) + ((data.Custo_Pessoal_PJ || [])[monthIndex] || 0) },
            { from: 'OPEX', to: 'Infra', value: (data.Custo_Infra || [])[monthIndex] || 0 },
            { from: 'OPEX', to: 'Marketing', value: (data.Custo_Marketing || [])[monthIndex] || 0 },
            { from: 'OPEX', to: 'Ferramentas', value: (data.Custo_Ferramentas || [])[monthIndex] || 0 },
        ];
        const nodes = Array.from(new Set(links.flatMap(l => [l.from, l.to]))).map(name => ({ name }));
        const nodeIndices = Object.fromEntries(nodes.map((node, i) => [node.name, i]));
        const plotlyLinks = links.map(l => ({ source: nodeIndices[l.from], target: nodeIndices[l.to], value: l.value }));
        return { nodes, links: plotlyLinks };
    }, [data]);

    const opexPieData = useMemo(() => {
        if (!data || !data.Custo_Pessoal_CLT || data.Custo_Pessoal_CLT.length < 12) return null;
        const monthIndex = 11; // Mês 12
        return {
            data: {
                'Pessoal': ((data.Custo_Pessoal_CLT || [])[monthIndex] || 0) + ((data.Custo_Pessoal_PJ || [])[monthIndex] || 0),
                'Infra': (data.Custo_Infra || [])[monthIndex] || 0,
                'Marketing': (data.Custo_Marketing || [])[monthIndex] || 0,
                'Ferramentas': (data.Custo_Ferramentas || [])[monthIndex] || 0,
                'Serviços': (data.Custo_Servicos_Profissionais || [])[monthIndex] || 0,
            },
            breakdown: {
                'Pessoal': {
                    'CLT': (data.Custo_Pessoal_CLT || [])[monthIndex] || 0,
                    'PJ': (data.Custo_Pessoal_PJ || [])[monthIndex] || 0,
                    'Fundador': (data.Salario_Fundador || [])[monthIndex] || 0,
                },
                'Infra': { 'Servidores': (data.Custo_Infra || [])[monthIndex] * 0.7 || 0, 'APIs Terceiras': (data.Custo_Infra || [])[monthIndex] * 0.3 || 0 }
            }
        }
    }, [data]);

    const barChartData = useMemo(() => {
        if (!data || !data.mes) return [];
        return data.mes.map((m, index) => ({
          mes: m,
          Custos_Fixos: (data.Custos_Fixos || [])[index] || 0,
          Custos_Variaveis: (data.Custos_Variaveis || [])[index] || 0,
        }));
      }, [data]);

    const tableData: CostData[] = useMemo(() => {
        if (!data || !data.mes) return [];
        return data.mes.map((m, index) => ({
            mes: m,
            OPEX_Total: (data.OPEX_Total || [])[index] || 0,
            Custo_Pessoal: ((data.Custo_Pessoal_CLT || [])[index] || 0) + ((data.Custo_Pessoal_PJ || [])[index] || 0),
            Custo_Infra: (data.Custo_Infra || [])[index] || 0,
            Custo_Marketing: (data.Custo_Marketing || [])[index] || 0,
            COGS_Total: (data.COGS_Total || [])[index] || 0,
        }));
      }, [data]);

    if (isLoading) {
        return <DashboardSkeleton />;
    }

    if (error || !data) {
        return <ErrorState title="Erro ao carregar dados de custos" description={error || "Não foi possível carregar os dados."} />;
    }

    return (
        <div className="space-y-8">
            <div className="p-4 rounded-lg">
                <h1 className="text-3xl font-bold text-slate-900">💸 Dashboard de Custos</h1>
                <p className="text-slate-500">Análise detalhada da composição e projeção dos custos.</p>
            </div>

            {barChartData.length > 0 ? (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {sankeyData && <SankeyChart 
                        title="Fluxo de Dinheiro (Mês 12)"
                        data={sankeyData}
                    />}
                    {opexPieData && <PieChartWithDrilldown
                        title="Composição de OPEX (Mês 12)"
                        data={opexPieData.data}
                        breakdown={opexPieData.breakdown}
                    />}
                    <div className="lg:col-span-2">
                        <StackedBarChart 
                            title="Custos Fixos vs. Variáveis"
                            data={barChartData}
                            xKey="mes"
                            yKeys={[
                                { key: 'Custos_Fixos', color: '#3b82f6' },
                                { key: 'Custos_Variaveis', color: '#f97316' },
                            ]}
                        />
                    </div>
                    <div className="lg:col-span-2">
                        <h3 className="text-lg font-semibold text-slate-800 mb-4">Análise Detalhada de Custos</h3>
                        <DataTable columns={costsColumns} data={tableData} exportable />
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
