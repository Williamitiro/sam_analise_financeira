import { Card } from '@/components/ui/Card';
import { cn } from '@/lib/utils/cn';

/**
 * Loading Spinner
 */
export function LoadingSpinner({ 
  size = 'md',
  fullScreen = false 
}: { 
  size?: 'sm' | 'md' | 'lg';
  fullScreen?: boolean;
}) {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
  };

  const spinner = (
    <div
      className={cn(
        'animate-spin rounded-full border-b-2 border-primary-500',
        sizeClasses[size]
      )}
    />
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-gray-50/80 backdrop-blur-sm z-50">
        <div className="text-center">
          {spinner}
          <p className="mt-4 text-sm text-gray-600">Carregando...</p>
        </div>
      </div>
    );
  }

  return spinner;
}

/**
 * Skeleton base
 */
export function Skeleton({ 
  className 
}: { 
  className?: string 
}) {
  return (
    <div
      className={cn(
        'animate-skeleton rounded bg-gray-200',
        className
      )}
    />
  );
}

/**
 * Skeleton para Métrica (KPI Card)
 */
export function MetricSkeleton() {
  return (
    <Card padding="md">
      <div className="space-y-3">
        <Skeleton className="h-4 w-24" />
        <Skeleton className="h-8 w-32" />
        <Skeleton className="h-3 w-16" />
      </div>
    </Card>
  );
}

/**
 * Skeleton para Gráfico
 */
export function ChartSkeleton({ height = 300 }: { height?: number }) {
  return (
    <Card padding="md">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <Skeleton className="h-6 w-48" />
          <Skeleton className="h-8 w-24" />
        </div>
        <Skeleton className="w-full" style={{ height: `${height}px` }} />
      </div>
    </Card>
  );
}

/**
 * Skeleton para Tabela
 */
export function TableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <Card padding="md">
      <div className="space-y-4">
        <Skeleton className="h-6 w-48" />
        <div className="space-y-2">
          {Array.from({ length: rows }).map((_, i) => (
            <div key={i} className="flex gap-4">
              <Skeleton className="h-10 flex-1" />
              <Skeleton className="h-10 flex-1" />
              <Skeleton className="h-10 flex-1" />
              <Skeleton className="h-10 flex-1" />
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}

/**
 * Skeleton para Dashboard completo
 */
export function DashboardSkeleton() {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* KPIs Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricSkeleton />
        <MetricSkeleton />
        <MetricSkeleton />
        <MetricSkeleton />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartSkeleton />
        <ChartSkeleton />
      </div>

      <ChartSkeleton height={250} />
    </div>
  );
}
