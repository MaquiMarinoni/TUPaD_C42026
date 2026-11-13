import React from 'react';
import { AlertCircle, Inbox, Loader2, RefreshCw, X } from 'lucide-react';

interface LoadingStateProps {
  message?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({
  message = 'Cargando datos del catálogo...',
}) => {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-slate-200 bg-white p-12 text-center shadow-sm">
      <Loader2 className="h-10 w-10 animate-spin text-indigo-600 mb-3" />
      <p className="text-base font-medium text-slate-700">{message}</p>
      <p className="text-sm text-slate-500 mt-1">Por favor esperá unos instantes.</p>
    </div>
  );
};

interface EmptyStateProps {
  title?: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'No hay registros disponibles',
  description = 'Aún no se han cargado elementos en esta sección.',
  actionLabel,
  onAction,
}) => {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-slate-300 bg-white p-12 text-center shadow-sm">
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-indigo-50 text-indigo-600 mb-4">
        <Inbox className="h-6 w-6" />
      </div>
      <h3 className="text-lg font-semibold text-slate-800">{title}</h3>
      <p className="mt-1 max-w-md text-sm text-slate-500">{description}</p>
      {actionLabel && onAction && (
        <button
          type="button"
          onClick={onAction}
          className="mt-5 inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 transition-colors"
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
};

interface ErrorStateProps {
  message: string;
  onRetry?: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({ message, onRetry }) => {
  return (
    <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-red-800 shadow-sm">
      <div className="flex items-start gap-3">
        <AlertCircle className="h-6 w-6 text-red-600 shrink-0 mt-0.5" />
        <div className="flex-1">
          <h3 className="text-base font-semibold text-red-900">Error al comunicarse con el servidor</h3>
          <p className="mt-1 text-sm text-red-700">{message}</p>
          {onRetry && (
            <button
              type="button"
              onClick={onRetry}
              className="mt-4 inline-flex items-center gap-2 rounded-lg bg-red-600 px-3.5 py-1.5 text-xs font-medium text-white hover:bg-red-700 transition-colors"
            >
              <RefreshCw className="h-3.5 w-3.5" />
              Reintentar
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

interface AlertBannerProps {
  message: string | null;
  onClose: () => void;
}

export const AlertBanner: React.FC<AlertBannerProps> = ({ message, onClose }) => {
  if (!message) return null;
  return (
    <div className="mb-6 flex items-center justify-between rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800 shadow-sm">
      <div className="flex items-center gap-2.5">
        <AlertCircle className="h-5 w-5 text-red-600 shrink-0" />
        <span className="font-medium">{message}</span>
      </div>
      <button
        type="button"
        onClick={onClose}
        className="rounded-lg p-1 text-red-600 hover:bg-red-100 transition-colors"
        aria-label="Cerrar alerta"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  );
};

