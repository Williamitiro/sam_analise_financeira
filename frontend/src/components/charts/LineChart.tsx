import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart,
} from 'recharts';
import { ChartContainer } from './ChartContainer';
import { formatCurrency, formatMonth, formatNumber, formatPercentage } from '@/lib/utils/formatters';
import { CHART_COLORS } from '@/lib/theme/colors';

type ChartData = {
  mes: number;
  [key: string]: number | string;
};

interface LineChartProps {
  title: string;
  data: ChartData[];
  yKeys: (keyof Omit<ChartData, 'mes'>)[];
  format?: 'currency' | 'number' | 'percentage';
  stacked?: boolean;
}

const CustomTooltip = ({ active, payload, label, format }: any) => {
  if (active && payload && payload.length) {
    const formatValue = (val: number) => {
      switch (format) {
        case 'currency':
          return formatCurrency(val, { decimals: 2 });
        case 'number':
          return formatNumber(val);
        case 'percentage':
          return formatPercentage(val);
        default:
          return val.toString();
      }
    };

    return (
      <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-sm">
        <p className="font-semibold text-gray-800">{formatMonth(label, { format: 'long' })}</p>
        {payload.map((pld: any, index: number) => (
          <div key={index} style={{ color: pld.color }} className="flex justify-between gap-4">
            <span>{pld.name}:</span>
            <span className="font-bold">{formatValue(pld.value)}</span>
          </div>
        ))}
      </div>
    );
  }

  return null;
};

export function LineChart({ title, data, yKeys, format = 'currency', stacked = false }: LineChartProps) {
  const ChartComponent = stacked ? AreaChart : RechartsLineChart;
  const LineComponent = stacked ? Area : Line;

  return (
    <ChartContainer title={title}>
      <ResponsiveContainer width="100%" height="100%">
        <ChartComponent data={data} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis
            dataKey="mes"
            tickFormatter={(tick) => formatMonth(tick)}
            tick={{ fontSize: 12 }}
            stroke="#6b7280"
          />
          <YAxis
            tickFormatter={(tick) => {
              switch (format) {
                case 'currency':
                  return formatCurrency(tick, { compact: true });
                case 'number':
                  return formatNumber(tick, { compact: true });
                case 'percentage':
                  return formatPercentage(tick);
                default:
                  return tick.toString();
              }
            }}
            tick={{ fontSize: 12 }}
            stroke="#6b7280"
            width={80}
          />
          <Tooltip content={<CustomTooltip format={format} />} />
          <Legend wrapperStyle={{ fontSize: '14px' }} />
          {yKeys.map((key, index) => (
            <LineComponent
              key={String(key)}
              type="monotone"
              dataKey={String(key)}
              name={String(key).replace(/_/g, ' ')}
              stroke={CHART_COLORS[index % CHART_COLORS.length]}
              fill={stacked ? CHART_COLORS[index % CHART_COLORS.length] : 'none'}
              fillOpacity={stacked ? 0.2 : 0}
              strokeWidth={2}
              dot={{ r: 2 }}
              activeDot={{ r: 6 }}
            />
          ))}
        </ChartComponent>
      </ResponsiveContainer>
    </ChartContainer>
  );
}
