import { useMockProjection } from '@/features/projection/hooks/useMockProjection';
import { MetricCard } from './MetricCard';
import { formatCurrency, formatNumber, calculateDelta } from '@/lib/utils/formatters';
import { motion, AnimatePresence } from 'framer-motion';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
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

export function KPIGrid() {
  const { kpis, data } = useMockProjection();

  if (!kpis || !data) {
    return null;
  }

  const getDelta = (series: number[]): number => {
    if (series.length < 2) return 0;
    const current = series[series.length - 1];
    const previous = series[series.length - 2];
    return calculateDelta(current, previous);
  };

  const metrics = [
    {
      id: 'mrr',
      label: 'MRR Final',
      value: formatCurrency(kpis.MRR_Final, { compact: true }),
      change: `${getDelta(data.MRR).toFixed(1)}%`,
      trend: getDelta(data.MRR) >= 0 ? 'up' : 'down',
      sparkline: data.MRR,
      color: 'indigo',
    },
    {
      id: 'users',
      label: 'Usuários Finais',
      value: formatNumber(kpis.Usuarios_Final, { compact: true }),
      change: `${getDelta(data.Usuarios_Finais).toFixed(1)}%`,
      trend: getDelta(data.Usuarios_Finais) >= 0 ? 'up' : 'down',
      sparkline: data.Usuarios_Finais,
      color: 'blue',
    },
    {
      id: 'ltv_cac',
      label: 'LTV / CAC Ratio',
      value: `${kpis.LTV_CAC_Ratio_Final.toFixed(1)}x`,
      change: kpis.LTV_CAC_Ratio_Final > 3 ? 'Saudável' : 'Atenção',
      trend: kpis.LTV_CAC_Ratio_Final > 3 ? 'up' : 'warning',
      sparkline: data.LTV_CAC_Ratio,
      color: 'green',
    },
    {
      id: 'runway',
      label: 'Runway',
      value: typeof kpis.Runway_Meses === 'number' ? `${kpis.Runway_Meses} meses` : '>= 36 meses',
      change: 'com aportes',
      trend: 'neutral',
      sparkline: data.Saldo_Caixa,
      color: 'amber',
    },
  ];

  return (
    <AnimatePresence>
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {metrics.map((metric) => (
          <motion.div key={metric.id} variants={itemVariants}>
            <MetricCard {...metric} />
          </motion.div>
        ))}
      </motion.div>
    </AnimatePresence>
  );
}
