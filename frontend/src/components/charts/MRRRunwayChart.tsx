import {
  ComposedChart,
  Area,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  ReferenceDot,
} from 'recharts';
import { ChartContainer } from './ChartContainer';
import { formatCurrency, formatMonth } from '@/lib/utils/formatters';
import { useChartData } from '@/features/projection/hooks/useProjectionData';

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="rounded-lg bg-white border border-slate-200 p-3 shadow-lg">
        <p className="text-sm font-medium text-slate-900">{formatMonth(label, { format: 'long' })}</p>
        {payload.map((p: any, i: number) => (
          <div key={i} className="flex items-center gap-2 mt-1">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: p.stroke }} />
            <span className="text-sm text-slate-600">{p.name}:</span>
            <span className="text-sm font-semibold text-slate-900">
              {formatCurrency(p.value, { decimals: 0 })}
            </span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

export function MRRRunwayChart() {
  const chartData = useChartData(['MRR', 'Saldo_Caixa']);

  return (
    <ChartContainer title="Projeção Financeira (MRR & Caixa)">
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart data={chartData} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
          <defs>
            <linearGradient id="colorMrr" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="colorCash" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis
            dataKey="mes"
            tickFormatter={(tick) => formatMonth(tick)}
            tick={{ fontSize: 12, fill: '#64748b' }}
            stroke="#cbd5e1"
          />
          <YAxis
            yAxisId="left"
            tickFormatter={(tick) => formatCurrency(tick, { compact: true })}
            tick={{ fontSize: 12, fill: '#64748b' }}
            stroke="#cbd5e1"
            label={{ value: 'MRR', angle: -90, position: 'insideLeft', fill: '#64748b' }}
          />
          <YAxis
            yAxisId="right"
            orientation="right"
            tickFormatter={(tick) => formatCurrency(tick, { compact: true })}
            tick={{ fontSize: 12, fill: '#64748b' }}
            stroke="#cbd5e1"
            label={{ value: 'Caixa', angle: 90, position: 'insideRight', fill: '#64748b' }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ fontSize: '14px' }} />
          
          <Area
            yAxisId="left"
            type="monotone"
            dataKey="MRR"
            name="MRR"
            stroke="#6366f1"
            fill="url(#colorMrr)"
            strokeWidth={2}
          />
          <Area
            yAxisId="right"
            type="monotone"
            dataKey="Saldo_Caixa"
            name="Saldo de Caixa"
            stroke="#10b981"
            strokeDasharray="5 5"
            fill="url(#colorCash)"
            strokeWidth={2}
          />
          
          <ReferenceLine yAxisId="right" x={13} stroke="#f59e0b" strokeDasharray="3 3" />
          <ReferenceDot yAxisId="right" y={148} x={13} r={5} fill="#10b981" stroke="white" strokeWidth={2} />
        </ComposedChart>
      </ResponsiveContainer>
    </ChartContainer>
  );
}
