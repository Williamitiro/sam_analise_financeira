// frontend/src/pages/ResultsPage/components/InsightsBar.tsx
import { Button } from '@/components/ui/Button';
import React from 'react';

export const InsightsBar = () => {
  return (
    <div className="flex items-center gap-2">
      <Button variant="outline">Insight 1</Button>
      <Button variant="outline">Insight 2</Button>
      <Button variant="outline">Insight 3</Button>
    </div>
  );
};
