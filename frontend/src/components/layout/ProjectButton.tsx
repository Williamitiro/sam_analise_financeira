// frontend/src/components/layout/ProjectButton.tsx
import React from 'react';
import { Button } from '@/components/ui/Button';
import { Rocket, Loader2 } from 'lucide-react';
import { useProjectionStore } from '@/stores/projectionStore';
import { defaultConfig } from '@/lib/api/projection';
import { useToast } from '@/hooks/use-toast';

export const ProjectButton = () => {
  const { runProjection, isLoading } = useProjectionStore();
  const { toast } = useToast();

  const handleProject = async () => {
    if (isLoading) return;
    toast({
      title: "Calculando projeção...",
      description: "Usando a configuração padrão.",
    });
    try {
      await runProjection(defaultConfig);
      toast({
        title: "Sucesso!",
        description: "Projeção calculada com sucesso.",
        variant: "success",
      });
    } catch (error) {
      toast({
        title: "Erro ao calcular",
        description: "Não foi possível gerar a projeção. Verifique se o backend está rodando.",
        variant: "destructive",
      });
    }
  };

  return (
    <Button onClick={handleProject} disabled={isLoading}>
      {isLoading ? (
        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
      ) : (
        <Rocket className="mr-2 h-4 w-4" />
      )}
      {isLoading ? 'Calculando...' : 'Projetar'}
    </Button>
  );
};
