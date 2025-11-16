import { Card, CardHeader, CardContent } from '@/components/ui/Card';
import { ReactNode } from 'react';

interface ChartContainerProps {
  title: string;
  subtitle?: string;
  children: ReactNode;
  height?: number;
  action?: ReactNode;
}

export function ChartContainer({ title, subtitle, children, height = 300, action }: ChartContainerProps) {
  return (
    <Card>
      <CardHeader title={title} subtitle={subtitle} action={action} />
      <CardContent padding="md">
        <div style={{ height: `${height}px` }}>
          {children}
        </div>
      </CardContent>
    </Card>
  );
}
