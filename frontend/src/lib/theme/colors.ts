/**
 * Sistema de Cores - SAM Financial Model
 * Paleta consistente para toda a aplicação
 */

export const COLORS = {
  // Cores para gráficos (ordem de prioridade)
  chart: [
    '#2E86AB', // Primary
    '#06A77D', // Success
    '#4895EF', // Info
    '#F77F00', // Warning
    '#D62828', // Danger
    '#66B1C8', // Primary Light
    '#36C3A2', // Success Light
    '#87BDF9', // Info Light
    '#FFA733', // Warning Light
    '#E05050', // Danger Light
  ],

  // Cores para categorias de custo
  cost: {
    pessoal: '#8338EC',     // Roxo
    infra: '#3A86FF',       // Azul
    marketing: '#FB5607',   // Laranja
    ferramentas: '#FFBE0B', // Amarelo
    servicos: '#06A77D',    // Verde
    outros: '#6B7280',      // Cinza
  },

  // Cores para status de alertas
  alert: {
    critical: '#D62828',
    warning: '#F77F00',
    success: '#06A77D',
    info: '#4895EF',
  },

  // Cores para tendências
  trend: {
    positive: '#06A77D',
    negative: '#D62828',
    neutral: '#6B7280',
  },

  // Cores para zonas de caixa
  cashZones: {
    safe: '#06A77D',      // Verde - Zona segura
    caution: '#F77F00',   // Laranja - Zona de atenção
    danger: '#D62828',    // Vermelho - Zona de perigo
  },
};

// Níveis de alerta para componentes
export type AlertLevel = 'CRITICAL' | 'WARNING' | 'INFO' | 'SUCCESS';

export const ALERT_COLORS: Record<AlertLevel, { bg: string; text: string; border: string; icon: string }> = {
  CRITICAL: {
    bg: 'bg-danger-50',
    text: 'text-danger-800',
    border: 'border-danger-200',
    icon: '🔴',
  },
  WARNING: {
    bg: 'bg-warning-50',
    text: 'text-warning-800',
    border: 'border-warning-200',
    icon: '🟡',
  },
  INFO: {
    bg: 'bg-info-50',
    text: 'text-info-800',
    border: 'border-info-200',
    icon: '🔵',
  },
  SUCCESS: {
    bg: 'bg-success-50',
    text: 'text-success-800',
    border: 'border-success-200',
    icon: '🟢',
  },
};

// Exporta cores para uso em gráficos Recharts/Plotly
export const CHART_COLORS = COLORS.chart;
export const COST_COLORS = COLORS.cost;
