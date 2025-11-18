// frontend/src/components/metrics/MetricCard.tsx
import { Card } from '@/components/ui/Card';
import { cn } from '@/lib/utils/cn';
import { ArrowUpRight, ArrowDownRight, Minus, TrendingUp, Users, PiggyBank, BarChart3, ChevronRight, AlertTriangle, HelpCircle, Search } from 'lucide-react';
import { motion } from 'framer-motion';
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/Sheet';
import { LineChart } from '../charts/LineChart';
import { useState } from 'react';
import { Button } from '../ui/Button';
import { Sparkline } from '../charts/Sparkline';

type MetricTrend = 'up' | 'down' | 'neutral' | 'warning';
type MetricId = 'mrr' | 'runway' | 'users' | 'ltv_cac' | 'break_even' | 'ltv' | 'cac' | 'arr' | 'ebitda' | 'churn' | 'gross_margin' | 'avg_cac';

interface MetricCardProps {
  id: MetricId;
  label: string;
  value: string;
  change?: string;
  trend?: MetricTrend;
  sparklineData?: { month: number; value: number }[];
  description?: string; // e.g., "vs mês ant." or "Meta: >3.0x"
  status?: {
    text: string;
    color: 'green' | 'amber' | 'red';
  };
  onInfoClick: (term: MetricId) => void;
}

const TREND_STYLES: Record<MetricTrend, { text: string; icon: React.ReactNode }> = {
    up: { text: 'text-green-700', icon: <TrendingUp size={14} /> },
    down: { text: 'text-red-700', icon: <ArrowDownRight size={14} /> },
    neutral: { text: 'text-slate-700', icon: <Minus size={14} /> },
    warning: { text: 'text-amber-700', icon: <AlertTriangle size={14} /> },
};

const STATUS_COLORS = {
  green: 'text-green-600',
  amber: 'text-amber-600',
  red: 'text-red-600',
}

export function MetricCard({ id, label, value, change, trend, sparklineData, description, status, onInfoClick }: MetricCardProps) {
  const trendStyle = trend ? TREND_STYLES[trend] : null;
  
  const handleInfoClick = (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent sheet from opening
    onInfoClick(id);
  };

  return (
    <Sheet>
      <SheetTrigger asChild>
        <motion.div
          whileHover={{ y: -4, boxShadow: '0 10px 20px rgba(0,0,0,0.07)' }}
          className="h-full"
        >
          <Card className="relative group h-full cursor-pointer transition-all shadow-sm hover:shadow-lg flex flex-col justify-between p-4 bg-white border border-slate-200 rounded-xl">
            {/* Header */}
            <div>
              <p className="text-sm font-semibold text-slate-800">{label}</p>
              <p className="text-3xl font-bold text-slate-900 mt-1 font-mono tabular-nums">{value}</p>
            </div>

            {/* Change and Description */}
            <div className="flex items-center text-sm mt-1">
              {trendStyle && (
                <div className={cn('inline-flex items-center gap-1 font-medium', trendStyle.text)}>
                  {trendStyle.icon}
                  <span>{change}</span>
                </div>
              )}
              {description && <span className="text-slate-500 ml-2">{description}</span>}
              {status && <span className={cn('font-semibold ml-2', STATUS_COLORS[status.color])}>{status.text}</span>}
            </div>

            {/* Sparkline */}
            <div className="mt-3 h-12 flex-grow">
              {sparklineData && sparklineData.length > 0 && (() => {
                const SPARKLINE_COLORS = {
                  up: { stroke: '#10b981', fill: '#dcfce7' },
                  down: { stroke: '#ef4444', fill: '#fef2f2' },
                  warning: { stroke: '#f59e0b', fill: '#fefce8' },
                  neutral: { stroke: '#64748b', fill: '#f1f5f9' },
                };
                const colors = SPARKLINE_COLORS[trend || 'neutral'];

                return (
                  <Sparkline 
                    data={sparklineData} 
                    dataKey="value"
                    strokeColor={colors.stroke}
                    fillColor={colors.fill}
                  />
                );
              })()}
            </div>

            {/* Footer Actions */}
            <div className="flex items-center justify-end gap-2 mt-2 border-t border-slate-100 pt-2 -mx-4 px-4">
              <button 
                onClick={handleInfoClick}
                className="flex items-center gap-1 text-xs text-slate-500 hover:text-blue-600 transition-colors"
              >
                <HelpCircle size={14} />
                <span>O que é?</span>
              </button>
              <button className="flex items-center gap-1 text-xs text-slate-500 hover:text-blue-600 transition-colors">
                <Search size={14} />
                <span>Analisar</span>
              </button>
            </div>
          </Card>
        </motion.div>
      </SheetTrigger>
      <SheetContent className="w-[600px] sm:max-w-[600px]">
        <SheetHeader>
          <SheetTitle className="text-2xl">{label}</SheetTitle>
          <SheetDescription>
            Análise detalhada e simulação de cenários para {label}.
          </SheetDescription>
        </SheetHeader>
        <div className="py-6">
          {/* Drill-down content will be enhanced later */}
          <p>Análise detalhada de {label} virá aqui.</p>
        </div>
      </SheetContent>
    </Sheet>
  );
}