// frontend/src/components/charts/Sparkline.tsx
import React from 'react';
import { Area, AreaChart, ResponsiveContainer } from 'recharts';

interface SparklineProps {
  data: any[];
  dataKey: string;
  strokeColor?: string;
  fillColor?: string;
  height?: number;
}

export const Sparkline = ({
  data,
  dataKey,
  strokeColor = '#10b981', // green-500
  fillColor = '#dcfce7',   // green-100
  height = 60,
}: SparklineProps) => {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <AreaChart
        data={data}
        margin={{
          top: 5,
          right: 0,
          left: 0,
          bottom: 5,
        }}
      >
        <defs>
          <linearGradient id={`sparkline-gradient-${dataKey}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor={fillColor} stopOpacity={0.4} />
            <stop offset="95%" stopColor={fillColor} stopOpacity={0} />
          </linearGradient>
        </defs>
        <Area
          type="monotone"
          dataKey={dataKey}
          stroke={strokeColor}
          strokeWidth={2}
          fillOpacity={1}
          fill={`url(#sparkline-gradient-${dataKey})`}
          isAnimationActive={false}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
};
