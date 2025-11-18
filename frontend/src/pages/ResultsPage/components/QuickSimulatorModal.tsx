// frontend/src/pages/ResultsPage/components/QuickSimulatorModal.tsx
import React, { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from '@/components/ui/Button';
import { Slider } from '@/components/ui/Slider';
import { Label } from '@/components/ui/label';
import { Rocket, Save, RotateCcw } from 'lucide-react';

interface QuickSimulatorModalProps {
  isOpen: boolean;
  onOpenChange: (isOpen: boolean) => void;
}

const SimulatorRow = ({ label, value, unit, impactText }: { label: string, value: number, unit: string, impactText: string }) => (
    <div className="grid grid-cols-3 items-center gap-4">
        <Label className="text-right">{label}</Label>
        <div className="col-span-2 flex items-center gap-4">
            <Slider defaultValue={[value]} max={value * 2} step={1} className="w-32" />
            <span className="text-sm font-semibold text-blue-600 w-48">
                {value}{unit} → {value}{unit} <span className="text-slate-500 font-normal">({impactText})</span>
            </span>
        </div>
    </div>
);

export const QuickSimulatorModal = ({ isOpen, onOpenChange }: QuickSimulatorModalProps) => {
  // TODO: Manage state for sliders
  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-2xl">
            <span role="img" aria-label="lightning">⚡</span> Simulador Rápido
          </DialogTitle>
          <DialogDescription>
            Ajuste as principais alavancas e veja o impacto em tempo real na projeção.
          </DialogDescription>
        </DialogHeader>
        
        <div className="py-6 space-y-6">
            <SimulatorRow label="Taxa Crescimento MRR:" value={12} unit="%" impactText="+3pp = +R$18k no Mês 36" />
            <SimulatorRow label="Churn Mensal:" value={4} unit="%" impactText="-1pp = +R$12k no Mês 36" />
            <SimulatorRow label="ARPU Médio:" value={97} unit=" R$" impactText="+R$13 = +R$8k no Mês 36" />
            <SimulatorRow label="CAC Médio:" value={450} unit=" R$" impactText="-R$100 = LTV/CAC 6.9x" />
        </div>

        <div className="bg-slate-100 p-4 rounded-lg text-center">
            <p className="font-medium text-slate-800">
                <span className="font-bold">Impacto Projetado:</span> MRR Final passaria de <span className="font-bold">R$76k</span> para <span className="font-bold text-green-600">R$114k</span> (+50%) <span role="img" aria-label="rocket">🚀</span>
            </p>
        </div>

        <DialogFooter className="mt-6">
          <Button variant="outline">
            <RotateCcw className="mr-2 h-4 w-4" /> Resetar
          </Button>
          <Button variant="outline">
            <Save className="mr-2 h-4 w-4" /> Salvar como "Cenário Agressivo"
          </Button>
          <Button>
            <Rocket className="mr-2 h-4 w-4" /> Aplicar Simulação
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
