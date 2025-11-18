// frontend/src/pages/ResultsPage/components/InsightCard.tsx
import { Card } from '@/components/ui/Card';
import { Lightbulb, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react';
import React from 'react';

interface InsightCardProps {
  icon?: React.ReactNode;
  title: string;
  description: string;
  level: 'SUCCESS' | 'OPPORTUNITY' | 'WARNING';
}

const LEVEL_CONFIG = {
    SUCCESS: {
        icon: <CheckCircle className="w-6 h-6 text-green-500" />,
        style: "bg-green-50 border-green-200"
    },
    OPPORTUNITY: {
        icon: <Lightbulb className="w-6 h-6 text-blue-500" />,
        style: "bg-blue-50 border-blue-200"
    },
    WARNING: {
        icon: <AlertTriangle className="w-6 h-6 text-amber-500" />,
        style: "bg-amber-50 border-amber-200"
    }
}

export const InsightCard = ({ title, description, level }: InsightCardProps) => {
    const config = LEVEL_CONFIG[level] || LEVEL_CONFIG.OPPORTUNITY;

  return (
    <Card className={`p-4 flex items-start gap-4 ${config.style}`}>
      <div className="flex-shrink-0">
        {config.icon}
      </div>
      <div className="flex-grow">
        <h4 className="font-semibold text-slate-800">{title}</h4>
        <p className="text-sm text-slate-600">{description}</p>
      </div>
    </Card>
  );
};
