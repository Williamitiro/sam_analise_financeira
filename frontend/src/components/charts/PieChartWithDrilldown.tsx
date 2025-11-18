// frontend/src/components/charts/PieChartWithDrilldown.tsx
import React, { useState } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { ArrowLeft } from 'lucide-react';
import { formatCurrency } from '@/lib/utils/formatters';

interface PieChartData {
  [key: string]: number;
}

interface PieChartWithDrilldownProps {
  title: string;
  data: PieChartData;
  breakdown?: {
    [key: string]: PieChartData;
  };
}

const COLORS = ['#0ea5e9', '#3b82f6', '#6366f1', '#8b5cf6', '#a855f7', '#d946ef'];

const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index, name }: any) => {
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
        <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" className="text-xs font-bold">
            {`${(percent * 100).toFixed(0)}%`}
        </text>
    );
};

const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="p-2 bg-white/90 border border-slate-300 rounded-lg shadow-lg">
          <p className="font-semibold">{`${payload[0].name}: ${formatCurrency(payload[0].value)}`}</p>
        </div>
      );
    }
    return null;
  };

export const PieChartWithDrilldown = ({ title, data, breakdown }: PieChartWithDrilldownProps) => {
  const [drilldownLevel, setDrilldownLevel] = useState<string | null>(null);

  const mainData = Object.entries(data).map(([name, value]) => ({ name, value }));
  const drilldownData = drilldownLevel && breakdown?.[drilldownLevel] 
    ? Object.entries(breakdown[drilldownLevel]).map(([name, value]) => ({ name, value }))
    : [];

  const currentData = drilldownLevel ? drilldownData : mainData;
  const currentTitle = drilldownLevel ? `${title}: ${drilldownLevel}` : title;

  const handlePieClick = (entry: any) => {
    if (breakdown && breakdown[entry.name]) {
      setDrilldownLevel(entry.name);
    }
  };

  return (
    <Card className="p-4 h-[450px] flex flex-col">
        <div className="flex items-center justify-between mb-4">
            {drilldownLevel && (
                <Button variant="ghost" size="sm" onClick={() => setDrilldownLevel(null)}>
                    <ArrowLeft className="mr-2 h-4 w-4" />
                    Voltar
                </Button>
            )}
            <h3 className="text-lg font-semibold text-slate-800">{currentTitle}</h3>
            <div />
        </div>
      
        <div className="flex-grow">
            <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                    <Pie
                        data={currentData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={renderCustomizedLabel}
                        outerRadius={120}
                        fill="#8884d8"
                        dataKey="value"
                        onClick={drilldownLevel ? undefined : handlePieClick}
                        cursor={drilldownLevel ? 'default' : 'pointer'}
                    >
                        {currentData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                    </Pie>
                    <Tooltip content={<CustomTooltip />} />
                    <Legend iconSize={12} wrapperStyle={{ fontSize: '14px' }} />
                </PieChart>
            </ResponsiveContainer>
        </div>
    </Card>
  );
};
