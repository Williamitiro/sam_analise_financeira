import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, X } from 'lucide-react';
import { useMockProjection } from '@/features/projection/hooks/useMockProjection';
import { cn } from '@/lib/utils/cn';

export function AlertHub() {
  const [isOpen, setIsOpen] = useState(false);
  const { insights } = useMockProjection();

  if (!insights || insights.length === 0) {
    return null;
  }

  const count = insights.length;
  const hasHighPriority = insights.some(a => a.level === 'CRITICAL');

  const handleAlertAction = (insight: any) => {
    console.log('Triggering action for:', insight.title);
    // Lógica para simulação ou navegação virá aqui
    setIsOpen(false);
  };

  return (
    <div className="relative">
      {/* Botão do Alerta */}
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className={cn(
          'relative flex items-center gap-2 px-3 py-2 rounded-lg border transition-all',
          hasHighPriority 
            ? 'bg-danger-50 border-danger-200 text-danger-700' 
            : 'bg-warning-50 border-warning-200 text-warning-700',
          'hover:shadow-md'
        )}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <AlertTriangle className="w-4 h-4" />
        <span className="text-sm font-medium">{count} alertas</span>
        
        {hasHighPriority && (
          <motion.span 
            className="absolute -top-1.5 -right-1.5 w-4 h-4 bg-danger-500 text-white text-[10px] rounded-full flex items-center justify-center border-2 border-white"
            animate={{ scale: [1, 1.25, 1] }}
            transition={{ repeat: Infinity, duration: 1.5, ease: "easeInOut" }}
          >
            !
          </motion.span>
        )}
      </motion.button>

      {/* Dropdown Panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            transition={{ type: "spring", stiffness: 300, damping: 25 }}
            className="absolute right-0 mt-2 w-80 rounded-xl bg-white border border-slate-200 shadow-xl z-50 overflow-hidden"
          >
            <div className="p-3 border-b border-slate-100 flex items-center justify-between">
              <p className="text-sm font-semibold text-slate-900">Alertas Inteligentes</p>
              <button 
                onClick={() => setIsOpen(false)}
                className="text-slate-400 hover:text-slate-600"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            
            <div className="max-h-96 overflow-y-auto">
              {insights.map((alert, i) => (
                <motion.div
                  key={alert.title}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.05 }}
                  className={cn(
                    'p-3 border-b border-slate-50 hover:bg-slate-50 cursor-pointer',
                    alert.level === 'CRITICAL' ? 'border-l-4 border-l-danger-500' : 'border-l-4 border-l-warning-500'
                  )}
                  onClick={() => handleAlertAction(alert)}
                >
                  <div className="flex items-start gap-2">
                    <AlertTriangle className={cn(
                      'w-4 h-4 flex-shrink-0 mt-0.5',
                      alert.level === 'CRITICAL' ? 'text-danger-500' : 'text-warning-500'
                    )} />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-slate-900">{alert.title}</p>
                      <p className="text-xs text-slate-600 mt-0.5">{alert.description}</p>
                      {alert.action && <p className="text-xs text-blue-600 mt-1 font-medium">{alert.action} →</p>}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
            
            <div className="p-2 bg-slate-50">
              <button className="w-full text-xs text-slate-600 text-center py-1 hover:text-slate-800">
                Ver histórico de alertas
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
