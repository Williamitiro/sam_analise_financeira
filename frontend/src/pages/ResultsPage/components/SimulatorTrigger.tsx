// frontend/src/pages/ResultsPage/components/SimulatorTrigger.tsx
import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { QuickSimulatorModal } from './QuickSimulatorModal';
import { Beaker } from 'lucide-react';

export const SimulatorTrigger = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div>
      <Button variant="outline" onClick={() => setIsModalOpen(true)}>
        <Beaker className="mr-2 h-4 w-4" />
        Simulador Rápido
      </Button>
      <QuickSimulatorModal isOpen={isModalOpen} onOpenChange={setIsModalOpen} />
    </div>
  );
};
