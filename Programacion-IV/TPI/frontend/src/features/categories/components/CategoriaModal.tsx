import React from 'react';
import { AlertCircle, X } from 'lucide-react';

interface CategoriaModalProps {
  isOpen: boolean;
  isEditing: boolean;
  apiError: string | null;
  onClose: () => void;
  children: React.ReactNode;
}

export const CategoriaModal: React.FC<CategoriaModalProps> = ({
  isOpen,
  isEditing,
  apiError,
  onClose,
  children,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4">
      <div className="w-full max-w-lg rounded-2xl bg-white shadow-xl border border-slate-200 overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between border-b border-slate-200 px-6 py-4 bg-slate-50">
          <h2 className="text-lg font-semibold text-slate-800">
            {isEditing ? 'Editar categoría' : 'Nueva categoría'}
          </h2>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-200/60 hover:text-slate-600 transition-colors"
            aria-label="Cerrar modal"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="p-6">
          {apiError && (
            <div className="mb-4 flex items-start gap-2.5 rounded-lg border border-red-200 bg-red-50 p-3.5 text-sm text-red-700">
              <AlertCircle className="h-5 w-5 text-red-600 shrink-0 mt-0.5" />
              <span>{apiError}</span>
            </div>
          )}
          {children}
        </div>
      </div>
    </div>
  );
};

