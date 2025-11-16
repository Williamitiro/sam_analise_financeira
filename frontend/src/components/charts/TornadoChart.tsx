import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LabelList,
} from 'recharts';
import { ChartContainer } from './ChartContainer';
import { formatPercentage } from '@/lib/utils/formatters';

const sensitivityData = [
  { variable: 'Churn', impact: 18.5 },
  { variable: 'Preço Médio', impact: 15.2 },
  { variable: 'CAC', impact: -12.8 },
  { variable: 'Custo Pessoal', impact: -9.7 },
  { variable: 'Conv. Pagante', impact: 8.1 },
].sort((a, b) => Math.abs(b.impact) - Math.abs(a.impact));

const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="rounded-lg bg-white border border-slate-200 p-3 shadow-lg">
        <p className="text-sm font-medium text-slate-900">{payload[0].payload.variable}</p>
        <p className="text-sm text-slate-600">
          Impacto no Resultado: <span className="font-bold">{formatPercentage(payload[0].value, { showSign: true })}</span>
        </p>
      </div>
    );
  }
  return null;
};

export function TornadoChart() {
  return (
    <ChartContainer title="Análise de Sensibilidade" subtitle="Impacto de variáveis no Lucro Final">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          layout="vertical"
          data={sensitivityData}
          margin={{ top: 5, right: 30, left: 30, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
          <XAxis type="number" tickFormatter={(v) => `${v}%`} tick={{ fontSize: 12, fill: '#64748b' }} />
          <YAxis
            type="category"
            dataKey="variable"
            width={80}
            tick={{ fontSize: 12, fill: '#64748b' }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(241, 245, 249, 0.5)' }} />
          <Bar dataKey="impact" radius={[0, 4, 4, 0]}>
            <LabelList
              dataKey="impact"
              position="right"
              formatter={(v: number) => `${v.toFixed(1)}%`}
              fontSize={12}
              fill="#334155"
            />
            {sensitivityData.map((entry, index) => (
              <cell key={`cell-${index}`} fill={entry.impact > 0 ? '#10b981' : '#ef4444'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </ChartContainer>
  );
}
