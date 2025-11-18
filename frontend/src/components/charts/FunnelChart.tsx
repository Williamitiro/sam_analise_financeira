// frontend/src/components/charts/FunnelChart.tsx
import React from 'react';
import Plot from 'react-plotly.js';
import { Card } from '../ui/Card';

interface FunnelChartProps {
  title: string;
  data: {
    labels: string[];
    values: number[];
  };
}

export const FunnelChart = ({ title, data }: FunnelChartProps) => {
  const plotData = [
    {
      type: 'funnel',
      y: data.labels,
      x: data.values,
      textposition: 'inside',
      textinfo: 'value+percent initial',
      connector: { 
        line: { 
          color: "royalblue", 
          dash: "dot", 
          width: 2 
        } 
      },
      marker: {
        color: ['#1e3a8a', '#1d4ed8', '#2563eb', '#3b82f6', '#60a5fa'], // blue shades
      },
    },
  ];

  const layout = {
    title: {
      text: title,
      font: {
        size: 18,
        color: '#1e293b', // slate-800
      },
    },
    margin: { l: 100, r: 50, t: 50, b: 50 },
  };

  return (
    <Card className="p-4">
      <Plot
        data={plotData as any}
        layout={layout}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
        config={{ responsive: true }}
      />
    </Card>
  );
};
