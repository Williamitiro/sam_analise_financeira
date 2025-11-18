/** @type {import('tailwindcss').Config} */
export default {
    darkMode: ["class"],
    content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
  	extend: {
  		colors: {
  			slate: {
  				'50': '#f8fafc',
  				'100': '#f1f5f9',
  				'200': '#e2e8f0',
  				'300': '#cbd5e1',
  				'400': '#94a3b8',
  				'500': '#64748b',
  				'600': '#475569',
  				'700': '#334155',
  				'800': '#1e293b',
  				'900': '#0f172a'
  			},
  			primary: {
  				'500': '#3b82f6',
  				DEFAULT: 'hsl(var(--primary))',
  				foreground: 'hsl(var(--primary-foreground))'
  			},
  			success: {
  				'50': '#f0fdf4',
  				'100': '#dcfce7',
  				'500': '#10b981',
  				'700': '#047857'
  			},
  			warning: {
  				'50': '#fffbeb',
  				'500': '#f59e0b',
  				'700': '#b45309'
  			},
  			danger: {
  				'50': '#fef2f2',
  				'500': '#ef4444',
  				'700': '#b91c1c'
  			},
  			mrr: '#6366f1',
  			cash: '#10b981',
  			opex: '#f97316',
  			background: 'hsl(var(--background))',
  			foreground: 'hsl(var(--foreground))',
  			card: {
  				DEFAULT: 'hsl(var(--card))',
  				foreground: 'hsl(var(--card-foreground))'
  			},
  			popover: {
  				DEFAULT: 'hsl(var(--popover))',
  				foreground: 'hsl(var(--popover-foreground))'
  			},
  			secondary: {
  				DEFAULT: 'hsl(var(--secondary))',
  				foreground: 'hsl(var(--secondary-foreground))'
  			},
  			muted: {
  				DEFAULT: 'hsl(var(--muted))',
  				foreground: 'hsl(var(--muted-foreground))'
  			},
  			accent: {
  				DEFAULT: 'hsl(var(--accent))',
  				foreground: 'hsl(var(--accent-foreground))'
  			},
  			destructive: {
  				DEFAULT: 'hsl(var(--destructive))',
  				foreground: 'hsl(var(--destructive-foreground))'
  			},
  			border: 'hsl(var(--border))',
  			input: 'hsl(var(--input))',
  			ring: 'hsl(var(--ring))',
  			chart: {
  				'1': 'hsl(var(--chart-1))',
  				'2': 'hsl(var(--chart-2))',
  				'3': 'hsl(var(--chart-3))',
  				'4': 'hsl(var(--chart-4))',
  				'5': 'hsl(var(--chart-5))'
  			}
  		},
  		fontFamily: {
  			sans: [
  				'Inter',
  				'system-ui',
  				'sans-serif'
  			],
  			mono: [
  				'JetBrains Mono"',
  				'monospace'
  			]
  		},
  		borderRadius: {
  			DEFAULT: '0.5rem',
  			md: 'calc(var(--radius) - 2px)',
  			lg: 'var(--radius)',
  			xl: '1rem',
  			'2xl': '1.5rem',
  			sm: 'calc(var(--radius) - 4px)'
  		},
  		animation: {
  			shimmer: 'shimmer 2s ease-in-out infinite'
  		},
  		keyframes: {
  			shimmer: {
  				'0%, 100%': {
  					backgroundPosition: '-200% 0'
  				},
  				'50%': {
  					backgroundPosition: '200% 0'
  				}
  			}
  		}
  	}
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
      require("tailwindcss-animate")
],
  safelist: [
    'bg-blue-500', 'bg-amber-500', 'bg-green-500', 'bg-indigo-500', 'bg-purple-500', 'bg-pink-500',
    'border-l-red-500', 'border-l-amber-500',
    'text-red-500', 'text-amber-500', 'text-green-700', 'text-red-700', 'text-slate-700', 'text-amber-700',
  ],
}