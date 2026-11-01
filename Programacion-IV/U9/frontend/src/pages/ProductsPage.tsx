import type { Categoria } from '../types/categoria';
import { axiosInstance, listAll } from '../api/axiosInstance';
import { useAuthStore } from '../store/authStore';
import React, { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
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
import type { Producto, ProductoFormData } from '../types/producto';
import { AlertBanner, EmptyState, ErrorState, LoadingState } from '../components/StatusStates';

async function fetchProductos(): Promise<Producto[]> {
  return listAll<Producto>('/productos/');
}
async function createProducto(payload: ProductoFormData): Promise<Producto> {
  return (await axiosInstance.post<Producto>('/productos/', payload)).data;
}
async function updateProducto({ id, payload }: { id: number; payload: ProductoFormData }): Promise<Producto> {
  return (await axiosInstance.put<Producto>(`/productos/${id}`, payload)).data;
}
async function deleteProducto(id: number): Promise<void> {
  await axiosInstance.delete(`/productos/${id}`);
}

const columnHelper = createColumnHelper<Producto>();

export const ProductsPage: React.FC = () => {
  const isAdmin = useAuthStore((state) => state.user?.roles.includes('admin') ?? false);
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [productoToEdit, setProductoToEdit] = useState<Producto | null>(null);
  const [modalError, setModalError] = useState<string | null>(null);
  const [pageAlert, setPageAlert] = useState<string | null>(null);
  const [sorting, setSorting] = useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = useState<string>('');

  const {
    data: productos = [],
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<Producto[], Error>({
    queryKey: ['productos'],
    queryFn: fetchProductos,
  });

  const { data: categorias = [], isError: categoriesError } = useQuery({ queryKey: ['categorias'], queryFn: () => listAll<Categoria>('/categorias/') });

  const createMutation = useMutation({
    mutationFn: createProducto,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['productos'] });
      handleCloseModal();
    },
    onError: (err: Error) => {
      setModalError(err.message);
    },
  });

  const updateMutation = useMutation({
    mutationFn: updateProducto,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['productos'] });
      handleCloseModal();
    },
    onError: (err: Error) => {
      setModalError(err.message);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteProducto,
    onSuccess: () => {
      setPageAlert(null);
      queryClient.invalidateQueries({ queryKey: ['productos'] });
    },
    onError: (err: Error) => {
      setPageAlert(err.message);
    },
  });

  const form = useForm({
    defaultValues: {
      nombre: productoToEdit?.nombre ?? '',
      descripcion: productoToEdit?.descripcion ?? '',
      precio_base: productoToEdit?.precio_base ?? 0,
      disponible: productoToEdit?.disponible ?? true,
      categoria_ids: productoToEdit?.categoria_ids ?? [] as number[],
    },
    onSubmit: async ({ value }) => {
      setModalError(null);
      const payload: ProductoFormData = {
        nombre: value.nombre.trim(),
        descripcion: value.descripcion.trim(),
        precio_base: Number(value.precio_base),
        disponible: Boolean(value.disponible),
        categoria_ids: value.categoria_ids,
      };
      if (productoToEdit) {
        await updateMutation.mutateAsync({ id: productoToEdit.id, payload });
      } else {
        await createMutation.mutateAsync(payload);
      }
    },
  });

  const handleOpenCreate = () => {
    setProductoToEdit(null);
    setModalError(null);
    form.reset();
    form.setFieldValue('nombre', '');
    form.setFieldValue('descripcion', '');
    form.setFieldValue('precio_base', 0);
    form.setFieldValue('disponible', true);
    form.setFieldValue('categoria_ids', []);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (producto: Producto) => {
    setProductoToEdit(producto);
    setModalError(null);
    form.reset();
    form.setFieldValue('nombre', producto.nombre);
    form.setFieldValue('descripcion', producto.descripcion ?? '');
    form.setFieldValue('precio_base', producto.precio_base);
    form.setFieldValue('disponible', producto.disponible);
    form.setFieldValue('categoria_ids', producto.categoria_ids ?? []);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setProductoToEdit(null);
    setModalError(null);
    form.reset();
  };

  const handleDelete = (producto: Producto) => {
    if (window.confirm(`¿Estás segura de que querés eliminar el producto "${producto.nombre}"?`)) {
      deleteMutation.mutate(producto.id);
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
      columnHelper.display({ id: 'categorias', header: 'Categorías', cell: ({ row }) => (row.original.categoria_ids ?? []).map((id) => categorias.find((c) => c.id === id)?.nombre ?? `#${id}`).join(', ') || 'Sin categorías' }),
      columnHelper.accessor('precio_base', {
        header: 'Precio Base',
        cell: (info) => (
          <span className="font-semibold text-slate-900">
            ${Number(info.getValue()).toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </span>
        ),
      }),
      columnHelper.accessor('disponible', {
        header: 'Estado',
        cell: (info) =>
          info.getValue() ? (
            <span className="inline-flex items-center rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-medium text-emerald-700 border border-emerald-200">
              Disponible
            </span>
          ) : (
            <span className="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-600 border border-slate-200">
              No disponible
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
    data: productos,
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
          <h1 className="text-2xl font-bold text-slate-900">Gestión de Productos</h1>
          <p className="mt-1 text-sm text-slate-600">
            Administrá los productos del catálogo, sus precios y su disponibilidad.
          </p>
        </div>
        {isAdmin && (<button
          type="button"
          onClick={handleOpenCreate}
          className="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700 transition-colors"
        >
          <Plus className="h-4 w-4" />
          Nuevo producto
        </button>)}
      </div>

      <AlertBanner message={pageAlert} onClose={() => setPageAlert(null)} />

      {isLoading ? (
        <LoadingState message="Cargando productos..." />
      ) : isError ? (
        <ErrorState message={error.message} onRetry={() => refetch()} />
      ) : productos.length === 0 ? (
        <EmptyState
          title="No hay productos registrados"
          description="Agregá el primer producto al catálogo."
          actionLabel="Nuevo producto"
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
                placeholder="Filtrar productos por nombre o descripción..."
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
                {productoToEdit ? 'Editar producto' : 'Nuevo producto'}
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
                        ? 'El nombre del producto es obligatorio.'
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
                        placeholder="Ej. Pizza Napolitana"
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
                        placeholder="Descripción del producto..."
                        className="w-full rounded-lg border border-slate-300 px-3.5 py-2 text-sm text-slate-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
                      />
                    </div>
                  )}
                </form.Field>

                <form.Field
                  name="precio_base"
                  validators={{
                    onChange: ({ value }) =>
                      value === undefined || value === null || Number.isNaN(Number(value))
                        ? 'Ingresá un precio válido.'
                        : Number(value) < 0
                        ? 'El precio base no puede ser negativo.'
                        : undefined,
                  }}
                >
                  {(field) => (
                    <div>
                      <label htmlFor={field.name} className="block text-sm font-medium text-slate-700 mb-1">
                        Precio Base ($) <span className="text-red-500">*</span>
                      </label>
                      <input
                        id={field.name}
                        name={field.name}
                        type="number"
                        step="0.01"
                        min="0"
                        value={field.state.value}
                        onBlur={field.handleBlur}
                        onChange={(e) => field.handleChange(Number(e.target.value))}
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

                <form.Field name="categoria_ids">
                  {(field) => <fieldset className="rounded-lg border p-3"><legend className="text-sm font-medium">Categorías</legend>
                    <p className="mb-2 text-xs text-slate-500">La primera seleccionada será la principal.</p>
                    {categoriesError && <p role="alert" className="text-sm text-red-700">No se pudieron cargar las categorías. Reintentá desde el listado.</p>}
                    {categorias.map((categoria) => <label key={categoria.id} className="mr-3 inline-flex items-center gap-2 text-sm">
                      <input type="checkbox" checked={field.state.value.includes(categoria.id)} onChange={(event) => field.handleChange(event.target.checked ? [...field.state.value, categoria.id] : field.state.value.filter((id) => id !== categoria.id))} />
                      {categoria.nombre}{field.state.value[0] === categoria.id ? ' (principal)' : ''}
                    </label>)}
                  </fieldset>}
                </form.Field>

                <form.Field name="disponible">
                  {(field) => (
                    <div className="flex items-center gap-2.5 pt-1">
                      <input
                        id={field.name}
                        name={field.name}
                        type="checkbox"
                        checked={field.state.value}
                        onBlur={field.handleBlur}
                        onChange={(e) => field.handleChange(e.target.checked)}
                        className="h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
                      />
                      <label htmlFor={field.name} className="text-sm font-medium text-slate-700">
                        Producto disponible para la venta
                      </label>
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
                          : productoToEdit
                          ? 'Guardar cambios'
                          : 'Crear producto'}
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

export default ProductsPage;
