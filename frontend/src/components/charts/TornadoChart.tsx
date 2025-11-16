import { motion } from 'framer-motion';
import { Play } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

// Example sensitivity data (replace with actual data prop later)
const sensitivityData = [
  { variable: 'Churn', impact: 18.5, rank: 1 },
  { variable: 'Preço Médio', impact: 15.2, rank: 2 },
  { variable: 'CAC', impact: -12.8, rank: 3 },
  { variable: 'Custo Pessoal', impact: -9.7, rank: 4 },
  { variable: 'Conv. Pagante', impact: 8.1, rank: 5 },
].sort((a, b) => Math.abs(b.impact) - Math.abs(a.impact)); // Sort by absolute impact

// Placeholder for modal function
const openSimulateModal = (variable: string) => {
  console.log(`Simular variável: ${variable}`);
  // Implement actual modal opening logic here
};

export function TornadoChart() {
  return (
    <div className="space-y-3">
      {/* Header com legenda */}
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-900">Análise de Sensibilidade</h3>
        <Badge variant="outline" className="text-xs">
          Top 5 variáveis
        </Badge>
      </div>
      
      {/* Descrição */}
      <p className="text-xs text-slate-500">
        Variação de ±20% no Lucro Final
      </p>
      
      {/* Barras com labels */}
      <div className="space-y-2">
        {sensitivityData.map(item => (
          <motion.div 
            key={item.variable}
            className="flex items-center gap-2"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: item.rank * 0.1 }}
          >
            {/* Nome da variável */}
            <div className="w-20 text-xs text-slate-600">
              {item.variable}
            </div>
            
            {/* Barra */}
            <div className="flex-1 h-6 bg-slate-100 rounded relative overflow-hidden">
              <motion.div 
                className={`h-full absolute top-0 left-1/2 transform -translate-x-1/2 ${
                  item.impact > 0 ? 'bg-green-500' : 'bg-red-500'
                }`}
                initial={{ width: 0 }}
                animate={{ width: `${Math.abs(item.impact) * 2}px` }} // Adjust scale as needed
                transition={{ duration: 0.8, ease: "easeOut" }}
              />
            </div>
            
            {/* Valor do impacto */}
            <div className={`w-12 text-xs font-medium ${
              item.impact > 0 ? 'text-green-700' : 'text-red-700'
            }`}>
              {item.impact > 0 ? '+' : ''}{item.impact}%
            </div>
            
            {/* Clique para simular */}
            <button 
              onClick={() => openSimulateModal(item.variable)}
              className="opacity-0 hover:opacity-100 transition-opacity"
            >
              <Play className="w-3 h-3 text-blue-600" />
            </button>
          </motion.div>
        ))}
      </div>
      
      {/* Régua visual */}
      <div className="flex justify-between text-xs text-slate-400">
        <span>-20%</span>
        <span>0%</span>
        <span>+20%</span>
      </div>
    </div>
  );
}
