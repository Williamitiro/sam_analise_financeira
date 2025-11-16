/**
 * Utilitários de formatação - Padrão Brasileiro
 */

/**
 * Formata valor monetário em Real brasileiro
 */
export function formatCurrency(
  value: number,
  options?: {
    compact?: boolean;
    showSign?: boolean;
    decimals?: number;
  }
): string {
  const { compact = false, showSign = false, decimals = 0 } = options || {};

  // Formato compacto (K, M)
  if (compact) {
    if (Math.abs(value) >= 1_000_000) {
      return `R$ ${(value / 1_000_000).toFixed(1)}M`;
    }
    if (Math.abs(value) >= 1_000) {
      return `R$ ${(value / 1_000).toFixed(1)}K`;
    }
  }

  const formatted = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);

  if (showSign && value > 0) {
    return `+${formatted}`;
  }

  return formatted;
}

/**
 * Formata percentual
 */
export function formatPercentage(
  value: number,
  options?: {
    decimals?: number;
    showSign?: boolean;
    multiplier?: number;
  }
): string {
  const { decimals = 1, showSign = false, multiplier = 1 } = options || {};

  const finalValue = value * multiplier;
  const formatted = `${finalValue.toFixed(decimals)}%`;

  if (showSign && finalValue > 0) {
    return `+${formatted}`;
  }

  return formatted;
}

/**
 * Formata número genérico
 */
export function formatNumber(
  value: number,
  options?: {
    compact?: boolean;
    decimals?: number;
  }
): string {
  const { compact = false, decimals = 0 } = options || {};

  if (compact) {
    if (Math.abs(value) >= 1_000_000) {
      return `${(value / 1_000_000).toFixed(1)}M`;
    }
    if (Math.abs(value) >= 1_000) {
      return `${(value / 1_000).toFixed(1)}K`;
    }
  }

  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

/**
 * Formata mês
 */
export function formatMonth(
  monthNumber: number,
  options?: {
    format?: 'short' | 'long';
  }
): string {
  const { format = 'short' } = options || {};

  if (format === 'short') {
    return `Mês ${monthNumber}`;
  }

  const year = Math.floor((monthNumber - 1) / 12) + 1;
  const month = ((monthNumber - 1) % 12) + 1;

  const monthNames = [
    'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'
  ];

  return `${monthNames[month - 1]}/Ano ${year}`;
}

/**
 * Formata delta (variação)
 */
export function formatDelta(
  value: number,
  type: 'currency' | 'percentage' | 'number' = 'percentage'
): {
  formatted: string;
  color: string;
  icon: string;
  trend: 'up' | 'down' | 'neutral';
} {
  const isPositive = value > 0;
  const isNeutral = Math.abs(value) < 0.01;

  let formatted: string;
  switch (type) {
    case 'currency':
      formatted = formatCurrency(value, { showSign: true });
      break;
    case 'number':
      formatted = formatNumber(value, { decimals: 1 });
      break;
    default:
      formatted = formatPercentage(value, { showSign: true });
  }

  if (isNeutral) {
    return {
      formatted: '0%',
      color: 'text-gray-500',
      icon: '→',
      trend: 'neutral',
    };
  }

  return {
    formatted,
    color: isPositive ? 'text-success-600' : 'text-danger-600',
    icon: isPositive ? '↑' : '↓',
    trend: isPositive ? 'up' : 'down',
  };
}

/**
 * Formata duração em meses para texto legível
 */
export function formatDuration(months: number | string): string {
  if (typeof months === 'string') return months;

  if (months < 1) return 'Menos de 1 mês';
  if (months === 1) return '1 mês';
  if (months < 12) return `${months} meses`;
  
  const years = Math.floor(months / 12);
  const remainingMonths = months % 12;
  
  if (remainingMonths === 0) {
    return years === 1 ? '1 ano' : `${years} anos`;
  }
  
  return `${years} ano${years > 1 ? 's' : ''} e ${remainingMonths} mês${remainingMonths > 1 ? 'es' : ''}`;
}

/**
 * Calcula delta entre dois valores
 */
export function calculateDelta(current: number, previous: number): number {
  if (previous === 0) return 0;
  return ((current - previous) / previous) * 100;
}

/**
 * Calcula taxa de crescimento de um array
 */
export function calculateGrowthRate(values: number[]): number {
  if (values.length < 2) return 0;
  
  const first = values[0];
  const last = values[values.length - 1];
  
  if (first === 0) return 0;
  
  return ((last - first) / first) * 100;
}

/**
 * Formata valor com sufixo apropriado
 */
export function formatValueWithSuffix(
  value: number,
  type: 'currency' | 'percentage' | 'number'
): string {
  switch (type) {
    case 'currency':
      return formatCurrency(value, { compact: true });
    case 'percentage':
      return formatPercentage(value);
    default:
      return formatNumber(value, { compact: true });
  }
}
