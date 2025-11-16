import { Card } from '@/components/ui/Card';
import { cn } from '@/lib/utils/cn';
import { ArrowUpRight, ArrowDownRight, Minus, TrendingUp, Users, PiggyBank, BarChart3, ChevronRight, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/Sheet';
import { LineChart } from '../charts/LineChart';
import { useState } from 'react';
import { Slider } from '../ui/Slider';
import { Button } from '../ui/Button';

type MetricTrend = 'up' | 'down' | 'neutral' | 'warning';
type MetricId = 'mrr' | 'runway' | 'users' | 'ltv_cac' | 'break_even' | 'ltv' | 'cac';

interface MetricCardProps {
  id: MetricId;
  label: string;
  value: string;
  change: string;
  trend: MetricTrend;
  color: 'blue' | 'amber' | 'green' | 'indigo' | 'purple' | 'pink';
  sparkline?: number[];
}

const ICONS: Record<MetricId, React.ReactNode> = {
    mrr: <BarChart3 size={20} />,
    runway: <PiggyBank size={20} />,
    users: <Users size={20} />,
    ltv_cac: <TrendingUp size={20} />,
    break_even: <PiggyBank size={20} />,
    ltv: <TrendingUp size={20} />,
    cac: <TrendingUp size={20} />,
};

const TREND_STYLES: Record<MetricTrend, { text: string; icon: React.ReactNode }> = {
    up: { text: 'text-green-700', icon: <TrendingUp size={12} /> },
    down: { text: 'text-red-700', icon: <ArrowDownRight size={12} /> },
    neutral: { text: 'text-slate-700', icon: <Minus size={12} /> },
    warning: { text: 'text-amber-700', icon: <AlertTriangle size={12} /> },
};

const COLOR_CLASSES: Record<MetricId, { bg: string; text: string; border: string }> = {
    mrr: { bg: 'bg-blue-50', text: 'text-blue-600', border: 'hover:border-blue-200' },
    runway: { bg: 'bg-amber-50', text: 'text-amber-600', border: 'hover:border-amber-200' },
    users: { bg: 'bg-purple-50', text: 'text-purple-600', border: 'hover:border-purple-200' },
    ltv_cac: { bg: 'bg-green-50', text: 'text-green-600', border: 'hover:border-green-200' },
    break_even: { bg: 'bg-indigo-50', text: 'text-indigo-600', border: 'hover:border-indigo-200' },
    ltv: { bg: 'bg-pink-50', text: 'text-pink-600', border: 'hover:border-pink-200' },
    cac: { bg: 'bg-red-50', text: 'text-red-600', border: 'hover:border-red-200' },
};

export function MetricCard({ id, label, value, change, trend, color, sparkline }: MetricCardProps) {
  const trendStyle = TREND_STYLES[trend];
  const colorStyle = COLOR_CLASSES[id];
  const [simulatedValue, setSimulatedValue] = useState<number | null>(null);

  const chartData = sparkline?.map((val, index) => ({ mes: index + 1, [label]: val })) || [];
  const originalValue = parseFloat(value.replace(/[^0-9.-]+/g,""));

  const handleApplySimulation = () => {
    console.log(`Applying simulation for ${label}: ${simulatedValue}`);
    // Here we would call a function from a store to update the global state
  };

  // Classe dinâmica para a barra superior - solução com safelist
  const topBarClass = {
    blue: 'bg-blue-500',
    amber: 'bg-amber-500',
    green: 'bg-green-500',
    indigo: 'bg-indigo-500',
    purple: 'bg-purple-500',
    pink: 'bg-pink-500',
  }[color];

  return (
    <Sheet>
      <SheetTrigger asChild>
        <motion.div
          whileHover={{ 
            y: -4, 
            boxShadow: '0 8px 24px rgba(0,0,0,0.08)',
            transition: { type: "spring", stiffness: 300 }
          }}
          className="h-full"
        >
          <Card className={cn(
            "relative group h-28 cursor-pointer transition-all shadow-sm hover:shadow-md",
            colorStyle.border
          )}>
            <div className={`absolute top-0 left-0 right-0 h-1 ${topBarClass}`} />
            
            <div className="p-4 h-full flex flex-col justify-between">
              <div className="flex items-start justify-between">
                {/* Metric Icon and Label */}
                <div className="flex items-center gap-2 flex-1">
                  <div className={cn('p-2 rounded-lg', colorStyle.bg, colorStyle.text)}>
                    {ICONS[id]}
                  </div>
                  <div>
                    <p className="text-xs font-medium text-slate-500 uppercase tracking-wide">{label}</p>
                    <p className="text-xl font-bold text-slate-900 mt-1 font-mono tabular-nums">{value}</p>
                  </div>
                </div>
                {/* Trend Icon in top right */}
                <div className={cn('p-1 rounded-full', colorStyle.bg, trendStyle.text)}>
                  {trendStyle.icon}
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className={cn('inline-flex items-center gap-1 text-xs font-medium', trendStyle.text)}>
                  {change}
                </div>
                
                <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <ChevronRight className="w-4 h-4 text-slate-400" />
                </div>
              </div>
            </div>
          </Card>
        </motion.div>
      </SheetTrigger>
      <SheetContent className="w-[600px] sm:max-w-[600px]">
        <SheetHeader>
          <SheetTitle className="text-2xl">{label}</SheetTitle>
          <SheetDescription>
            Análise detalhada e simulação de cenários.
          </SheetDescription>
        </SheetHeader>
        
        <div className="py-6 space-y-6">
          {/* Mostrar valor simulado */}
          {simulatedValue !== null && (
            <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
              <span className="text-sm font-medium">Valor Simulado: </span>
              <span className="text-sm font-bold text-blue-700">
                {id === 'mrr' || id === 'runway' 
                  ? `R$ ${simulatedValue.toLocaleString('pt-BR')}`
                  : simulatedValue.toLocaleString()}
              </span>
            </div>
          )}

          {/* Gráfico expandido */}
          {sparkline && sparkline.length > 0 ? (
            <LineChart 
              title={`Evolução de ${label}`}
              data={chartData}
              yKeys={[label]}
              format={id === 'mrr' || id === 'runway' ? 'currency' : 'number'}
            />
          ) : (
            <p className="text-sm text-slate-500">Não há dados históricos para esta métrica.</p>
          )}

          {/* Seção de Simulação */}
          <div className="p-4 rounded-lg bg-slate-50 border border-slate-200">
            <h3 className="text-sm font-semibold text-slate-900 mb-3">Simulador de Cenário</h3>
            <Slider
              defaultValue={[originalValue]}
              max={originalValue * 2}
              step={id === 'mrr' ? 1000 : 1}
              onValueChange={(v) => setSimulatedValue(v[0])}
            />
            <div className="flex justify-between text-xs text-slate-500 mt-2">
              <span>{originalValue / 2}</span>
              <span>{originalValue * 2}</span>
            </div>
            <div className="flex gap-2 mt-4">
              <Button 
                onClick={handleApplySimulation}
                disabled={simulatedValue === null}
                className="flex-1"
              >
                Aplicar Simulação
              </Button>
              <Button 
                variant="outline" 
                onClick={() => setSimulatedValue(null)}
                disabled={simulatedValue === null}
              >
                Resetar
              </Button>
            </div>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}
