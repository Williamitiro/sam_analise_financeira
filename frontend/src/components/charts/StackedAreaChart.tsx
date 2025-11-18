// frontend/src/components/charts/StackedAreaChart.tsx
import { formatCurrency } from '@/lib/utils/formatters';
import React from 'react';
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis, Legend } from 'recharts';
import { Card } from '../ui/Card';

interface StackedAreaChartProps {
  title: string;
  data: any[];
  xKey: string;
  yKeys: { key: string; color: string }[];
}

const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="p-3 bg-white/90 border border-slate-300 rounded-lg shadow-lg backdrop-blur-sm">
          <p className="font-bold text-slate-800">{`Mês ${label}`}</p>
          {payload.map((pld: any) => (
            <div key={pld.dataKey} style={{ color: pld.color }} className="flex justify-between gap-4 items-center">
              <span className="font-medium">{pld.name}:</span>
              <span className="font-mono font-semibold">{formatCurrency(pld.value)}</span>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

export const StackedAreaChart = ({ title, data, xKey, yKeys }: StackedAreaChartProps) => {
  return (
    <Card className="p-4 h-[450px] flex flex-col">
        <h3 className="text-lg font-semibold text-slate-800 mb-4">{title}</h3>
        <div className="flex-grow">
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart
                data={data}
                margin={{
                    top: 10,
                    right: 30,
                    left: 20,
                    bottom: 20,
                }}
                >
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey={xKey} stroke="#475569" fontSize={12} />
                <YAxis stroke="#475569" fontSize={12} tickFormatter={(value) => formatCurrency(value, { compact: true })} />
                <Tooltip content={<CustomTooltip />} />
                <Legend iconSize={12} wrapperStyle={{ fontSize: '14px', paddingTop: '20px' }} />
                {yKeys.map(({ key, color }) => (
                    <Area
                    key={key}
                    type="monotone"
                    dataKey={key}
                    stackId="1"
                    stroke={color}
                    fill={color}
                    fillOpacity={0.7}
                    name={key.replace(/_/g, ' ')}
                    />
                ))}
                </AreaChart>
            </ResponsiveContainer>
        </div>
    </Card>
  );
};
