import React from 'react';
import { KPIs, ProjectionData } from '@/types/api.types';
import { MetricCard } from '@/components/metrics/MetricCard';
import { formatCurrency, formatNumber, calculateDelta } from '@/lib/utils/formatters';

type MetricId = 'mrr' | 'runway' | 'users' | 'ltv_cac' | 'break_even' | 'ltv' | 'cac' | 'arr' | 'ebitda' | 'churn' | 'gross_margin' | 'avg_cac';

interface DashboardOverviewProps {
  kpis: KPIs;
  data: ProjectionData;
  onInfoClick: (term: MetricId) => void;
}

export const DashboardOverview = ({ kpis, data, onInfoClick }: DashboardOverviewProps) => {
  
  const getDelta = (series?: number[]): number => {
    if (!series || series.length < 2) return 0;
    const current = series[series.length - 1];
    const previous = series[series.length - 2];
    return calculateDelta(current, previous);
  };

  const formatSparkline = (series?: number[]) => {
    return (series || []).map((val, index) => ({ month: index + 1, value: val }));
  };

  // --- Section 1: Executive Summary ---
  const executiveMetrics = [
    {
      id: 'runway' as MetricId,
      label: 'Runway',
      value: `${kpis?.Runway_Meses ?? 0} meses`,
      status: {
        text: (kpis?.Runway_Meses ?? 0) > 12 ? 'Seguro' : 'Atenção',
        color: ((kpis?.Runway_Meses ?? 0) > 12 ? 'green' : 'amber') as 'green' | 'amber' | 'red',
      },
      sparklineData: formatSparkline(data?.Saldo_Caixa?.slice(-12)),
      description: 'Caixa disponível',
    },
    {
      id: 'break_even' as MetricId,
      label: 'Break-Even',
      value: `Mês ${kpis?.Breakeven_Month || '-'}`,
      description: `MRR: ${formatCurrency(kpis?.Breakeven_MRR || 0, { compact: true })}`,
      status: {
        text: kpis?.Breakeven_Month ? 'Atingido' : 'Pendente',
        color: (kpis?.Breakeven_Month ? 'green' : 'amber') as 'green' | 'amber' | 'red',
      },
       sparklineData: formatSparkline(data?.Resultado_Operacional?.slice(-12)),
    },
    {
      id: 'ebitda' as MetricId,
      label: 'Saldo em Caixa',
      value: formatCurrency(data?.Saldo_Caixa?.[data.Saldo_Caixa.length - 1] || 0, { compact: true }),
      change: `${getDelta(data?.Saldo_Caixa).toFixed(1)}%`,
      trend: (getDelta(data?.Saldo_Caixa) >= 0 ? 'up' : 'down') as 'up' | 'down',
      sparklineData: formatSparkline(data?.Saldo_Caixa?.slice(-12)),
      description: 'Final do período',
    },
    {
      id: 'ebitda' as MetricId, // Reusing ID for now
      label: 'Resultado Líquido',
      value: formatCurrency(data?.Lucro_Liquido?.[data.Lucro_Liquido.length - 1] || 0, { compact: true }),
      change: `${getDelta(data?.Lucro_Liquido).toFixed(1)}%`,
      trend: (getDelta(data?.Lucro_Liquido) >= 0 ? 'up' : 'down') as 'up' | 'down',
      sparklineData: formatSparkline(data?.Lucro_Liquido?.slice(-12)),
      description: 'Último mês',
    }
  ];

  // --- Section 2: Growth & Revenue ---
  const growthMetrics = [
    {
      id: 'mrr' as MetricId,
      label: 'MRR',
      value: formatCurrency(kpis?.MRR_Final ?? 0, { compact: true }),
      change: `${getDelta(data?.MRR).toFixed(1)}%`,
      trend: (getDelta(data?.MRR) >= 0 ? 'up' : 'down') as 'up' | 'down',
      sparklineData: formatSparkline(data?.MRR?.slice(-12)),
      description: 'Receita Recorrente',
    },
    {
      id: 'arr' as MetricId,
      label: 'ARR',
      value: formatCurrency((kpis?.MRR_Final ?? 0) * 12, { compact: true }),
      change: `${getDelta(data?.MRR).toFixed(1)}%`, // Assuming ARR follows MRR trend
      trend: 'up' as 'up' | 'down',
      sparklineData: formatSparkline(data?.MRR?.slice(-12).map(m => m * 12)),
      description: 'Anualizado',
    },
    {
      id: 'users' as MetricId,
      label: 'Usuários Ativos',
      value: formatNumber(kpis?.Usuarios_Final ?? 0, { compact: true }),
      change: `+${(data?.Novos_Pagantes || []).slice(-1)[0] || 0}`,
      trend: (getDelta(data?.Usuarios_Finais) >= 0 ? 'up' : 'down') as 'up' | 'down',
      sparklineData: formatSparkline(data?.Usuarios_Finais?.slice(-12)),
      description: 'Base total',
    },
    {
      id: 'churn' as MetricId,
      label: 'Churn Rate',
      value: '4.0%', // Placeholder, should come from data if available
      change: '0.0%',
      trend: 'neutral' as 'neutral',
      sparklineData: formatSparkline(data?.Usuarios_Perdidos?.slice(-12)), // Proxy for churn
      description: 'Mensal',
    }
  ];

  // --- Section 3: Unit Economics ---
  const efficiencyMetrics = [
    {
      id: 'ltv' as MetricId,
      label: 'LTV',
      value: formatCurrency(kpis?.LTV_Final ?? 0),
      description: 'Lifetime Value',
      sparklineData: formatSparkline(Array(12).fill(kpis?.LTV_Final ?? 0)), // Constant for now
    },
    {
      id: 'cac' as MetricId,
      label: 'CAC',
      value: formatCurrency(kpis?.CAC_Medio_Periodo ?? 0),
      description: 'Custo Aquisição',
      sparklineData: formatSparkline(data?.CAC_Mensal?.slice(-12)),
    },
    {
      id: 'ltv_cac' as MetricId,
      label: 'LTV / CAC',
      value: `${(kpis?.LTV_CAC_Ratio_Final ?? 0).toFixed(1)}x`,
      status: {
        text: (kpis?.LTV_CAC_Ratio_Final ?? 0) > 3 ? 'Saudável' : 'Atenção',
        color: ((kpis?.LTV_CAC_Ratio_Final ?? 0) > 3 ? 'green' : 'amber') as 'green' | 'amber' | 'red',
      },
      sparklineData: formatSparkline(Array(12).fill(kpis?.LTV_CAC_Ratio_Final ?? 0)),
      description: 'Eficiência',
    },
    {
      id: 'gross_margin' as MetricId,
      label: 'Margem Bruta',
      value: `${(data?.Margem_Bruta_Pct?.[data.Margem_Bruta_Pct.length - 1] || 0).toFixed(1)}%`,
      status: {
        text: (data?.Margem_Bruta_Pct?.[data.Margem_Bruta_Pct.length - 1] || 0) > 70 ? 'Excelente' : 'Ok',
        color: ((data?.Margem_Bruta_Pct?.[data.Margem_Bruta_Pct.length - 1] || 0) > 70 ? 'green' : 'amber') as 'green' | 'amber' | 'red',
      },
      sparklineData: formatSparkline(data?.Margem_Bruta_Pct?.slice(-12)),
      description: 'Lucrabilidade',
    }
  ];

  return (
    <div className="space-y-8">
      {/* Executive Summary */}
      <section>
        <div className="flex items-center gap-2 mb-4">
          <span className="text-2xl">🚨</span>
          <h2 className="text-xl font-bold text-slate-800">Resumo Executivo</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {executiveMetrics.map((metric, idx) => (
            <MetricCard key={`exec-${idx}`} {...metric} onInfoClick={onInfoClick} />
          ))}
        </div>
      </section>

      {/* Growth & Revenue */}
      <section>
        <div className="flex items-center gap-2 mb-4">
          <span className="text-2xl">🚀</span>
          <h2 className="text-xl font-bold text-slate-800">Crescimento & Receita</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {growthMetrics.map((metric, idx) => (
            <MetricCard key={`growth-${idx}`} {...metric} onInfoClick={onInfoClick} />
          ))}
        </div>
      </section>

      {/* Unit Economics */}
      <section>
        <div className="flex items-center gap-2 mb-4">
          <span className="text-2xl">💰</span>
          <h2 className="text-xl font-bold text-slate-800">Eficiência (Unit Economics)</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {efficiencyMetrics.map((metric, idx) => (
            <MetricCard key={`eff-${idx}`} {...metric} onInfoClick={onInfoClick} />
          ))}
        </div>
      </section>
    </div>
  );
};
