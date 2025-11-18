// frontend/src/pages/ResultsPage/components/HeroSection.tsx
import { KPIs } from '@/types/api.types';
import React from 'react';
import { HeroCard } from './HeroCard';
import { formatCurrency, formatNumber } from '@/lib/utils/formatters';
import { Sparkline } from '@/components/charts/Sparkline';

interface HeroSectionProps {
    kpis: KPIs;
}

export const HeroSection = ({ kpis }: HeroSectionProps) => {
  // Dummy data for sparklines - this should be replaced with real data later
  const dummySparkline = [
    { month: 1, value: 10 }, { month: 2, value: 20 }, { month: 3, value: 15 },
    { month: 4, value: 30 }, { month: 5, value: 25 }, { month: 6, value: 40 },
  ];

  return (
    <div className="p-4 rounded-lg">
      <h2 className="text-lg font-semibold text-slate-800 mb-4">🚨 Status Executivo</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <HeroCard
          title="💀 Vale da Morte"
          value={formatCurrency(kpis.Vale_da_Morte_Valor)}
          description={`Mês ${kpis.Vale_da_Morte_Month}`}
          className="border-l-4 border-red-500"
        >
            <div className="h-12 mt-2">
                <Sparkline data={dummySparkline} dataKey="value" strokeColor="#ef4444" fillColor="#fef2f2" />
            </div>
        </HeroCard>
        <HeroCard
          title="🎯 Break-Even"
          value={`Mês ${kpis.Breakeven_Month}`}
          description={`MRR: ${formatCurrency(kpis.Breakeven_MRR)}`}
          className="border-l-4 border-green-500"
        >
            <div className="h-12 mt-2">
                <Sparkline data={dummySparkline.map(d => ({...d, value: d.value * 2}))} dataKey="value" strokeColor="#22c55e" fillColor="#f0fdf4" />
            </div>
        </HeroCard>
        <HeroCard
          title="💰 Resultado (Mês 12)"
          value={formatCurrency(kpis.Lucro_Prejuizo_Mes_12)}
          description={kpis.Lucro_Prejuizo_Mes_12 > 0 ? '💚 Lucro' : '🔴 Prejuízo'}
          className={`border-l-4 ${kpis.Lucro_Prejuizo_Mes_12 > 0 ? 'border-green-500' : 'border-red-500'}`}
        >
            <div className="h-12 mt-2">
                <Sparkline data={dummySparkline.map(d => ({...d, value: d.value * 1.5}))} dataKey="value" strokeColor="#3b82f6" fillColor="#eff6ff" />
            </div>
        </HeroCard>
        <HeroCard
          title="⏱️ Runway"
          value={`${kpis.Runway_Meses} meses`}
          description={kpis.Runway_Meses > 12 ? '✅ Seguro' : '🟡 Atenção'}
          className={`border-l-4 ${kpis.Runway_Meses > 12 ? 'border-green-500' : 'border-amber-500'}`}
        >
            <div className="h-12 mt-2">
                <Sparkline data={dummySparkline.map(d => ({...d, value: 60 - d.value}))} dataKey="value" strokeColor="#6366f1" fillColor="#eef2ff" />
            </div>
        </HeroCard>
      </div>
    </div>
  );
};
