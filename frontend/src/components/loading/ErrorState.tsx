import { Button } from '@/components/ui/Button';

/**
 * Empty State
 */
export function EmptyState({
  icon = '📊',
  title,
  description,
  action,
}: {
  icon?: string;
  title: string;
  description: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="text-6xl mb-4">{icon}</div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-500 mb-6 max-w-sm">{description}</p>
      {action && (
        <Button
          onClick={action.onClick}
          variant="primary"
        >
          {action.label}
        </Button>
      )}
    </div>
  );
}

/**
 * Error State
 */
export function ErrorState({
  title = 'Algo deu errado',
  description,
  onRetry,
}: {
  title?: string;
  description: string;
  onRetry?: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="text-6xl mb-4">⚠️</div>
      <h3 className="text-lg font-semibold text-danger-700 mb-2">{title}</h3>
      <p className="text-gray-600 mb-6 max-w-sm">{description}</p>
      {onRetry && (
        <Button
          onClick={onRetry}
          variant="secondary"
        >
          Tentar Novamente
        </Button>
      )}
    </div>
  );
}
