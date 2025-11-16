import {
  ComposedChart,
  Area,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  ReferenceDot,
} from 'recharts';
import { motion } from 'framer-motion'; // Added motion import
import { ChartContainer } from './ChartContainer';
import { formatCurrency, formatMonth } from '@/lib/utils/formatters';
import { CHART_COLORS } from '@/lib/theme/colors'; // Assuming this is needed for other charts or future expansion

type ChartData = {
  mes: number;
  mrr: number;
  cash: number;
  // Add other relevant data keys if they are part of the projectionData
  // For example, if 'Mês 13' is a string, the 'mes' type might need to be string | number
  // For now, assuming 'mes' is number and 'Mês 13' is a label.
};

interface FinancialProjectionChartProps {
  title: string;
  data: ChartData[];
}

export function FinancialProjectionChart({ title, data }: FinancialProjectionChartProps) {
  return (
    <ChartContainer title={title} height={400}>
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart data={data} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis
            dataKey="mes"
            tickFormatter={(tick) => formatMonth(tick)}
            tick={{ fontSize: 12 }}
            stroke="#6b7280"
          />
          <YAxis
            tickFormatter={(tick) => formatCurrency(tick, { compact: true })}
            tick={{ fontSize: 12 }}
            stroke="#6b7280"
            width={80}
          />
          <Legend wrapperStyle={{ fontSize: '14px' }} />

          {/* Área de MRR com gradiente premium */}
          <defs>
            <linearGradient id="mrrGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4}/>
              <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
            </linearGradient>
          </defs>
          
          {/* Linha de MRR */}
          <Area 
            type="monotone"
            dataKey="mrr"
            stroke="#4f46e5"
            strokeWidth={3}
            fill="url(#mrrGradient)"
            dot={{ r: 4, fill: "#4f46e5", stroke: "#ffffff", strokeWidth: 2 }}
            activeDot={{ r: 6 }}
          />
          
          {/* Linha de Caixa com efeito "cashflow" */}
          <Line
            type="monotone"
            dataKey="cash"
            stroke="#10b981"
            strokeWidth={2}
            strokeDasharray="4 4"
            dot={{ r: 3, fill: "#10b981" }}
          />
          
          {/* 🔥 DESTAQUE: Anotações que contam a história */}
          <ReferenceLine 
            x={13} // Changed from "Mês 13" to numeric 13
            stroke="#f59e0b"
            strokeDasharray="3 3"
            label={{ 
              value: "🏢 Contratação Dev + Tier 2", 
              position: "top",
              fill: "#f59e0b",
              fontSize: 12,
              fontWeight: 500
            }}
          />
          
          {/* Break-even point */}
          <ReferenceDot 
            x={13} // Changed from "Mês 13" to numeric 13
            y={0}
            r={8}
            fill="#10b981"
            stroke="#ffffff"
            strokeWidth={2}
            label={{ 
              value: "🎯 Break-even", 
              position: "top",
              fill: "#10b981"
            }}
          />

          {/* Projeção de MRR */}
          <ReferenceLine 
            x={24} // Added for "Mês 24" insight
            stroke="#8b5cf6"
            strokeDasharray="3 3"
            label={{ 
              value: "📈 Projeção de R$50k MRR", 
              position: "top",
              fill: "#8b5cf6",
              fontSize: 12,
              fontWeight: 500
            }}
          />
          
          {/* Tooltip rico */}
          <Tooltip 
            content={({ active, payload, label }) => {
              if (!active || !payload) return null;
              return (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  transition={{ duration: 0.15 }}
                  className="rounded-lg bg-white border border-slate-200 p-3 shadow-xl"
                >
                  <p className="text-sm font-semibold text-slate-900">{formatMonth(label, { format: 'long' })}</p>
                  <div className="mt-2 space-y-1">
                    {payload.map(item => (
                      <div key={item.name} className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full" style={{ backgroundColor: item.color }} />
                        <span className="text-sm text-slate-600">{item.name}:</span>
                        <span className="text-sm font-semibold">
                          {formatCurrency(item.value)}
                        </span>
                      </div>
                    ))}
                  </div>
                  {/* Insight contextual */}
                  <div className="mt-2 pt-2 border-t border-slate-100">
                    <p className="text-xs text-slate-500">
                      {label === 13 && '⚠️ Impacto do aumento de OPEX'}
                      {label === 24 && '📈 Projeção de R$50k MRR'}
                    </p>
                  </div>
                </motion.div>
              );
            }}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </ChartContainer>
  );
}
