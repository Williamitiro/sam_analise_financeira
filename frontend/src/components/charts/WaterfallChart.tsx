// frontend/src/components/charts/WaterfallChart.tsx
import React from 'react';
import Plot from 'react-plotly.js';
import { Card } from '../ui/Card';

interface WaterfallChartProps {
  title: string;
  data: {
    labels: string[];
    values: number[];
  };
}

export const WaterfallChart = ({ title, data }: WaterfallChartProps) => {
  const plotData = [
    {
      type: 'waterfall',
      orientation: 'v',
      measure: [
        'absolute', // Start
        ...data.values.slice(1, -1).map(() => 'relative'), // Deltas
        'total', // End
      ],
      x: data.labels,
      y: data.values,
      connector: {
        line: {
          color: 'rgb(63, 63, 63)',
        },
      },
      increasing: {
        marker: {
          color: '#22c55e', // green-500
        },
      },
      decreasing: {
        marker: {
          color: '#ef4444', // red-500
        },
      },
      totals: {
        marker: {
          color: '#3b82f6', // blue-500
        },
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
    xaxis: {
      type: 'category',
    },
    yaxis: {
      type: 'linear',
    },
    autosize: true,
    margin: {
      t: 50,
      b: 50,
      l: 50,
      r: 50,
    },
    showlegend: false,
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
