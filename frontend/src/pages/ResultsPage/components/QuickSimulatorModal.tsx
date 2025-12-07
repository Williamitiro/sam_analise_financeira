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
import { Rocket, Save, RotateCcw, Loader2 } from 'lucide-react';
import { useConfigurationStore } from '@/stores/configurationStore';
import { useProjectionStore } from '@/stores/projectionStore';
import { useToast } from '@/hooks/use-toast';
import { defaultConfig } from '@/lib/api/projection';

interface QuickSimulatorModalProps {
  isOpen: boolean;
  onOpenChange: (isOpen: boolean) => void;
}

const SimulatorRow = ({ label, value, unit, impactText, onValueChange, max, step }: { label: string, value: number, unit: string, impactText: string, onValueChange: (value: number) => void, max: number, step: number }) => {
    const [localValue, setLocalValue] = useState(value);
    
    const handleValueChange = (newValue: number[]) => {
        setLocalValue(newValue[0]);
    };

    const handleCommit = (newValue: number[]) => {
        onValueChange(newValue[0]);
    };

    return (
        <div className="grid grid-cols-3 items-center gap-4">
            <Label className="text-right">{label}</Label>
            <div className="col-span-2 flex items-center gap-4">
                <Slider value={[localValue]} max={max} step={step} className="w-48" onValueChange={handleValueChange} onValueCommit={handleCommit} />
                <span className="text-sm font-semibold text-blue-600 w-48">
                    {localValue}{unit} <span className="text-slate-500 font-normal">({impactText})</span>
                </span>
            </div>
        </div>
    );
};

export const QuickSimulatorModal = ({ isOpen, onOpenChange }: QuickSimulatorModalProps) => {
  const { config, setConfig, resetConfig } = useConfigurationStore();
  const { runProjection, isLoading } = useProjectionStore();
  const { toast } = useToast();

  const handleApply = async () => {
    toast({
      title: "Aplicando simulação...",
      description: "A nova projeção está sendo gerada com os parâmetros do simulador.",
    });
    try {
      await runProjection(config);
      toast({
        title: "Sucesso!",
        description: "Simulação aplicada com sucesso.",
        variant: "success",
      });
      onOpenChange(false); // Close modal on success
    } catch (error) {
      toast({
        title: "Erro na simulação",
        description: "Não foi possível aplicar a simulação. Tente novamente.",
        variant: "destructive",
      });
    }
  };

  const handleReset = () => {
    resetConfig();
    toast({
      title: "Simulador resetado",
      description: "Os valores foram restaurados para o padrão.",
    });
  };

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
            <SimulatorRow label="Crescimento do Tráfego:" value={config.taxa_crescimento_trafego_mensal * 100} onValueChange={(v) => setConfig({ taxa_crescimento_trafego_mensal: v / 100 })} max={100} step={1} unit="%" impactText="Placeholder" />
            <SimulatorRow label="Churn Mensal:" value={config.churn_mensal * 100} onValueChange={(v) => setConfig({ churn_mensal: v / 100 })} max={20} step={0.1} unit="%" impactText="Placeholder" />
            <SimulatorRow label="ARPU Médio:" value={config.arpu_medio_override || ((config.preco_plano_lite * config.mix_plano_lite) + (config.preco_plano_trader * config.mix_plano_trader) + (config.preco_plano_pro * config.mix_plano_pro))} onValueChange={(v) => setConfig({ arpu_medio_override: v })} max={300} step={1} unit=" R$" impactText="Placeholder" />
            <SimulatorRow label="CAC Médio:" value={config.cac_pago_meta} onValueChange={(v) => setConfig({ cac_pago_meta: v })} max={1000} step={10} unit=" R$" impactText="Placeholder" />
        </div>

        <div className="bg-slate-100 p-4 rounded-lg text-center">
            <p className="font-medium text-slate-800">
                <span className="font-bold">Impacto Projetado:</span> (Cálculo do impacto pendente)
            </p>
        </div>

        <DialogFooter className="mt-6">
          <Button variant="outline" onClick={handleReset}>
            <RotateCcw className="mr-2 h-4 w-4" /> Resetar
          </Button>
          <Button variant="outline" disabled>
            <Save className="mr-2 h-4 w-4" /> Salvar como Cenário
          </Button>
          <Button onClick={handleApply} disabled={isLoading}>
            {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Rocket className="mr-2 h-4 w-4" />}
            {isLoading ? 'Aplicando...' : 'Aplicar Simulação'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
