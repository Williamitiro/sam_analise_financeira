import { MetricCard } from './MetricCard';
import { formatCurrency, formatNumber, calculateDelta } from '@/lib/utils/formatters';
import { motion, AnimatePresence } from 'framer-motion';
import { KPIs, ProjectionData } from '@/types/api.types';

type MetricId = 'mrr' | 'runway' | 'users' | 'ltv_cac' | 'break_even' | 'ltv' | 'cac' | 'arr' | 'ebitda' | 'churn' | 'gross_margin' | 'avg_cac';

interface KPIGridProps {
  onInfoClick: (term: MetricId) => void;
  kpis: KPIs;
  data: ProjectionData;
}

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
    },
  },
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.4,
      ease: 'easeOut',
    },
  },
};

export function KPIGrid({ onInfoClick, kpis, data }: KPIGridProps) {
  const getDelta = (series: number[]): number => {
    if (!series || series.length < 2) return 0;
    const current = series[series.length - 1];
    const previous = series[series.length - 2];
    return calculateDelta(current, previous);
  };

  const formatSparkline = (series: number[]) => {
    return (series || []).map((val, index) => ({ month: index + 1, value: val }));
  };

  const metrics = [
    {
      id: 'mrr',
      label: 'MRR Final',
      value: formatCurrency(kpis.MRR_Final, { compact: true }),
      change: `${getDelta(data.MRR).toFixed(1)}%`,
      trend: getDelta(data.MRR) >= 0 ? 'up' : 'down',
      sparklineData: formatSparkline((data.MRR || []).slice(-12)),
      description: 'vs mês ant.',
    },
    {
      id: 'users',
      label: 'Usuários',
      value: formatNumber(kpis.Usuarios_Final, { compact: true }),
      change: `+${(data.Novos_Pagantes || []).slice(-1)[0] || 0}`,
      trend: getDelta(data.Usuarios_Finais) >= 0 ? 'up' : 'down',
      sparklineData: formatSparkline((data.Usuarios_Finais || []).slice(-12)),
      description: 'novos usuários',
    },
    {
      id: 'ltv_cac',
      label: 'LTV / CAC',
      value: `${kpis.LTV_CAC_Ratio_Final.toFixed(1)}x`,
      sparklineData: formatSparkline((data.LTV_CAC_Ratio || []).slice(-12)),
      status: {
        text: kpis.LTV_CAC_Ratio_Final > 3 ? 'Saudável' : 'Atenção',
        color: kpis.LTV_CAC_Ratio_Final > 3 ? 'green' : 'amber',
      },
      description: 'Meta: >3.0x',
    },
    {
        id: 'gross_margin',
        label: 'Margem Bruta',
        value: '84.3%', // Placeholder
        sparklineData: formatSparkline(((data.LTV_CAC_Ratio || [])).slice(-12).map(d => d * 15 + 10)), // Placeholder
        status: { text: 'Excelente', color: 'green' },
        description: 'Meta: >70%',
    },
    {
        id: 'avg_cac',
        label: 'CAC Médio',
        value: formatCurrency(kpis.CAC_Medio_Periodo),
        change: '-5.2%', // Placeholder
        trend: 'down',
        sparklineData: formatSparkline((data.CAC || []).slice(-12)),
        description: 'vs mês ant.',
    },
    {
        id: 'churn',
        label: 'Churn Mensal',
        value: '4.0%', // Placeholder
        change: '+0.2pp', // Placeholder
        trend: 'warning',
        sparklineData: formatSparkline(((data.Taxa_Churn || [])).slice(-12).map(c => c*100)),
        description: 'Pontos percentuais',
    },
    {
        id: 'ebitda',
        label: 'EBITDA',
        value: formatCurrency(2700, {compact: true}), // Placeholder
        change: '+15%', // Placeholder
        trend: 'up',
        sparklineData: formatSparkline((data.Lucro_Operacional_EBITDA || []).slice(-12)),
        description: 'vs mês ant.',
    },
    {
        id: 'arr',
        label: 'ARR',
        value: formatCurrency(kpis.MRR_Final * 12, { compact: true }),
        change: `${getDelta(data.MRR).toFixed(1)}%`,
        trend: 'up',
        sparklineData: formatSparkline(((data.MRR || [])).slice(-12).map(m => m * 12)),
        description: 'MRR x 12',
    },
  ];

  return (
    <AnimatePresence>
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {metrics.map((metric) => (
          <motion.div key={metric.id} variants={itemVariants}>
            <MetricCard {...metric} onInfoClick={onInfoClick} />
          </motion.div>
        ))}
      </motion.div>
    </AnimatePresence>
  );
}
