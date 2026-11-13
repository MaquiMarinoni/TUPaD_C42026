import { useAuthStore } from '@/features/auth';
import { useIngredients } from '../hooks/useIngredients';
import React, { useState } from 'react';
import { useForm } from '@tanstack/react-form';
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
  type SortingState,
} from '@tanstack/react-table';
import {
  AlertCircle,
  ArrowDown,
  ArrowUp,
  ArrowUpDown,
  ChevronLeft,
  ChevronRight,
  Pencil,
  Plus,
  Search,
  Trash2,
  X,
} from 'lucide-react';
import type { Ingrediente, IngredienteFormData } from '@/features/ingredients';
import { AlertBanner, EmptyState, ErrorState, LoadingState } from '@/shared/components/StatusStates';

const columnHelper = createColumnHelper<Ingrediente>();

export const IngredientesPage: React.FC = () => {
  const isAdmin = useAuthStore((state) => state.user?.role === 'admin');

  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [ingredienteToEdit, setIngredienteToEdit] = useState<Ingrediente | null>(null);
  const [modalError, setModalError] = useState<string | null>(null);
  const [pageAlert, setPageAlert] = useState<string | null>(null);
  const [sorting, setSorting] = useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = useState<string>('');

  const {
    data: ingredientes = [],
    isLoading,
    isError,
    error,
    refetch,
    createMutation,
    updateMutation,
    deleteMutation,
  } = useIngredients({
    onSaved: () => handleCloseModal(),
    onSaveError: (err) => setModalError(err.message),
    onDeleted: () => setPageAlert(null),
    onDeleteError: (err) => setPageAlert(err.message),
  });
  const form = useForm({
    defaultValues: {
      nombre: ingredienteToEdit?.nombre ?? '',
    },
    onSubmit: async ({ value }) => {
      setModalError(null);
      const payload: IngredienteFormData = {
        nombre: value.nombre.trim(),
      };
      if (ingredienteToEdit) {
        await updateMutation.mutateAsync({ id: ingredienteToEdit.id, payload });
      } else {
        await createMutation.mutateAsync(payload);
      }
    },
  });

  const handleOpenCreate = () => {
    setIngredienteToEdit(null);
    setModalError(null);
    form.reset();
    form.setFieldValue('nombre', '');
    setIsModalOpen(true);
  };

  const handleOpenEdit = (ingrediente: Ingrediente) => {
    setIngredienteToEdit(ingrediente);
    setModalError(null);
    form.reset();
    form.setFieldValue('nombre', ingrediente.nombre);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setIngredienteToEdit(null);
    setModalError(null);
    form.reset();
  };

  const handleDelete = (ingrediente: Ingrediente) => {
    if (window.confirm(`¿Estás segura de que querés eliminar el ingrediente "${ingrediente.nombre}"?`)) {
      deleteMutation.mutate(ingrediente.id);
    }
  };

  const columns = [
      columnHelper.accessor('id', {
        header: 'ID',
        cell: (info) => <span className="font-mono text-xs text-slate-500">#{info.getValue()}</span>,
      }),
      columnHelper.accessor('nombre', {
        header: 'Nombre del Ingrediente',
        cell: (info) => <span className="font-semibold text-slate-900">{info.getValue()}</span>,
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
    data: ingredientes,
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
          <h1 className="text-2xl font-bold text-slate-900">Gestión de Ingredientes</h1>
          <p className="mt-1 text-sm text-slate-600">
            Administrá la lista de ingredientes disponibles en el sistema.
          </p>
        </div>
        {isAdmin && (<button
          type="button"
          onClick={handleOpenCreate}
          className="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700 transition-colors"
        >
          <Plus className="h-4 w-4" />
          Nuevo ingrediente
        </button>)}
      </div>

      <AlertBanner message={pageAlert} onClose={() => setPageAlert(null)} />

      {isLoading ? (
        <LoadingState message="Cargando ingredientes..." />
      ) : isError ? (
        <ErrorState message={error.message} onRetry={() => refetch()} />
      ) : ingredientes.length === 0 ? (
        <EmptyState
          title="No hay ingredientes registrados"
          description="Creá el primer ingrediente para el catálogo."
          actionLabel="Nuevo ingrediente"
          onAction={isAdmin ? handleOpenCreate : undefined}
        />
      ) : (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <div className="relative flex-1 max-w-md">
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                value={globalFilter ?? ''}
                onChange={(e) => setGlobalFilter(e.target.value)}
                placeholder="Filtrar ingredientes por nombre..."
                className="w-full rounded-lg border border-slate-300 pl-9 pr-3 py-2 text-sm text-slate-800 placeholder-slate-400 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
              />
            </div>
            <span className="text-xs font-medium text-slate-500">
              Mostrando {table.getRowModel().rows.length} de {table.getFilteredRowModel().rows.length} registros
            </span>
          </div>

          <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-200">
                <thead className="bg-slate-50">
                  {table.getHeaderGroups().map((headerGroup) => (
                    <tr key={headerGroup.id}>
                      {headerGroup.headers.map((header) => {
                        const canSort = header.column.getCanSort();
                        const sorted = header.column.getIsSorted();
                        return (
                          <th
                            key={header.id}
                            scope="col"
                            onClick={canSort ? header.column.getToggleSortingHandler() : undefined}
                            className={`px-6 py-3.5 text-left text-xs font-semibold uppercase tracking-wider text-slate-600 ${
                              canSort ? 'cursor-pointer select-none hover:bg-slate-100 transition-colors' : ''
                            }`}
                          >
                            <div className="flex items-center gap-1.5">
                              {header.isPlaceholder
                                ? null
                                : flexRender(header.column.columnDef.header, header.getContext())}
                              {canSort && (
                                <span className="text-slate-400">
                                  {sorted === 'asc' ? (
                                    <ArrowUp className="h-3.5 w-3.5 text-indigo-600" />
                                  ) : sorted === 'desc' ? (
                                    <ArrowDown className="h-3.5 w-3.5 text-indigo-600" />
                                  ) : (
                                    <ArrowUpDown className="h-3.5 w-3.5" />
                                  )}
                                </span>
                              )}
                            </div>
                          </th>
                        );
                      })}
                    </tr>
                  ))}
                </thead>
                <tbody className="divide-y divide-slate-200 bg-white">
                  {table.getRowModel().rows.map((row) => (
                    <tr key={row.id} className="hover:bg-slate-50/80 transition-colors">
                      {row.getVisibleCells().map((cell) => (
                        <td key={cell.id} className="px-6 py-4 text-sm text-slate-700 whitespace-nowrap">
                          {flexRender(cell.column.columnDef.cell, cell.getContext())}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="flex items-center justify-between border-t border-slate-200 bg-slate-50 px-6 py-3">
              <div className="text-xs font-medium text-slate-600">
                Página <span className="font-semibold text-slate-900">{table.getState().pagination.pageIndex + 1}</span> de{' '}
                <span className="font-semibold text-slate-900">{Math.max(1, table.getPageCount())}</span>
              </div>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => table.previousPage()}
                  disabled={!table.getCanPreviousPage()}
                  className="inline-flex items-center gap-1 rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 shadow-sm hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50 transition-colors"
                >
                  <ChevronLeft className="h-4 w-4" />
                  Anterior
                </button>
                <button
                  type="button"
                  onClick={() => table.nextPage()}
                  disabled={!table.getCanNextPage()}
                  className="inline-flex items-center gap-1 rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 shadow-sm hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50 transition-colors"
                >
                  Siguiente
                  <ChevronRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {isAdmin && isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4">
          <div className="w-full max-w-lg rounded-2xl bg-white shadow-xl border border-slate-200 overflow-hidden">
            <div className="flex items-center justify-between border-b border-slate-200 px-6 py-4 bg-slate-50">
              <h2 className="text-lg font-semibold text-slate-800">
                {ingredienteToEdit ? 'Editar ingrediente' : 'Nuevo ingrediente'}
              </h2>
              <button
                type="button"
                onClick={handleCloseModal}
                className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-200/60 hover:text-slate-600 transition-colors"
                aria-label="Cerrar modal"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="p-6">
              {modalError && (
                <div className="mb-4 flex items-start gap-2.5 rounded-lg border border-red-200 bg-red-50 p-3.5 text-sm text-red-700">
                  <AlertCircle className="h-5 w-5 text-red-600 shrink-0 mt-0.5" />
                  <span>{modalError}</span>
                </div>
              )}

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
                        ? 'El nombre del ingrediente es obligatorio.'
                        : value.trim().length > 100
                        ? 'El nombre no puede superar los 100 caracteres.'
                        : undefined,
                  }}
                >
                  {(field) => (
                    <div>
                      <label htmlFor={field.name} className="block text-sm font-medium text-slate-700 mb-1">
                        Nombre del ingrediente <span className="text-red-500">*</span>
                      </label>
                      <input
                        id={field.name}
                        name={field.name}
                        type="text"
                        value={field.state.value}
                        onBlur={field.handleBlur}
                        onChange={(e) => field.handleChange(e.target.value)}
                        placeholder="Ej. Queso Muzzarella, Harina 0000, Tomate..."
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
                          : ingredienteToEdit
                          ? 'Guardar cambios'
                          : 'Crear ingrediente'}
                      </button>
                    )}
                  </form.Subscribe>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default IngredientesPage;





