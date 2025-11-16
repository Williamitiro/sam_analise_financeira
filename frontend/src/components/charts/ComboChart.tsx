import {
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { ChartContainer } from './ChartContainer';
import { formatCurrency, formatMonth } from '@/lib/utils/formatters';
import { CHART_COLORS } from '@/lib/theme/colors';

type ChartData = {
  mes: number;
  [key: string]: number | string;
};

interface ComboChartProps {
  title: string;
  data: ChartData[];
  barKeys: (keyof Omit<ChartData, 'mes'>)[];
  lineKeys: (keyof Omit<ChartData, 'mes'>)[];
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-sm">
        <p className="font-semibold text-gray-800">{formatMonth(label, { format: 'long' })}</p>
        {payload.map((pld: any, index: number) => (
          <div key={index} style={{ color: pld.color || pld.fill }} className="flex justify-between gap-4">
            <span>{pld.name}:</span>
            <span className="font-bold">{formatCurrency(pld.value, { decimals: 0 })}</span>
          </div>
        ))}
      </div>
    );
  }

  return null;
};

export function ComboChart({ title, data, barKeys, lineKeys }: ComboChartProps) {
  return (
    <ChartContainer title={title} height={400}>
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart data={data} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis
            dataKey="mes"
            tickFormatter={(tick) => formatMonth(tick)}
            tick={{ fontSize: 12 }}
            stroke="#6b7280"
          />
          <YAxis
            tickFormatter={(tick) => formatCurrency(tick, { compact: true })}
            tick={{ fontSize: 12 }}
            stroke="#6b7280"
            width={80}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ fontSize: '14px' }} />
          
          {barKeys.map((key, index) => (
            <Bar
              key={String(key)}
              dataKey={String(key)}
              name={String(key).replace(/_/g, ' ')}
              fill={CHART_COLORS[index % CHART_COLORS.length]}
            />
          ))}

          {lineKeys.map((key, index) => (
            <Line
              key={String(key)}
              type="monotone"
              dataKey={String(key)}
              name={String(key).replace(/_/g, ' ')}
              stroke={CHART_COLORS[(barKeys.length + index) % CHART_COLORS.length]}
              strokeWidth={2}
              dot={{ r: 2 }}
              activeDot={{ r: 6 }}
            />
          ))}
        </ComposedChart>
      </ResponsiveContainer>
    </ChartContainer>
  );
}
