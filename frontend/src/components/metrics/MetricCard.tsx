import { Card, CardContent } from '@/components/ui/Card';
import { cn } from '@/lib/utils/cn';
import { ArrowUpRight, ArrowDownRight, Minus, TrendingUp, Users, PiggyBank, BarChart3, ChevronRight, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/Sheet';
import { LineChart } from '../charts/LineChart';
import { useState } from 'react';
import { Slider } from '../ui/Slider';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input'; // Assuming an Input component exists or will be created

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

// ... (rest of the constants: ICONS, TREND_STYLES, COLOR_CLASSES)

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
    up: { text: 'text-success-700', icon: <TrendingUp size={12} /> },
    down: { text: 'text-danger-700', icon: <ArrowDownRight size={12} /> },
    neutral: { text: 'text-slate-700', icon: <Minus size={12} /> },
    warning: { text: 'text-warning-700', icon: <AlertTriangle size={12} /> },
};

const COLOR_CLASSES: Record<string, { bg: string; text: string; border: string }> = {
    blue: { bg: 'bg-blue-50', text: 'text-blue-600', border: 'hover:border-blue-200' },
    amber: { bg: 'bg-amber-50', text: 'text-amber-600', border: 'hover:border-amber-200' },
    green: { bg: 'bg-green-50', text: 'text-green-600', border: 'hover:border-green-200' },
    indigo: { bg: 'bg-indigo-50', text: 'text-indigo-600', border: 'hover:border-indigo-200' },
    purple: { bg: 'bg-purple-50', text: 'text-purple-600', border: 'hover:border-purple-200' },
    pink: { bg: 'bg-pink-50', text: 'text-pink-600', border: 'hover:border-pink-200' },
};


export function MetricCard({ id, label, value, change, trend, color, sparkline }: MetricCardProps) {
  const trendStyle = TREND_STYLES[trend];
  const colorStyle = COLOR_CLASSES[color];
  const [simulatedValue, setSimulatedValue] = useState<number | null>(null);

  const chartData = sparkline?.map((val, index) => ({ mes: index + 1, [label]: val })) || [];
  const originalValue = parseFloat(value.replace(/[^0-9.-]+/g,""));

  const handleApplySimulation = () => {
    console.log(`Applying simulation for ${label}: ${simulatedValue}`);
    // Here we would call a function from a store to update the global state
  };

  return (
    <Sheet>
      <SheetTrigger asChild>
        <motion.div
          whileHover={{ y: -3, boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }}
          className="h-full"
        >
          <Card className={cn("relative group p-5 h-full cursor-pointer transition-all", colorStyle.border)}>
            <div className={`absolute top-0 left-0 right-0 h-1 bg-${color}-500`} />
            
            <div className="flex items-start justify-between">
              <div>
                <p className="text-xs font-medium text-slate-500">{label}</p>
                <p className="text-2xl font-bold text-slate-900 mt-1">{value}</p>
              </div>
              <div className={cn('p-2 rounded-lg', colorStyle.bg, colorStyle.text)}>
                {ICONS[id]}
              </div>
            </div>

            <div className={cn('mt-3 inline-flex items-center gap-1 text-xs font-medium', trendStyle.text)}>
              {trendStyle.icon}
              {change}
            </div>

            <div className="absolute bottom-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <ChevronRight className="w-4 h-4 text-slate-400" />
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
          {/* Gráfico expandido */}
          {sparkline && sparkline.length > 0 ? (
            <LineChart 
              title={`Evolução de ${label}`}
              data={chartData}
              yKeys={[label]}
              format={id === 'mrr' || id === 'runway' ? 'currency' : 'number'}
            />
          ) : (
            <p>Não há dados históricos para esta métrica.</p>
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
