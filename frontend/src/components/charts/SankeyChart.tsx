// frontend/src/components/charts/SankeyChart.tsx
import React from 'react';
import Plot from 'react-plotly.js';
import { Card } from '../ui/Card';

interface SankeyNode {
    name: string;
}

interface SankeyLink {
    source: number;
    target: number;
    value: number;
}

interface SankeyChartProps {
  title: string;
  data: {
    nodes: SankeyNode[];
    links: SankeyLink[];
  };
}

export const SankeyChart = ({ title, data }: SankeyChartProps) => {
  const plotData = [
    {
      type: 'sankey',
      orientation: 'h',
      node: {
        pad: 15,
        thickness: 20,
        line: {
          color: 'black',
          width: 0.5,
        },
        label: data.nodes.map(n => n.name),
      },
      link: {
        source: data.links.map(l => l.source),
        target: data.links.map(l => l.target),
        value: data.links.map(l => l.value),
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
    font: {
      size: 10,
    },
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
