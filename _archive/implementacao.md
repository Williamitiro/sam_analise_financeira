# 🚀 INICIANDO IMPLEMENTAÇÃO - PADRÃO OURO DA INDÚSTRIA

---

# 📦 PARTE 1: SETUP INICIAL DO PROJETO

## **PASSO 1: Criar Projeto e Instalar Dependências**

```bash
# 1. Criar projeto com Vite + React + TypeScript
npm create vite@latest sam-financial-frontend -- --template react-ts

# 2. Entrar no diretório
cd sam-financial-frontend

# 3. Instalar dependências principais
npm install

# 4. Instalar bibliotecas de estado e formulários
npm install zustand@^4.5.0 immer@^10.0.3

# 5. Instalar React Hook Form + Validação
npm install react-hook-form@^7.49.0 @hookform/resolvers@^3.3.0 zod@^3.22.0

# 6. Instalar TanStack Query
npm install @tanstack/react-query@^5.17.0 @tanstack/react-query-devtools@^5.17.0

# 7. Instalar bibliotecas de gráficos
npm install recharts@^2.10.0 plotly.js-basic-dist@^2.27.0 react-plotly.js@^2.6.0

# 8. Instalar Axios para API
npm install axios@^1.6.0

# 9. Instalar Radix UI (headless components)
npm install @radix-ui/react-dialog@^1.0.5 @radix-ui/react-tabs@^1.0.4 @radix-ui/react-select@^2.0.0 @radix-ui/react-tooltip@^1.0.7 @radix-ui/react-dropdown-menu@^2.0.6

# 10. Instalar Tailwind CSS + Plugins
npm install -D tailwindcss@^3.4.0 postcss@^8.4.32 autoprefixer@^10.4.16
npm install -D @tailwindcss/forms@^0.5.7 @tailwindcss/typography@^0.5.10

# 11. Instalar utilitários UI
npm install clsx@^2.1.0 tailwind-merge@^2.2.0 class-variance-authority@^0.7.0

# 12. Instalar animações e ícones
npm install framer-motion@^10.18.0 lucide-react@^0.303.0

# 13. Instalar toast notifications
npm install sonner@^1.3.0

# 14. Instalar manipulação de datas
npm install date-fns@^3.0.0

# 15. Instalar React Router
npm install react-router-dom@^6.20.0

# 16. Instalar tipos TypeScript
npm install -D @types/node@^20.10.0

# 17. Inicializar Tailwind
npx tailwindcss init -p
```

---

## **PASSO 2: Configurar Tailwind CSS**---

```bash
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Cores Primárias
        primary: {
          50: '#E6F2F7',
          100: '#CCE5EF',
          200: '#99CBD0',
          300: '#66B1C8',
          400: '#4A9DBD',
          500: '#2E86AB',
          600: '#256B8A',
          700: '#1C5068',
          800: '#133546',
          900: '#0A1A23',
        },
        // Sucesso (Receita, Lucro, Positivo)
        success: {
          50: '#E6F9F4',
          100: '#CCF3E9',
          200: '#99E7D3',
          300: '#66DBBD',
          400: '#36C3A2',
          500: '#06A77D',
          600: '#058664',
          700: '#04644B',
          800: '#034332',
          900: '#012119',
        },
        // Perigo (Custos, Perdas, Negativo)
        danger: {
          50: '#FBE9E9',
          100: '#F7D3D3',
          200: '#EFA7A7',
          300: '#E77B7B',
          400: '#E05050',
          500: '#D62828',
          600: '#AB2020',
          700: '#801818',
          800: '#551010',
          900: '#2B0808',
        },
        // Aviso (Alertas, Atenção)
        warning: {
          50: '#FFF4E6',
          100: '#FFE9CC',
          200: '#FFD399',
          300: '#FFBD66',
          400: '#FFA733',
          500: '#F77F00',
          600: '#C66600',
          700: '#944C00',
          800: '#633300',
          900: '#311900',
        },
        // Info (Neutro, Informação)
        info: {
          50: '#EBF4FE',
          100: '#D7E9FD',
          200: '#AFD3FB',
          300: '#87BDF9',
          400: '#5FA7F7',
          500: '#4895EF',
          600: '#3A77BF',
          700: '#2B598F',
          800: '#1D3B60',
          900: '#0E1E30',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
      },
      fontSize: {
        xs: ['0.75rem', { lineHeight: '1rem' }],
        sm: ['0.875rem', { lineHeight: '1.25rem' }],
        base: ['1rem', { lineHeight: '1.5rem' }],
        lg: ['1.125rem', { lineHeight: '1.75rem' }],
        xl: ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
      },
      borderRadius: {
        sm: '0.25rem',
        DEFAULT: '0.5rem',
        md: '0.5rem',
        lg: '0.75rem',
        xl: '1rem',
      },
      boxShadow: {
        sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        DEFAULT: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)',
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)',
        xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-in': 'slideIn 0.3s ease-in-out',
        'scale-in': 'scaleIn 0.2s ease-in-out',
        'spin-slow': 'spin 3s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideIn: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```



## **PASSO 3: Configurar Estilos Globais**---


```bash

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  * {
    @apply border-gray-200;
  }
  
  body {
    @apply bg-gray-50 text-gray-900 antialiased;
  }
  
  /* Scrollbar personalizado */
  ::-webkit-scrollbar {
    @apply w-2 h-2;
  }
  
  ::-webkit-scrollbar-track {
    @apply bg-gray-100;
  }
  
  ::-webkit-scrollbar-thumb {
    @apply bg-gray-300 rounded-full;
  }
  
  ::-webkit-scrollbar-thumb:hover {
    @apply bg-gray-400;
  }
}

@layer components {
  /* Container responsivo */
  .container-custom {
    @apply mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl;
  }
  
  /* Card base */
  .card {
    @apply bg-white rounded-lg border border-gray-200 shadow-sm;
  }
  
  /* Botão base */
  .btn {
    @apply inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none;
  }
  
  .btn-primary {
    @apply bg-primary-500 text-white hover:bg-primary-600;
  }
  
  .btn-secondary {
    @apply bg-gray-100 text-gray-900 hover:bg-gray-200;
  }
  
  .btn-ghost {
    @apply hover:bg-gray-100 text-gray-700;
  }
  
  /* Input base */
  .input {
    @apply block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm;
  }
  
  /* Badge base */
  .badge {
    @apply inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium;
  }
  
  .badge-success {
    @apply bg-success-100 text-success-800;
  }
  
  .badge-danger {
    @apply bg-danger-100 text-danger-800;
  }
  
  .badge-warning {
    @apply bg-warning-100 text-warning-800;
  }
  
  .badge-info {
    @apply bg-info-100 text-info-800;
  }
}

@layer utilities {
  /* Utilitários customizados */
  .text-balance {
    text-wrap: balance;
  }
  
  .animate-skeleton {
    @apply animate-pulse bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 bg-[length:200%_100%];
    animation: shimmer 1.5s ease-in-out infinite;
  }
  
  @keyframes shimmer {
    0% {
      background-position: -200% 0;
    }
    100% {
      background-position: 200% 0;
    }
  }
  
  /* Hide scrollbar */
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
  
  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
}

/* Toaster personalizado (Sonner) */
:root {
  --sonner-toast-background: white;
  --sonner-toast-border: #e5e7eb;
  --sonner-toast-color: #111827;
}

[data-sonner-toast][data-type="success"] {
  --sonner-toast-background: #f0fdf4;
  --sonner-toast-border: #86efac;
  --sonner-toast-color: #166534;
}

[data-sonner-toast][data-type="error"] {
  --sonner-toast-background: #fef2f2;
  --sonner-toast-border: #fca5a5;
  --sonner-toast-color: #991b1b;
}

[data-sonner-toast][data-type="warning"] {
  --sonner-toast-background: #fffbeb;
  --sonner-toast-border: #fcd34d;
  --sonner-toast-color: #92400e;
}

```


## **PASSO 4: Configurar Vite**---


```bash

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  
  server: {
    port: 5173,
    host: true,
    open: true,
  },
  
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          // Separa vendors grandes
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'chart-vendor': ['recharts', 'plotly.js-basic-dist', 'react-plotly.js'],
          'form-vendor': ['react-hook-form', '@hookform/resolvers', 'zod'],
          'query-vendor': ['@tanstack/react-query'],
          'ui-vendor': [
            '@radix-ui/react-dialog',
            '@radix-ui/react-tabs',
            '@radix-ui/react-select',
            '@radix-ui/react-tooltip',
          ],
        },
      },
    },
    chunkSizeWarningLimit: 1000,
  },
  
  optimizeDeps: {
    include: [
      'react',
      'react-dom',
      'react-router-dom',
      'recharts',
      'zustand',
      'react-hook-form',
      '@tanstack/react-query',
    ],
  },
});

```


## **PASSO 5: Configurar TypeScript**---


```bash

{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    
    /* Path mapping */
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

## **PASSO 6: Criar Estrutura de Pastas**

```bash
# Criar estrutura completa de pastas
mkdir -p src/app
mkdir -p src/pages/ResultsPage/dashboards
mkdir -p src/components/ui
mkdir -p src/components/layout
mkdir -p src/components/forms
mkdir -p src/components/metrics
mkdir -p src/components/charts
mkdir -p src/components/tables
mkdir -p src/components/drill-down
mkdir -p src/components/insights
mkdir -p src/components/filters
mkdir -p src/components/loading
mkdir -p src/features/projection/hooks
mkdir -p src/features/projection/stores
mkdir -p src/features/projection/types
mkdir -p src/lib/api
mkdir -p src/lib/utils
mkdir -p src/lib/theme
mkdir -p src/types
mkdir -p src/hooks
```

---

# 📦 PARTE 2: MOCK DATA E TIPOS

## **PASSO 7: Criar Tipos TypeScript da API**---


```bash

/**
 * Tipos da API - Alinhados com o backend FastAPI
 */

// Dados da projeção mês a mês
export interface ProjectionData {
  mes: number[];
  
  // Funil de Aquisição
  Usuarios_Iniciais: number[];
  Visitantes: number[];
  Novos_Trials: number[];
  Novos_Pagantes: number[];
  Usuarios_Perdidos: number[];
  Usuarios_Finais: number[];
  
  // Taxas de Conversão
  Taxa_Conv_Trial: number[];
  Taxa_Conv_Pagante: number[];
  Taxa_Conv_Geral: number[];
  
  // Receita
  MRR: number[];
  ARR: number[];
  ARPU: number[];
  Receita_Total: number[];
  
  // COGS Detalhado
  Custo_IA: number[];
  Impostos: number[];
  Taxas_Pagamento: number[];
  Comissoes_Afiliados: number[];
  COGS_Total: number[];
  
  // Margens
  Lucro_Bruto: number[];
  Margem_Bruta_Pct: number[];
  
  // OPEX Detalhado
  Custo_Infra: number[];
  Tier_Infra: number[];
  Custo_Marketing: number[];
  Fase_Marketing: number[];
  Salario_Fundador: number[];
  Custo_Pessoal_CLT: number[];
  Custo_Pessoal_PJ: number[];
  Custo_Escritorio: number[];
  Custo_Ferramentas: number[];
  Custo_Servicos_Profissionais: number[];
  Custo_Depreciacao: number[];
  Custo_Despesas_Anuais: number[];
  OPEX_Total: number[];
  
  // Resultado
  EBITDA: number[];
  Resultado_Operacional: number[];
  
  // Fluxo de Caixa
  Aportes: number[];
  Fluxo_Caixa: number[];
  Saldo_Caixa: number[];
  
  // Métricas de Análise
  CAC_Mensal: number[];
  LTV: number[];
  LTV_CAC_Ratio: number[];
  Payback_Meses: number[];
  Churn_Absoluto: number[];
}

// KPIs principais
export interface KPIs {
  Break_Even_Mes: number | null;
  Payback_Investimento_Mes: number | null;
  Vale_da_Morte_Minimo_Caixa: number;
  Vale_da_Morte_Mes: number;
  Runway_Meses: number | string;
  LTV_Final: number;
  CAC_Medio_Periodo: number;
  LTV_CAC_Ratio_Final: number;
  CAC_Payback_Meses_Config: number;
  MRR_Ano1: number;
  MRR_Ano2: number;
  MRR_Ano3: number;
  Usuarios_Ano1: number;
  Usuarios_Ano2: number;
  Usuarios_Ano3: number;
  Saldo_Caixa_Final: number;
  MRR_Final: number;
  Usuarios_Final: number;
  eventos: Event[];
}

// Insight automático
export interface Insight {
  level: 'CRITICAL' | 'WARNING' | 'INFO' | 'SUCCESS';
  category: 'caixa' | 'crescimento' | 'custos' | 'unit_economics';
  title: string;
  description: string;
  value?: number;
  action?: string;
  impact?: string;
}

// Evento no timeline
export interface Event {
  mes: number;
  tipo: string;
  descricao: string;
  valor: number;
}

// Response completa da API
export interface ProjectionResponse {
  projecao_df: ProjectionData;
  kpis: KPIs;
  insights?: Insight[];
  eventos?: Event[];
}

// Tipos auxiliares para charts
export interface ChartDataPoint {
  mes: number;
  [key: string]: number | string;
}

// Tipo para waterfall
export interface WaterfallItem {
  label: string;
  value: number;
  type: 'increase' | 'decrease' | 'total';
}

// Tipo para Sankey
export interface SankeyNode {
  label: string;
  color?: string;
}

export interface SankeyLink {
  source: number;
  target: number;
  value: number;
  color?: string;
}

export interface SankeyData {
  nodes: SankeyNode[];
  links: SankeyLink[];
}

// Tipo para cohorts
export interface CohortData {
  cohort: string;
  retention: Record<string, number>;
}


```

## **PASSO 8: Criar Mock Data Completo**---


```bash

import type { ProjectionResponse } from '@/types/api.types';

/**
 * Mock Data - Simula resposta da API /projecao/
 * Baseado em projeção real do SAM Financial Model
 */

// Gera array de 36 meses com crescimento exponencial
const generateGrowthArray = (initial: number, growthRate: number, months: number = 36): number[] => {
  return Array.from({ length: months }, (_, i) => 
    Math.round(initial * Math.pow(1 + growthRate, i))
  );
};

// Gera array com valores decrescentes (churn)
const generateDecayArray = (rate: number, months: number = 36): number[] => {
  return Array.from({ length: months }, () => rate);
};

export const MOCK_PROJECTION_DATA: ProjectionResponse = {
  projecao_df: {
    mes: Array.from({ length: 36 }, (_, i) => i + 1),
    
    // Funil de Aquisição
    Usuarios_Iniciais: generateGrowthArray(0, 0.12, 36),
    Visitantes: generateGrowthArray(1000, 0.15, 36),
    Novos_Trials: generateGrowthArray(50, 0.15, 36),
    Novos_Pagantes: generateGrowthArray(8, 0.15, 36),
    Usuarios_Perdidos: generateGrowthArray(0, 0.12, 36).map((v, i) => Math.round(v * 0.04)),
    Usuarios_Finais: generateGrowthArray(8, 0.12, 36),
    
    // Taxas de Conversão (%)
    Taxa_Conv_Trial: Array(36).fill(5.0),
    Taxa_Conv_Pagante: Array(36).fill(15.0),
    Taxa_Conv_Geral: Array(36).fill(0.75),
    
    // Receita
    MRR: generateGrowthArray(776, 0.12, 36),
    ARR: generateGrowthArray(9312, 0.12, 36),
    ARPU: Array(36).fill(97),
    Receita_Total: generateGrowthArray(776, 0.12, 36),
    
    // COGS Detalhado
    Custo_IA: generateGrowthArray(40, 0.12, 36),
    Impostos: generateGrowthArray(47, 0.12, 36),
    Taxas_Pagamento: generateGrowthArray(35, 0.12, 36),
    Comissoes_Afiliados: Array(36).fill(0),
    COGS_Total: generateGrowthArray(122, 0.12, 36),
    
    // Margens
    Lucro_Bruto: generateGrowthArray(654, 0.12, 36),
    Margem_Bruta_Pct: Array(36).fill(84.3),
    
    // OPEX Detalhado
    Custo_Infra: [
      ...Array(6).fill(209),    // Tier 1 meses 1-6
      ...Array(6).fill(209),    // Tier 1 meses 7-12
      ...Array(12).fill(5559),  // Tier 2 meses 13-24
      ...Array(12).fill(5859),  // Tier 2+ meses 25-36
    ],
    Tier_Infra: [
      ...Array(12).fill(1),     // Tier 1
      ...Array(12).fill(2),     // Tier 2
      ...Array(12).fill(2),     // Tier 2
    ],
    Custo_Marketing: [
      ...Array(3).fill(500),    // Fase 1: validação
      ...Array(9).fill(150),    // Fase 2: % lucro
      ...Array(12).fill(400),   // Fase 2: crescendo
      ...Array(12).fill(800),   // Fase 2: escala
    ],
    Fase_Marketing: [
      ...Array(3).fill(1),
      ...Array(33).fill(2),
    ],
    Salario_Fundador: [
      ...Array(6).fill(0),      // Sem salário
      ...Array(6).fill(3000),   // Salário mínimo
      ...Array(24).fill(5000),  // Salário pleno
    ],
    Custo_Pessoal_CLT: [
      ...Array(12).fill(0),     // Sem contratações
      ...Array(12).fill(13440), // Dev Backend
      ...Array(12).fill(22240), // Dev + CS Manager
    ],
    Custo_Pessoal_PJ: [
      ...Array(6).fill(0),
      ...Array(30).fill(3000),  // Designer
    ],
    Custo_Escritorio: Array(36).fill(0), // Remoto
    Custo_Ferramentas: Array(36).fill(400),
    Custo_Servicos_Profissionais: Array(36).fill(500),
    Custo_Depreciacao: Array(36).fill(333),
    Custo_Despesas_Anuais: Array(36).fill(3.33),
    OPEX_Total: [
      ...Array(6).fill(1442),
      ...Array(6).fill(4442),
      ...Array(12).fill(19876),
      ...Array(12).fill(29876),
    ],
    
    // Resultado
    EBITDA: generateGrowthArray(-788, 0.15, 36).map((v, i) => 
      i < 6 ? -788 : i < 12 ? -1500 : i < 24 ? 200 : 1500
    ),
    Resultado_Operacional: generateGrowthArray(-1121, 0.15, 36).map((v, i) => 
      i < 6 ? -1121 : i < 12 ? -1833 : i < 24 ? -133 : 1167
    ),
    
    // Fluxo de Caixa
    Aportes: [
      ...Array(12).fill(1800),  // Aportes primeiros 12 meses
      ...Array(24).fill(0),
    ],
    Fluxo_Caixa: generateGrowthArray(679, 0.10, 36).map((v, i) => 
      i < 12 ? 679 - (i * 50) : v
    ),
    Saldo_Caixa: [
      -8000, -7321, -6642, -5963, -5284, -4605, // Vale da morte
      -3926, -3247, -2568, -1889, -1210, -531,
      148, 827, 1506, 2185, 2864, 3543,         // Recuperação
      4222, 4901, 5580, 6259, 6938, 7617,
      8296, 8975, 9654, 10333, 11012, 11691,
      12370, 13049, 13728, 14407, 15086, 15765,
    ],
    
    // Métricas de Análise
    CAC_Mensal: generateGrowthArray(62.5, 0.02, 36),
    LTV: Array(36).fill(2425),
    LTV_CAC_Ratio: Array(36).fill(4.6),
    Payback_Meses: Array(36).fill(5.8),
    Churn_Absoluto: generateGrowthArray(0, 0.12, 36).map((v, i) => Math.round(v * 0.04)),
  },
  
  kpis: {
    Break_Even_Mes: 13,
    Payback_Investimento_Mes: 13,
    Vale_da_Morte_Minimo_Caixa: -8000,
    Vale_da_Morte_Mes: 1,
    Runway_Meses: '>= 36',
    LTV_Final: 2425,
    CAC_Medio_Periodo: 450,
    LTV_CAC_Ratio_Final: 5.4,
    CAC_Payback_Meses_Config: 5.8,
    MRR_Ano1: 7760,
    MRR_Ano2: 24320,
    MRR_Ano3: 76160,
    Usuarios_Ano1: 80,
    Usuarios_Ano2: 251,
    Usuarios_Ano3: 785,
    Saldo_Caixa_Final: 15765,
    MRR_Final: 76160,
    Usuarios_Final: 785,
    eventos: [
      { mes: 1, tipo: 'INICIO', descricao: 'Início da operação', valor: -8000 },
      { mes: 6, tipo: 'CONTRATACAO', descricao: 'Designer PJ contratado', valor: 3000 },
      { mes: 7, tipo: 'SALARIO', descricao: 'Fundador começa salário mínimo', valor: 3000 },
      { mes: 12, tipo: 'TRANSICAO', descricao: 'Fim dos aportes mensais', valor: 0 },
      { mes: 13, tipo: 'MILESTONE', descricao: 'Break-even atingido', valor: 148 },
      { mes: 13, tipo: 'CONTRATACAO', descricao: 'Dev Backend contratado', valor: 13440 },
      { mes: 13, tipo: 'INFRA', descricao: 'Migração para Tier 2', valor: 5559 },
      { mes: 18, tipo: 'CONTRATACAO', descricao: 'Community Manager contratado', valor: 8800 },
      { mes: 24, tipo: 'MILESTONE', descricao: 'MRR passa de R$50k', valor: 50000 },
    ],
  },
  
  insights: [
    {
      level: 'CRITICAL',
      category: 'caixa',
      title: 'Caixa inicial negativo',
      description: 'Investimento inicial de R$8.000 (CAPEX). Runway de 12 meses com aportes.',
      value: -8000,
      action: 'Monitorar fluxo de caixa mensalmente',
      impact: 'Break-even previsto para mês 13',
    },
    {
      level: 'SUCCESS',
      category: 'crescimento',
      title: 'Crescimento consistente',
      description: 'MRR crescendo 12% ao mês em média',
      value: 0.12,
      action: 'Manter estratégia de marketing atual',
      impact: 'Atingirá R$50k MRR no mês 24',
    },
    {
      level: 'SUCCESS',
      category: 'unit_economics',
      title: 'Unit Economics saudável',
      description: 'LTV/CAC de 5.4x (acima do mínimo de 3x)',
      value: 5.4,
      action: 'Considerar aumentar investimento em marketing',
      impact: 'Margem para acelerar crescimento',
    },
    {
      level: 'WARNING',
      category: 'custos',
      title: 'OPEX sobe significativamente no mês 13',
      description: 'Contratação de Dev Backend + migração para Tier 2',
      value: 19876,
      action: 'Garantir que MRR suporte o aumento de custos',
      impact: 'OPEX passa de R$4k para R$20k',
    },
    {
      level: 'INFO',
      category: 'caixa',
      title: 'Runway estendido',
      description: 'Com aportes mensais, runway > 36 meses',
      action: 'Planejamento de captação pode ser postergado',
      impact: 'Maior flexibilidade operacional',
    },
  ],
};

```

---


# 🚀 CONTINUANDO - PARTE 3: UTILITÁRIOS E STORES

---

## **PASSO 9: Utilitários de Formatação**---

```bash

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
```

## **PASSO 10: Utilitário de Classes CSS (cn)**---

```bash

import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Utilitário para merge de classes Tailwind
 * Combina clsx + tailwind-merge para evitar conflitos de classes
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

```



## **PASSO 11: Tema e Cores**---


```bash

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
```

## **PASSO 12: Store Zustand - Projection**---

```bash

import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import type { ProjectionData, KPIs, Insight } from '@/types/api.types';

/**
 * Store de Projeção - Zustand
 * Gerencia dados da projeção, KPIs e insights
 */

interface ProjectionState {
  // Dados
  data: ProjectionData | null;
  kpis: KPIs | null;
  insights: Insight[] | null;
  
  // Filtros globais
  filters: {
    periodStart: number;
    periodEnd: number;
    granularity: 'monthly' | 'quarterly' | 'yearly';
  };
  
  // UI State
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setProjectionData: (data: ProjectionData) => void;
  setKPIs: (kpis: KPIs) => void;
  setInsights: (insights: Insight[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  
  // Filtros
  updateFilters: (filters: Partial<ProjectionState['filters']>) => void;
  resetFilters: () => void;
  
  // Reset
  reset: () => void;
}

const initialState = {
  data: null,
  kpis: null,
  insights: null,
  filters: {
    periodStart: 1,
    periodEnd: 36,
    granularity: 'monthly' as const,
  },
  isLoading: false,
  error: null,
};

export const useProjectionStore = create<ProjectionState>()(
  devtools(
    (set) => ({
      ...initialState,
      
      setProjectionData: (data) => set({ data, error: null }),
      
      setKPIs: (kpis) => set({ kpis }),
      
      setInsights: (insights) => set({ insights }),
      
      setLoading: (isLoading) => set({ isLoading }),
      
      setError: (error) => set({ error, isLoading: false }),
      
      updateFilters: (newFilters) =>
        set((state) => ({
          filters: { ...state.filters, ...newFilters },
        })),
      
      resetFilters: () =>
        set({
          filters: initialState.filters,
        }),
      
      reset: () => set(initialState),
    }),
    { name: 'ProjectionStore' }
  )
);

// Seletores otimizados (evitam re-renders desnecessários)
export const selectProjectionData = (state: ProjectionState) => state.data;
export const selectKPIs = (state: ProjectionState) => state.kpis;
export const selectInsights = (state: ProjectionState) => state.insights;
export const selectFilters = (state: ProjectionState) => state.filters;
export const selectIsLoading = (state: ProjectionState) => state.isLoading;
export const selectError = (state: ProjectionState) => state.error;
```


## **PASSO 13: Hook para Mock Data**---


```BASH
import { useEffect } from 'react';
import { useProjectionStore } from '../stores/projectionStore';
import { MOCK_PROJECTION_DATA } from '@/lib/api/mockData';

/**
 * Hook para carregar mock data
 * Simula chamada de API com delay
 */
export function useMockProjection() {
  const {
    data,
    kpis,
    insights,
    isLoading,
    error,
    setProjectionData,
    setKPIs,
    setInsights,
    setLoading,
    setError,
  } = useProjectionStore();

  useEffect(() => {
    // Se já tem dados, não recarrega
    if (data) return;

    // Simula loading
    setLoading(true);

    // Simula delay de rede (1 segundo)
    const timer = setTimeout(() => {
      try {
        setProjectionData(MOCK_PROJECTION_DATA.projecao_df);
        setKPIs(MOCK_PROJECTION_DATA.kpis);
        setInsights(MOCK_PROJECTION_DATA.insights || []);
        setLoading(false);
      } catch (err) {
        setError('Erro ao carregar dados mock');
        setLoading(false);
      }
    }, 1000);

    return () => clearTimeout(timer);
  }, [data, setProjectionData, setKPIs, setInsights, setLoading, setError]);

  return {
    data,
    kpis,
    insights,
    isLoading,
    error,
  };
}

```

## **PASSO 14: Hook para Dados Filtrados**---

```bash

import { useMemo } from 'react';
import { useProjectionStore, selectProjectionData, selectFilters } from '../stores/projectionStore';
import type { ProjectionData } from '@/types/api.types';

/**
 * Hook para obter dados filtrados
 * Aplica filtros de período e granularidade
 */
export function useFilteredData() {
  const data = useProjectionStore(selectProjectionData);
  const filters = useProjectionStore(selectFilters);

  const filteredData = useMemo(() => {
    if (!data) return null;

    // Aplica filtro de período
    const startIndex = filters.periodStart - 1;
    const endIndex = filters.periodEnd;

    const filtered: ProjectionData = {} as ProjectionData;

    // Filtra cada array
    Object.keys(data).forEach((key) => {
      const dataKey = key as keyof ProjectionData;
      filtered[dataKey] = data[dataKey].slice(startIndex, endIndex) as any;
    });

    // Aplica granularidade (se necessário)
    if (filters.granularity !== 'monthly') {
      return applyGranularity(filtered, filters.granularity);
    }

    return filtered;
  }, [data, filters]);

  return filteredData;
}

/**
 * Aplica granularidade (trimestral ou anual)
 */
function applyGranularity(
  data: ProjectionData,
  granularity: 'quarterly' | 'yearly'
): ProjectionData {
  const groupSize = granularity === 'quarterly' ? 3 : 12;
  const aggregated: ProjectionData = {} as ProjectionData;

  Object.keys(data).forEach((key) => {
    const dataKey = key as keyof ProjectionData;
    const values = data[dataKey];
    const aggregatedValues: number[] = [];

    for (let i = 0; i < values.length; i += groupSize) {
      const chunk = values.slice(i, i + groupSize);

      // Para 'mes', pega o primeiro valor do grupo
      if (key === 'mes') {
        aggregatedValues.push(chunk[0]);
      }
      // Para percentuais e médias, calcula média
      else if (
        key.includes('Taxa_') ||
        key.includes('Margem_') ||
        key.includes('Pct')
      ) {
        const avg = chunk.reduce((sum, val) => sum + val, 0) / chunk.length;
        aggregatedValues.push(avg);
      }
      // Para valores absolutos, soma
      else {
        const sum = chunk.reduce((sum, val) => sum + val, 0);
        aggregatedValues.push(sum);
      }
    }

    aggregated[dataKey] = aggregatedValues as any;
  });

  return aggregated;
}

/**
 * Hook para converter dados em formato de gráfico
 */
export function useChartData(keys: string[]) {
  const data = useFilteredData();

  const chartData = useMemo(() => {
    if (!data) return [];

    return data.mes.map((mes, index) => {
      const point: Record<string, number> = { mes };

      keys.forEach((key) => {
        const dataKey = key as keyof ProjectionData;
        point[key] = data[dataKey][index];
      });

      return point;
    });
  }, [data, keys]);

  return chartData;
}
```

## **PASSO 15: Componentes UI Base - Button**---


```bash
import { ButtonHTMLAttributes, forwardRef } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils/cn';

/**
 * Variantes do Button usando CVA (Class Variance Authority)
 * Padrão da indústria para gerenciamento de variantes
 */
const buttonVariants = cva(
  // Base styles
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none',
  {
    variants: {
      variant: {
        primary: 'bg-primary-500 text-white hover:bg-primary-600 active:bg-primary-700',
        secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200 active:bg-gray-300',
        ghost: 'hover:bg-gray-100 text-gray-700 active:bg-gray-200',
        danger: 'bg-danger-500 text-white hover:bg-danger-600 active:bg-danger-700',
        success: 'bg-success-500 text-white hover:bg-success-600 active:bg-success-700',
        outline: 'border border-gray-300 bg-transparent hover:bg-gray-50 text-gray-700',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4 text-base',
        lg: 'h-12 px-6 text-lg',
      },
      fullWidth: {
        true: 'w-full',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant,
      size,
      fullWidth,
      isLoading,
      leftIcon,
      rightIcon,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    return (
      <button
        ref={ref}
        className={cn(buttonVariants({ variant, size, fullWidth, className }))}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading ? (
          <>
            <svg
              className="animate-spin -ml-1 mr-2 h-4 w-4"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            Carregando...
          </>
        ) : (
          <>
            {leftIcon && <span className="mr-2">{leftIcon}</span>}
            {children}
            {rightIcon && <span className="ml-2">{rightIcon}</span>}
          </>
        )}
      </button>
    );
  }
);

Button.displayName = 'Button';
```

## **PASSO 16: Componente UI Base - Card**---


```bash
import { HTMLAttributes, forwardRef } from 'react';
import { cn } from '@/lib/utils/cn';

/**
 * Componente Card - Container base para conteúdo
 */

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  hover?: boolean;
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, hover = false, padding = 'md', children, ...props }, ref) => {
    const paddingClasses = {
      none: '',
      sm: 'p-4',
      md: 'p-6',
      lg: 'p-8',
    };

    return (
      <div
        ref={ref}
        className={cn(
          'bg-white rounded-lg border border-gray-200 shadow-sm',
          hover && 'hover:shadow-md transition-shadow cursor-pointer',
          paddingClasses[padding],
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = 'Card';

/**
 * Card Header
 */
export interface CardHeaderProps extends HTMLAttributes<HTMLDivElement> {
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
}

export const CardHeader = forwardRef<HTMLDivElement, CardHeaderProps>(
  ({ className, title, subtitle, action, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn('flex items-start justify-between mb-4', className)}
        {...props}
      >
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          {subtitle && (
            <p className="text-sm text-gray-500 mt-1">{subtitle}</p>
          )}
        </div>
        {action && <div className="ml-4">{action}</div>}
      </div>
    );
  }
);

CardHeader.displayName = 'CardHeader';

/**
 * Card Content
 */
export const CardContent = forwardRef<
  HTMLDivElement,
  HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => {
  return <div ref={ref} className={cn('', className)} {...props} />;
});

CardContent.displayName = 'CardContent';

/**
 * Card Footer
 */
export const CardFooter = forwardRef<
  HTMLDivElement,
  HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={cn('mt-4 pt-4 border-t border-gray-200', className)}
      {...props}
    />
  );
});

CardFooter.displayName = 'CardFooter';

```


# 🚀 CONTINUANDO - PARTE 4: LOADING & LAYOUT

---

## **PASSO 17: Componentes de Loading**---

```bash
import { Card } from '@/components/ui/Card';
import { cn } from '@/lib/utils/cn';

/**
 * Loading Spinner
 */
export function LoadingSpinner({ 
  size = 'md',
  fullScreen = false 
}: { 
  size?: 'sm' | 'md' | 'lg';
  fullScreen?: boolean;
}) {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
  };

  const spinner = (
    <div
      className={cn(
        'animate-spin rounded-full border-b-2 border-primary-500',
        sizeClasses[size]
      )}
    />
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-gray-50/80 backdrop-blur-sm z-50">
        <div className="text-center">
          {spinner}
          <p className="mt-4 text-sm text-gray-600">Carregando...</p>
        </div>
      </div>
    );
  }

  return spinner;
}

/**
 * Skeleton base
 */
export function Skeleton({ 
  className 
}: { 
  className?: string 
}) {
  return (
    <div
      className={cn(
        'animate-skeleton rounded bg-gray-200',
        className
      )}
    />
  );
}

/**
 * Skeleton para Métrica (KPI Card)
 */
export function MetricSkeleton() {
  return (
    <Card>
      <div className="space-y-3">
        <Skeleton className="h-4 w-24" />
        <Skeleton className="h-8 w-32" />
        <Skeleton className="h-3 w-16" />
      </div>
    </Card>
  );
}

/**
 * Skeleton para Gráfico
 */
export function ChartSkeleton({ height = 400 }: { height?: number }) {
  return (
    <Card>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <Skeleton className="h-6 w-48" />
          <Skeleton className="h-8 w-24" />
        </div>
        <Skeleton className="w-full" style={{ height: `${height}px` }} />
      </div>
    </Card>
  );
}

/**
 * Skeleton para Tabela
 */
export function TableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <Card>
      <div className="space-y-4">
        <Skeleton className="h-6 w-48" />
        <div className="space-y-2">
          {Array.from({ length: rows }).map((_, i) => (
            <div key={i} className="flex gap-4">
              <Skeleton className="h-10 flex-1" />
              <Skeleton className="h-10 flex-1" />
              <Skeleton className="h-10 flex-1" />
              <Skeleton className="h-10 flex-1" />
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}

/**
 * Skeleton para Dashboard completo
 */
export function DashboardSkeleton() {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* KPIs Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricSkeleton />
        <MetricSkeleton />
        <MetricSkeleton />
        <MetricSkeleton />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartSkeleton />
        <ChartSkeleton />
      </div>

      <ChartSkeleton height={300} />
    </div>
  );
}

/**
 * Empty State
 */
export function EmptyState({
  icon = '📊',
  title,
  description,
  action,
}: {
  icon?: string;
  title: string;
  description: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="text-6xl mb-4">{icon}</div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-500 mb-6 max-w-sm">{description}</p>
      {action && (
        <button
          onClick={action.onClick}
          className="btn btn-primary"
        >
          {action.label}
        </button>
      )}
    </div>
  );
}

/**
 * Error State
 */
export function ErrorState({
  title = 'Algo deu errado',
  description,
  onRetry,
}: {
  title?: string;
  description: string;
  onRetry?: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="text-6xl mb-4">⚠️</div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-500 mb-6 max-w-sm">{description}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="btn btn-secondary"
        >
          Tentar Novamente
        </button>
      )}
    </div>
  );
}
```

## **PASSO 18: Componente de Badge**---

```bash

import { HTMLAttributes, forwardRef } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils/cn';

const badgeVariants = cva(
  'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors',
  {
    variants: {
      variant: {
        success: 'bg-success-100 text-success-800 border border-success-200',
        danger: 'bg-danger-100 text-danger-800 border border-danger-200',
        warning: 'bg-warning-100 text-warning-800 border border-warning-200',
        info: 'bg-info-100 text-info-800 border border-info-200',
        default: 'bg-gray-100 text-gray-800 border border-gray-200',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

export interface BadgeProps
  extends HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {
  icon?: React.ReactNode;
}

export const Badge = forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className, variant, icon, children, ...props }, ref) => {
    return (
      <span
        ref={ref}
        className={cn(badgeVariants({ variant }), className)}
        {...props}
      >
        {icon && <span className="mr-1">{icon}</span>}
        {children}
      </span>
    );
  }
);

Badge.displayName = 'Badge';

```

## **PASSO 19: Layout - Sidebar**---

```bash
import { useState } from 'react';
import { 
  LayoutDashboard, 
  DollarSign, 
  TrendingDown, 
  Wallet,
  Users,
  Megaphone,
  Target,
  Activity,
  GitCompare,
  Table,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';
import { cn } from '@/lib/utils/cn';

interface NavItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  badge?: string;
}

const NAV_ITEMS: NavItem[] = [
  { id: 'overview', label: 'Visão Geral', icon: <LayoutDashboard size={20} /> },
  { id: 'revenue', label: 'Receita', icon: <DollarSign size={20} /> },
  { id: 'costs', label: 'Custos', icon: <TrendingDown size={20} /> },
  { id: 'cash', label: 'Caixa', icon: <Wallet size={20} />, badge: 'Em breve' },
  { id: 'team', label: 'Equipe', icon: <Users size={20} />, badge: 'Em breve' },
  { id: 'marketing', label: 'Marketing', icon: <Megaphone size={20} />, badge: 'Em breve' },
  { id: 'unit-economics', label: 'Unit Economics', icon: <Target size={20} />, badge: 'Em breve' },
  { id: 'sensitivity', label: 'Sensibilidade', icon: <Activity size={20} />, badge: 'Em breve' },
  { id: 'scenarios', label: 'Cenários', icon: <GitCompare size={20} />, badge: 'Em breve' },
  { id: 'tables', label: 'Explorador de Dados', icon: <Table size={20} />, badge: 'Em breve' },
];

interface SidebarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export function Sidebar({ activeTab, onTabChange }: SidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <aside
      className={cn(
        'fixed left-0 top-0 h-screen bg-white border-r border-gray-200 transition-all duration-300 z-40',
        isCollapsed ? 'w-16' : 'w-64'
      )}
    >
      {/* Header */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-gray-200">
        {!isCollapsed && (
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">S</span>
            </div>
            <div>
              <h1 className="font-bold text-gray-900">SAM</h1>
              <p className="text-xs text-gray-500">Financial Model</p>
            </div>
          </div>
        )}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="p-1.5 hover:bg-gray-100 rounded-md transition-colors"
          aria-label={isCollapsed ? 'Expandir sidebar' : 'Recolher sidebar'}
        >
          {isCollapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
        </button>
      </div>

      {/* Navigation */}
      <nav className="p-2 space-y-1 overflow-y-auto h-[calc(100vh-4rem)]">
        {NAV_ITEMS.map((item) => {
          const isActive = activeTab === item.id;
          const isDisabled = !!item.badge;

          return (
            <button
              key={item.id}
              onClick={() => !isDisabled && onTabChange(item.id)}
              disabled={isDisabled}
              className={cn(
                'w-full flex items-center gap-3 px-3 py-2.5 rounded-md transition-colors text-left',
                isActive && 'bg-primary-50 text-primary-700',
                !isActive && !isDisabled && 'text-gray-700 hover:bg-gray-50',
                isDisabled && 'text-gray-400 cursor-not-allowed opacity-60'
              )}
              title={isCollapsed ? item.label : undefined}
            >
              <span className={cn(isActive && 'text-primary-600')}>
                {item.icon}
              </span>
              
              {!isCollapsed && (
                <>
                  <span className="flex-1 font-medium text-sm">{item.label}</span>
                  {item.badge && (
                    <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                      {item.badge}
                    </span>
                  )}
                </>
              )}
            </button>
          );
        })}
      </nav>

      {/* Footer (se não colapsado) */}
      {!isCollapsed && (
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200 bg-gray-50">
          <div className="text-xs text-gray-500 text-center">
            <p className="font-semibold">SAM v4.0</p>
            <p className="mt-1">Dados simulados (Mock)</p>
          </div>
        </div>
      )}
    </aside>
  );
}   


```


## **PASSO 20: Layout - Header**---

```bash

import { Filter, Download } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';

interface HeaderProps {
  title: string;
  subtitle?: string;
  showFilters?: boolean;
  onFilterClick?: () => void;
  onExport?: () => void;
}

export function Header({ 
  title, 
  subtitle, 
  showFilters = true,
  onFilterClick,
  onExport 
}: HeaderProps) {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-30">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Título */}
          <div className="flex-1">
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
              <Badge variant="info" icon="🔄">
                Mock Data
              </Badge>
            </div>
            {subtitle && (
              <p className="text-sm text-gray-500 mt-1">{subtitle}</p>
            )}
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2">
            {showFilters && (
              <Button
                variant="outline"
                size="md"
                leftIcon={<Filter size={16} />}
                onClick={onFilterClick}
              >
                Filtros
              </Button>
            )}
            
            {onExport && (
              <Button
                variant="secondary"
                size="md"
                leftIcon={<Download size={16} />}
                onClick={onExport}
              >
                Exportar
              </Button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}

```


## **PASSO 21: Layout - AppLayout Principal**---

```bash

import { useState, ReactNode } from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { FiltersPanel } from '@/components/filters/FiltersPanel';
import { cn } from '@/lib/utils/cn';

interface AppLayoutProps {
  children: ReactNode;
  title: string;
  subtitle?: string;
}

export function AppLayout({ children, title, subtitle }: AppLayoutProps) {
  const [activeTab, setActiveTab] = useState('overview');
  const [showFilters, setShowFilters] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const handleExport = () => {
    // TODO: Implementar exportação
    console.log('Exportar dados');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar 
        activeTab={activeTab} 
        onTabChange={setActiveTab}
      />

      {/* Main Content */}
      <div
        className={cn(
          'transition-all duration-300',
          sidebarCollapsed ? 'ml-16' : 'ml-64'
        )}
      >
        {/* Header */}
        <Header
          title={title}
          subtitle={subtitle}
          showFilters={true}
          onFilterClick={() => setShowFilters(!showFilters)}
          onExport={handleExport}
        />

        {/* Content Area */}
        <main className="p-6">
          {children}
        </main>
      </div>

      {/* Filters Panel (Sidebar direita) */}
      <FiltersPanel 
        isOpen={showFilters} 
        onClose={() => setShowFilters(false)} 
      />
    </div>
  );
}

```


## **PASSO 22: Painel de Filtros**---

```bash
import { X, RotateCcw } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { useProjectionStore } from '@/features/projection/stores/projectionStore';
import { cn } from '@/lib/utils/cn';

interface FiltersPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

export function FiltersPanel({ isOpen, onClose }: FiltersPanelProps) {
  const { filters, updateFilters, resetFilters } = useProjectionStore();

  const handleApply = () => {
    onClose();
  };

  return (
    <>
      {/* Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 transition-opacity"
          onClick={onClose}
        />
      )}

      {/* Panel */}
      <aside
        className={cn(
          'fixed right-0 top-0 h-screen w-80 bg-white border-l border-gray-200 shadow-xl z-50 transition-transform duration-300',
          isOpen ? 'translate-x-0' : 'translate-x-full'
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Filtros</h2>
          <button
            onClick={onClose}
            className="p-1.5 hover:bg-gray-100 rounded-md transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Content */}
        <div className="p-4 space-y-6 overflow-y-auto h-[calc(100vh-130px)]">
          {/* Período */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700">
              Período
            </label>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs text-gray-500 mb-1">
                  Mês Início
                </label>
                <input
                  type="number"
                  min={1}
                  max={filters.periodEnd}
                  value={filters.periodStart}
                  onChange={(e) =>
                    updateFilters({ periodStart: Number(e.target.value) })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-500 mb-1">
                  Mês Fim
                </label>
                <input
                  type="number"
                  min={filters.periodStart}
                  max={36}
                  value={filters.periodEnd}
                  onChange={(e) =>
                    updateFilters({ periodEnd: Number(e.target.value) })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                />
              </div>
            </div>
            <p className="text-xs text-gray-500">
              Visualizando {filters.periodEnd - filters.periodStart + 1} meses
            </p>
          </div>

          {/* Granularidade */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700">
              Granularidade
            </label>
            <div className="space-y-2">
              {[
                { value: 'monthly', label: 'Mensal' },
                { value: 'quarterly', label: 'Trimestral' },
                { value: 'yearly', label: 'Anual' },
              ].map((option) => (
                <label
                  key={option.value}
                  className="flex items-center gap-2 cursor-pointer"
                >
                  <input
                    type="radio"
                    name="granularity"
                    value={option.value}
                    checked={filters.granularity === option.value}
                    onChange={(e) =>
                      updateFilters({
                        granularity: e.target.value as any,
                      })
                    }
                    className="w-4 h-4 text-primary-500 focus:ring-primary-500"
                  />
                  <span className="text-sm text-gray-700">{option.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Cenários (disabled por enquanto) */}
          <div className="space-y-3 opacity-50">
            <label className="block text-sm font-medium text-gray-700">
              Cenário
            </label>
            <select
              disabled
              className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 cursor-not-allowed"
            >
              <option>Base (Mock Data)</option>
            </select>
            <p className="text-xs text-gray-500">
              Múltiplos cenários disponíveis na próxima versão
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200 bg-white space-y-2">
          <Button
            variant="primary"
            fullWidth
            onClick={handleApply}
          >
            Aplicar Filtros
          </Button>
          <Button
            variant="ghost"
            fullWidth
            leftIcon={<RotateCcw size={16} />}
            onClick={() => {
              resetFilters();
              handleApply();
            }}
          >
            Resetar
          </Button>
        </div>
      </aside>
    </>
  );
}


```


## **PASSO 23: Componente MetricCard**---

```bash

import { Card } from '@/components/ui/Card';
import { formatCurrency, formatPercentage, formatNumber, formatDelta } from '@/lib/utils/formatters';
import { cn } from '@/lib/utils/cn';

interface MetricCardProps {
  label: string;
  value: number | string;
  delta?: number;
  format?: 'currency' | 'percentage' | 'number' | 'text';
  icon?: React.ReactNode;
  description?: string;
  trend?: 'up' | 'down' | 'neutral';
}

export function MetricCard({
  label,
  value,
  delta,
  format = 'number',
  icon,
  description,
  trend,
}: MetricCardProps) {
  // Formata o valor principal
  const formattedValue = typeof value === 'string' 
    ? value 
    : format === 'currency'
    ? formatCurrency(value)
    : format === 'percentage'
    ? formatPercentage(value)
    : formatNumber(value);

  // Formata o delta se existir
  const deltaInfo = delta !== undefined ? formatDelta(delta, format === 'currency' ? 'currency' : 'percentage') : null;

  return (
    <Card hover className="transition-all duration-200 hover:scale-[1.02]">
      <div className="space-y-3">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-500">{label}</p>
          </div>
          {icon && (
            <div className="text-gray-400">
              {icon}
            </div>
          )}
        </div>

        {/* Valor Principal */}
        <div>
          <p className="text-3xl font-bold text-gray-900">
            {formattedValue}
          </p>
          
          {/* Delta/Variação */}
          {deltaInfo && (
            <div className="flex items-center gap-1 mt-2">
              <span className={cn('text-sm font-medium', deltaInfo.color)}>
                {deltaInfo.icon} {deltaInfo.formatted}
              </span>
              <span className="text-xs text-gray-500">vs. anterior</span>
            </div>
          )}
        </div>

        {/* Descrição adicional */}
        {description && (
          <p className="text-xs text-gray-500 border-t border-gray-100 pt-2">
            {description}
          </p>
        )}
      </div>
    </Card>
  );
}

/**
 * Grid de Métricas
 */
interface MetricGridProps {
  children: React.ReactNode;
  columns?: 2 | 3 | 4;
}

export function MetricGrid({ children, columns = 4 }: MetricGridProps) {
  const gridCols = {
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4',
  };

  return (
    <div className={cn('grid gap-4', gridCols[columns])}>
      {children}
    </div>
  );
}

```


## **PASSO 24: Componente de Alert/Insight**---

```bash

import { AlertLevel, ALERT_COLORS } from '@/lib/theme/colors';
import { formatCurrency } from '@/lib/utils/formatters';
import { cn } from '@/lib/utils/cn';
import type { Insight } from '@/types/api.types';

interface AlertCardProps {
  insight: Insight;
}

export function AlertCard({ insight }: AlertCardProps) {
  const colors = ALERT_COLORS[insight.level];

  return (
    <div
      className={cn(
        'rounded-lg border p-4 transition-all hover:shadow-md',
        colors.bg,
        colors.border,
        colors.text
      )}
    >
      <div className="flex gap-3">
        {/* Icon */}
        <div className="flex-shrink-0 text-2xl">
          {colors.icon}
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <h4 className="font-semibold text-sm mb-1">
            {insight.title}
          </h4>
          <p className="text-sm opacity-90 mb-2">
            {insight.description}
          </p>

          {/* Value */}
          {insight.value !== undefined && (
            <p className="text-lg font-bold mb-2">
              {formatCurrency(insight.value)}
            </p>
          )}

          {/* Action */}
          {insight.action && (
            <div className="mt-2 pt-2 border-t border-current/20">
              <p className="text-xs font-medium">
                💡 Ação: {insight.action}
              </p>
            </div>
          )}

          {/* Impact */}
          {insight.impact && (
            <div className="mt-1">
              <p className="text-xs opacity-75">
                📊 Impacto: {insight.impact}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

/**
 * Seção de Alertas
 */
interface AlertsSectionProps {
  insights: Insight[];
  title?: string;
  maxVisible?: number;
}

export function AlertsSection({ 
  insights, 
  title = '🚨 Alertas Críticos',
  maxVisible = 3 
}: AlertsSectionProps) {
  const visibleInsights = insights.slice(0, maxVisible);
  const hasMore = insights.length > maxVisible;

  if (insights.length === 0) {
    return null;
  }

  return (
    <div className="space-y-3">
      <h2 className="text-xl font-bold text-gray-900">{title}</h2>
      <div className="space-y-3">
        {visibleInsights.map((insight, index) => (
          <AlertCard key={index} insight={insight} />
        ))}
      </div>
      {hasMore && (
        <button className="text-sm text-primary-600 hover:text-primary-700 font-medium">
          Ver mais {insights.length - maxVisible} alertas →
        </button>
      )}
    </div>
  );
}

```



