import { useAuthStore } from '@/features/auth';
import { useCategories } from '../hooks/useCategories';
import React, { useState } from 'react';
import { useForm } from '@tanstack/react-form';
import {
  createColumnHelper,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
  type SortingState,
} from '@tanstack/react-table';
import { Pencil, Plus, Trash2 } from 'lucide-react';
import type { Categoria, CategoriaFormData } from '@/features/categories';
import { CategoriaList } from '../components/CategoriaList';
import { CategoriaModal } from '../components/CategoriaModal';
import { AlertBanner, EmptyState, ErrorState, LoadingState } from '@/shared/components/StatusStates';

const columnHelper = createColumnHelper<Categoria>();

export const CategoriasPage: React.FC = () => {
  const isAdmin = useAuthStore((state) => state.user?.role === 'admin');

  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [categoriaToEdit, setCategoriaToEdit] = useState<Categoria | null>(null);
  const [modalError, setModalError] = useState<string | null>(null);
  const [pageAlert, setPageAlert] = useState<string | null>(null);
  const [sorting, setSorting] = useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = useState<string>('');

  const {
    data: categorias = [],
    isLoading,
    isError,
    error,
    refetch,
    createMutation,
    updateMutation,
    deleteMutation,
  } = useCategories({
    onSaved: () => handleCloseModal(),
    onSaveError: (err) => setModalError(err.message),
    onDeleted: () => setPageAlert(null),
    onDeleteError: (err) => setPageAlert(err.message),
  });
  const form = useForm({
    defaultValues: {
      nombre: categoriaToEdit?.nombre ?? '',
      descripcion: categoriaToEdit?.descripcion ?? '',
    },
    onSubmit: async ({ value }) => {
      setModalError(null);
      const payload: CategoriaFormData = {
        nombre: value.nombre.trim(),
        descripcion: value.descripcion.trim(),
      };
      if (categoriaToEdit) {
        await updateMutation.mutateAsync({ id: categoriaToEdit.id, payload });
      } else {
        await createMutation.mutateAsync(payload);
      }
    },
  });

  const handleOpenCreate = () => {
    setCategoriaToEdit(null);
    setModalError(null);
    form.reset();
    form.setFieldValue('nombre', '');
    form.setFieldValue('descripcion', '');
    setIsModalOpen(true);
  };

  const handleOpenEdit = (categoria: Categoria) => {
    setCategoriaToEdit(categoria);
    setModalError(null);
    form.reset();
    form.setFieldValue('nombre', categoria.nombre);
    form.setFieldValue('descripcion', categoria.descripcion ?? '');
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setCategoriaToEdit(null);
    setModalError(null);
    form.reset();
  };

  const handleDelete = (categoria: Categoria) => {
    if (window.confirm(`¿Estás segura de que querés eliminar la categoría "${categoria.nombre}"?`)) {
      deleteMutation.mutate(categoria.id);
    }
  };

  const columns = [
      columnHelper.accessor('id', {
        header: 'ID',
        cell: (info) => <span className="font-mono text-xs text-slate-500">#{info.getValue()}</span>,
      }),
      columnHelper.accessor('nombre', {
        header: 'Nombre',
        cell: (info) => <span className="font-semibold text-slate-900">{info.getValue()}</span>,
      }),
      columnHelper.accessor('descripcion', {
        header: 'Descripción',
        cell: (info) => (
          <span className="text-slate-600">
            {info.getValue() ? info.getValue() : <em className="text-slate-400">Sin descripción</em>}
          </span>
        ),
      }),
      columnHelper.display({
        id: 'acciones',
        header: 'Acciones',
        enableSorting: false,
        cell: ({ row }) => (
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => handleOpenEdit(row.original)}
              className="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-2.5 py-1.5 text-xs font-medium text-slate-700 hover:bg-indigo-50 hover:text-indigo-700 hover:border-indigo-200 transition-colors"
            >
              <Pencil className="h-3.5 w-3.5" />
              Editar
            </button>
            <button
              type="button"
              onClick={() => handleDelete(row.original)}
              className="inline-flex items-center gap-1.5 rounded-lg border border-red-200 bg-white px-2.5 py-1.5 text-xs font-medium text-red-600 hover:bg-red-50 transition-colors"
            >
              <Trash2 className="h-3.5 w-3.5" />
              Eliminar
            </button>
          </div>
        ),
      }),
  ];

  // TanStack Table administra su estado; esta llamada no se memoiza.
  // oxlint-disable-next-line react/incompatible-library
  const table = useReactTable({
    data: categorias,
    columns,
    state: {
      columnVisibility: { acciones: isAdmin },
      sorting,
      globalFilter,
    },
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    initialState: {
      pagination: {
        pageSize: 5,
      },
    },
  });

  return (
    <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
      <div className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Gestión de Categorías</h1>
          <p className="mt-1 text-sm text-slate-600">
            Administrá las categorías del catálogo con ordenamiento, filtrado y paginación.
          </p>
        </div>
        {isAdmin && (<button
          type="button"
          onClick={handleOpenCreate}
          className="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700 transition-colors"
        >
          <Plus className="h-4 w-4" />
          Nueva categoría
        </button>)}
      </div>

      <AlertBanner message={pageAlert} onClose={() => setPageAlert(null)} />

      {isLoading ? (
        <LoadingState message="Cargando categorías..." />
      ) : isError ? (
        <ErrorState message={error.message} onRetry={() => refetch()} />
      ) : categorias.length === 0 ? (
        <EmptyState
          title="No hay categorías registradas"
          description="Creá la primera categoría para comenzar a organizar tus productos."
          actionLabel="Nueva categoría"
          onAction={isAdmin ? handleOpenCreate : undefined}
        />
      ) : (
        <CategoriaList
          table={table}
          globalFilter={globalFilter}
          onGlobalFilterChange={setGlobalFilter}
        />
      )}

      <CategoriaModal
        isOpen={isAdmin && isModalOpen}
        isEditing={Boolean(categoriaToEdit)}
        apiError={modalError}
        onClose={handleCloseModal}
      >
        <form
          onSubmit={(e) => {
            e.preventDefault();
            e.stopPropagation();
            form.handleSubmit();
          }}
          className="space-y-4"
        >
          <form.Field
            name="nombre"
            validators={{
              onChange: ({ value }) =>
                !value || !value.trim()
                  ? 'El nombre de la categoría es obligatorio.'
                  : value.trim().length > 100
                  ? 'El nombre no puede superar los 100 caracteres.'
                  : undefined,
            }}
          >
            {(field) => (
              <div>
                <label htmlFor={field.name} className="block text-sm font-medium text-slate-700 mb-1">
                  Nombre <span className="text-red-500">*</span>
                </label>
                <input
                  id={field.name}
                  name={field.name}
                  type="text"
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                  placeholder="Ej. Pizzas, Bebidas, Postres..."
                  className="w-full rounded-lg border border-slate-300 px-3.5 py-2 text-sm text-slate-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
                />
                {field.state.meta.errors.length > 0 && (
                  <p className="mt-1 text-xs font-medium text-red-600">
                    {field.state.meta.errors.filter(Boolean).join(', ')}
                  </p>
                )}
              </div>
            )}
          </form.Field>

          <form.Field name="descripcion">
            {(field) => (
              <div>
                <label htmlFor={field.name} className="block text-sm font-medium text-slate-700 mb-1">
                  Descripción
                </label>
                <textarea
                  id={field.name}
                  name={field.name}
                  rows={3}
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                  placeholder="Descripción opcional de la categoría..."
                  className="w-full rounded-lg border border-slate-300 px-3.5 py-2 text-sm text-slate-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
                />
              </div>
            )}
          </form.Field>

          <div className="flex items-center justify-end gap-2.5 pt-3 border-t border-slate-200">
            <button
              type="button"
              onClick={handleCloseModal}
              className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors"
            >
              Cancelar
            </button>
            <form.Subscribe
              selector={(state) => [state.canSubmit, state.isSubmitting] as const}
            >
              {([canSubmit, isSubmitting]) => (
                <button
                  type="submit"
                  disabled={!canSubmit || isSubmitting || createMutation.isPending || updateMutation.isPending}
                  className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50 transition-colors"
                >
                  {isSubmitting || createMutation.isPending || updateMutation.isPending
                    ? 'Guardando...'
                    : categoriaToEdit
                    ? 'Guardar cambios'
                    : 'Crear categoría'}
                </button>
              )}
            </form.Subscribe>
          </div>
        </form>
      </CategoriaModal>
    </div>
  );
};

export default CategoriasPage;





