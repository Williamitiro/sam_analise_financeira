/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        slate: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
        primary: {
          500: '#3b82f6', // Azul confiança
        },
        success: {
          50: '#f0fdf4',
          100: '#dcfce7',
          500: '#10b981', // Caixa positivo
          700: '#047857',
        },
        warning: {
          50: '#fffbeb',
          500: '#f59e0b', // Atenção runway
          700: '#b45309',
        },
        danger: {
          50: '#fef2f2',
          500: '#ef4444', // Crítico
          700: '#b91c1c',
        },
        mrr: '#6366f1',      // Roxo premium
        cash: '#10b981',     // Verde dinheiro
        opex: '#f97316',     // Laranja custos
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      borderRadius: {
        DEFAULT: '0.5rem',
        md: '0.5rem',
        lg: '0.75rem',
        xl: '1rem',
        '2xl': '1.5rem',
      },
      animation: {
        'shimmer': 'shimmer 2s ease-in-out infinite',
      },
      keyframes: {
        shimmer: {
          '0%, 100%': { backgroundPosition: '-200% 0' },
          '50%': { backgroundPosition: '200% 0' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}