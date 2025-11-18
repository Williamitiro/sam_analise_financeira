// frontend/src/components/charts/InteractiveChart.tsx
import {
  ResponsiveContainer,
  LineChart,
  BarChart,
  AreaChart,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  Line,
  Bar,
  Area,
  ReferenceLine,
} from 'recharts';
import { ChartSeries, ChartType } from '@/types/charts';
import { formatCurrency, formatNumber } from '@/lib/utils/formatters';

interface InteractiveChartProps {
  data: any[];
  visibleSeries: Set<ChartSeries>;
  chartType: ChartType;
  breakEvenMonth?: number;
  valeDaMorteMonth?: number;
}

const seriesConfig: Record<ChartSeries, { color: string; format: (val: number) => string; }> = {
  MRR: { color: '#3b82f6', format: (v) => formatCurrency(v, { compact: true }) }, // blue-500
  Caixa: { color: '#22c55e', format: (v) => formatCurrency(v, { compact: true }) }, // green-500
  Usuarios_Finais: { color: '#8b5cf6', format: (v) => formatNumber(v, { compact: true }) }, // violet-500
  OPEX: { color: '#f97316', format: (v) => formatCurrency(v, { compact: true }) }, // orange-500
  Lucro_Prejuizo: { color: '#ef4444', format: (v) => formatCurrency(v, { compact: true }) }, // red-500
  Receita_Total: { color: '#14b8a6', format: (v) => formatCurrency(v, { compact: true }) }, // teal-500
};

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="p-3 bg-white/90 border border-slate-300 rounded-lg shadow-lg backdrop-blur-sm">
        <p className="font-bold text-slate-800">{`Mês ${label}`}</p>
        {payload.map((pld: any) => (
          <div key={pld.dataKey} style={{ color: pld.color }} className="flex justify-between gap-4 items-center">
            <span className="font-medium">{pld.name}:</span>
            <span className="font-mono font-semibold">{seriesConfig[pld.dataKey as ChartSeries].format(pld.value)}</span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

export function InteractiveChart({ data, visibleSeries, chartType, breakEvenMonth, valeDaMorteMonth }: InteractiveChartProps) {
  const ChartComponent = chartType === 'bar' ? BarChart : chartType === 'area' ? AreaChart : LineChart;
  const SeriesComponent = chartType === 'bar' ? Bar : chartType === 'area' ? Area : Line;

  return (
    <div className="w-full h-[450px] p-4 bg-white rounded-lg border border-slate-200 shadow-sm">
      <ResponsiveContainer>
        <ChartComponent data={data} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="mes" stroke="#475569" fontSize={12} />
          <YAxis
            stroke="#475569"
            fontSize={12}
            tickFormatter={(value) => formatCurrency(value, { compact: true })}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend iconSize={12} wrapperStyle={{ fontSize: '14px', paddingTop: '20px' }} />

          {Array.from(visibleSeries).map((series) => (
            <SeriesComponent
              key={series}
              type="monotone"
              dataKey={series}
              name={series.replace(/_/g, ' ')}
              stroke={seriesConfig[series].color}
              fill={seriesConfig[series].color}
              fillOpacity={chartType === 'area' ? 0.2 : 1}
              strokeWidth={2}
              dot={chartType === 'line' ? { r: 3, strokeWidth: 2 } : false}
              isAnimationActive={false}
            />
          ))}

          {breakEvenMonth && (
            <ReferenceLine
              x={breakEvenMonth}
              stroke="#22c55e"
              strokeWidth={2}
              strokeDasharray="4 4"
              label={{ value: 'Break-Even', position: 'top', fill: '#22c55e', fontSize: 12 }}
            />
          )}
          {valeDaMorteMonth && (
             <ReferenceLine
              x={valeDaMorteMonth}
              stroke="#ef4444"
              strokeWidth={2}
              strokeDasharray="4 4"
              label={{ value: 'Vale da Morte', position: 'top', fill: '#ef4444', fontSize: 12 }}
            />
          )}

        </ChartComponent>
      </ResponsiveContainer>
    </div>
  );
}
