// frontend/src/pages/ResultsPage/components/HeroCard.tsx
import { Card } from '@/components/ui/Card';
import React from 'react';

interface HeroCardProps {
  title: string;
  value: string;
  description?: string;
  children?: React.ReactNode;
  className?: string;
}

export const HeroCard = ({ title, value, description, children, className }: HeroCardProps) => {
  return (
    <Card className={`p-4 flex flex-col justify-between ${className}`}>
      <div>
        <h3 className="text-sm font-semibold text-slate-600 uppercase tracking-wider">{title}</h3>
        <p className="text-3xl font-bold text-slate-900 mt-1">{value}</p>
        {description && <p className="text-sm text-slate-500 mt-1">{description}</p>}
      </div>
      {children}
    </Card>
  );
};
