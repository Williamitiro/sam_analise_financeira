// frontend/src/pages/ResultsPage/components/MainControls.tsx
import React from 'react';
import { InsightsBar } from './InsightsBar';
import { SimulatorTrigger } from './SimulatorTrigger';

export const MainControls = () => {
  return (
    <div className="flex items-center justify-between mb-8">
      <InsightsBar />
      <SimulatorTrigger />
    </div>
  );
};
