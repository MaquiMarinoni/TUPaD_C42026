import { useCartStore } from '@/features/cart/store/cartStore';
import { useCategories } from '@/features/categories';
import { useAuthStore } from '@/features/auth';
import { useProducts } from '../hooks/useProducts';
import { useCatalogo } from '../hooks/useCatalogo';
import { useEffect, useState } from 'react';
import { useForm } from '@tanstack/react-form';
import {
  createColumnHelper, flexRender, getCoreRowModel,
  getSortedRowModel,
  useReactTable, type SortingState, type PaginationState,
} from '@tanstack/react-table';
import { Pencil, Plus, Trash2, Search, ChevronLeft, ChevronRight, X } from 'lucide-react';
import type { Producto, ProductoFormData } from '@/features/products';
import { AlertBanner, ErrorState } from '@/shared/components/StatusStates';

const columnHelper = createColumnHelper<Producto>();
const emptyValues: ProductoFormData = {
  categoria_id: 0, nombre: '', descripcion: '', precio_base: 0,
  imagen_url: null, stock: 0, disponible: true,
};

export function ProductsPage() {
  const isAdmin = useAuthStore((state) => state.user?.role === 'admin');
  const addToCart = useCartStore((state) => state.add);
  const [editing, setEditing] = useState<Producto | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);
  const [pageAlert, setPageAlert] = useState<string | null>(null);
  const [sorting, setSorting] = useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = useState('');
  const [busquedaAplicada, setBusquedaAplicada] = useState('');

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setBusquedaAplicada(globalFilter);
    }, 1000);

    return () => window.clearTimeout(timer);
  }, [globalFilter]);
  const [categoriaFiltro, setCategoriaFiltro] = useState<number | undefined>();
  const [pagination, setPagination] = useState<PaginationState>({
    pageIndex: 0,
    pageSize: 5,
  });
  const { data: categorias = [], isError: categoriesError } = useCategories();
  const closeModal = () => { setModalOpen(false); setEditing(null); setModalError(null); };
  const {
    createMutation, updateMutation, deleteMutation,
  } = useProducts({
    enabled: false,
    onSaved: closeModal,
    onSaveError: (err) => setModalError(err.message),
    onDeleted: () => setPageAlert(null),
    onDeleteError: (err) => setPageAlert(err.message),
  });
  const {
    data: catalogo,
    isLoading,
    isError,
    error,
    refetch,
  } = useCatalogo({
    skip: pagination.pageIndex * pagination.pageSize,
    limit: pagination.pageSize,
    search: busquedaAplicada,
    categoria_id: categoriaFiltro,
  });

  const productos = catalogo?.items ?? [];
  const totalProductos = catalogo?.total ?? 0;

  const form = useForm({
    defaultValues: emptyValues,
    onSubmit: async ({ value }) => {
      setModalError(null);
      const payload: ProductoFormData = {
        categoria_id: Number(value.categoria_id),
        nombre: value.nombre.trim(),
        descripcion: value.descripcion.trim(),
        precio_base: Number(value.precio_base),
        imagen_url: value.imagen_url?.trim() || null,
        stock: Number(value.stock),
        disponible: Boolean(value.disponible),
      };
      if (!payload.categoria_id || !payload.nombre || !Number.isFinite(payload.precio_base) || payload.precio_base < 0 || !Number.isInteger(payload.stock) || payload.stock < 0) {
        setModalError('Revisá categoría, nombre, precio y stock.');
        return;
      }
      if (editing) await updateMutation.mutateAsync({ id: editing.id, payload });
      else await createMutation.mutateAsync(payload);
    },
  });
  const openCreate = () => {
    setEditing(null); setModalError(null); form.reset();
    form.setFieldValue('categoria_id', 0);
    form.setFieldValue('nombre', '');
    form.setFieldValue('descripcion', '');
    form.setFieldValue('precio_base', 0);
    form.setFieldValue('imagen_url', null);
    form.setFieldValue('stock', 0);
    form.setFieldValue('disponible', true);
    setModalOpen(true);
  };
  const openEdit = (producto: Producto) => {
    setEditing(producto); setModalError(null); form.reset();
    form.setFieldValue('categoria_id', producto.categoria_id);
    form.setFieldValue('nombre', producto.nombre);
    form.setFieldValue('descripcion', producto.descripcion ?? '');
    form.setFieldValue('precio_base', Number(producto.precio_base));
    form.setFieldValue('imagen_url', producto.imagen_url);
    form.setFieldValue('stock', producto.stock);
    form.setFieldValue('disponible', producto.disponible);
    setModalOpen(true);
  };
  const handleDelete = (producto: Producto) => {
    if (window.confirm(`¿Eliminar el producto "${producto.nombre}"?`)) deleteMutation.mutate(producto.id);
  };
  const columns = [
    columnHelper.accessor('id', { header: 'ID', cell: (info) => `#${info.getValue()}` }),
    columnHelper.accessor('nombre', { header: 'Nombre', cell: (info) => <strong>{info.getValue()}</strong> }),
    columnHelper.accessor('categoria_id', {
      header: 'Categoría',
      cell: (info) => categorias.find((c) => c.id === info.getValue())?.nombre ?? `#${info.getValue()}`,
    }),
    columnHelper.accessor('precio_base', {
      header: 'Precio', cell: (info) => `$${Number(info.getValue()).toLocaleString('es-AR', { minimumFractionDigits: 2 })}`,
    }),
    columnHelper.accessor('stock', { header: 'Stock' }),
    columnHelper.accessor('disponible', { header: 'Disponible', cell: (info) => info.getValue() ? 'Sí' : 'No' }),
    columnHelper.display({
      id: 'carrito', header: 'Comprar', enableSorting: false,
      cell: ({ row }) => <button type="button" disabled={!row.original.activo || !row.original.disponible || row.original.stock < 1}
        onClick={() => addToCart(row.original)} className="rounded bg-indigo-600 px-3 py-2 text-xs font-semibold text-white disabled:cursor-not-allowed disabled:opacity-40">Agregar al carrito</button>,
    }),
    columnHelper.display({
      id: 'acciones', header: 'Acciones', enableSorting: false,
      cell: ({ row }) => <div className="flex gap-2">
        <button type="button" onClick={() => openEdit(row.original)} className="rounded border px-2 py-1 text-indigo-700"><Pencil className="inline h-4 w-4" /> Editar</button>
        <button type="button" onClick={() => handleDelete(row.original)} className="rounded border px-2 py-1 text-red-700"><Trash2 className="inline h-4 w-4" /> Eliminar</button>
      </div>,
    }),
  ];
  // TanStack Table administra su estado.
  // oxlint-disable-next-line react/incompatible-library
  const table = useReactTable({
    data: productos, columns,
    state: { sorting, pagination, columnVisibility: { acciones: isAdmin } },
    onSortingChange: setSorting,
    onPaginationChange: setPagination,
    manualPagination: true,
    pageCount: Math.max(1, Math.ceil(totalProductos / pagination.pageSize)),
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });
  const inputClass = 'w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900';
  return <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
    <div className="mb-6 flex items-center justify-between gap-4">
      <div><h1 className="text-2xl font-bold text-slate-900">Gestión de Productos</h1>
        <p className="text-sm text-slate-600">Catálogo, precios, stock y disponibilidad.</p></div>
      {isAdmin && <button type="button" onClick={openCreate} className="rounded-xl bg-indigo-600 px-4 py-2 text-white"><Plus className="inline h-4 w-4" /> Nuevo producto</button>}
    </div>
    <AlertBanner message={pageAlert} onClose={() => setPageAlert(null)} />
    {isLoading && (
      <p role="status" className="mb-3 text-sm text-slate-600">
        Actualizando productos...
      </p>
    )}
    {isError && (
      <ErrorState
        message={error?.message ?? 'Error al cargar productos'}
        onRetry={() => { void refetch(); }}
      />
    )}
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
        <div className="relative mb-4"><Search className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
          <input className={`${inputClass} pl-9`} placeholder="Buscar productos..." value={globalFilter} onChange={(e) => {
            setGlobalFilter(e.target.value);
            setPagination((current) => ({ ...current, pageIndex: 0 }));
          }} /></div>
        <div className="mb-4 flex flex-wrap items-center gap-3">
          <label
            className="text-sm text-slate-700"
            htmlFor="filtro-categoria"
          >
            Categoria
          </label>
          <select
            id="filtro-categoria"
            className="rounded-lg border border-slate-300 px-3 py-2 text-sm"
            value={categoriaFiltro ?? ''}
            onChange={(e) => {
              setCategoriaFiltro(
                e.target.value ? Number(e.target.value) : undefined
              );
              setPagination((current) => ({ ...current, pageIndex: 0 }));
            }}
          >
            <option value="">Todas las categorias</option>
            {categorias.filter((c) => c.activo).map((c) => (
              <option key={c.id} value={c.id}>
                {c.nombre}
              </option>
            ))}
          </select>

          <span className="text-sm text-slate-600">
            {totalProductos} productos encontrados
          </span>
        </div>

        {productos.length === 0 && (
          <p className="rounded-lg bg-slate-50 p-4 text-sm text-slate-600">
            No hay productos que coincidan con los filtros.
          </p>
        )}

        <div className="overflow-x-auto"><table className="min-w-full divide-y divide-slate-200 text-sm">
          <thead className="bg-slate-50">{table.getHeaderGroups().map((group) => <tr key={group.id}>{group.headers.map((header) =>
            <th key={header.id} className="cursor-pointer px-4 py-3 text-left" onClick={header.column.getToggleSortingHandler()}>
              {flexRender(header.column.columnDef.header, header.getContext())}</th>)}</tr>)}</thead>
          <tbody className="divide-y divide-slate-100">{table.getRowModel().rows.map((row) => <tr key={row.id}>{row.getVisibleCells().map((cell) =>
            <td key={cell.id} className="px-4 py-3">{flexRender(cell.column.columnDef.cell, cell.getContext())}</td>)}</tr>)}</tbody>
        </table></div>
        <div className="mt-4 flex items-center justify-between text-sm">
          <span>Página {table.getState().pagination.pageIndex + 1} de {Math.max(1, table.getPageCount())}</span>
          <div className="flex gap-2"><button type="button" className="rounded border px-3 py-1 disabled:opacity-40" disabled={!table.getCanPreviousPage()} onClick={() => table.previousPage()}><ChevronLeft className="inline h-4 w-4" /> Anterior</button>
          <button type="button" className="rounded border px-3 py-1 disabled:opacity-40" disabled={!table.getCanNextPage()} onClick={() => table.nextPage()}>Siguiente <ChevronRight className="inline h-4 w-4" /></button></div>
        </div>
      </div>
    {isAdmin && modalOpen && <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4">
      <div className="max-h-[90vh] w-full max-w-lg overflow-y-auto rounded-2xl bg-white p-6 shadow-xl">
        <div className="mb-4 flex items-center justify-between"><h2 className="text-lg font-semibold">{editing ? 'Editar producto' : 'Nuevo producto'}</h2>
          <button type="button" onClick={closeModal} aria-label="Cerrar"><X className="h-5 w-5" /></button></div>
        {modalError && <p role="alert" className="mb-3 rounded bg-red-50 p-3 text-sm text-red-700">{modalError}</p>}
        <form onSubmit={(e) => { e.preventDefault(); e.stopPropagation(); void form.handleSubmit(); }} className="space-y-4">
          <form.Field name="nombre">{(field) => <label className="block text-sm">Nombre *<input className={inputClass} required value={field.state.value} onChange={(e) => field.handleChange(e.target.value)} /></label>}</form.Field>
          <form.Field name="descripcion">{(field) => <label className="block text-sm">Descripción<textarea className={inputClass} value={field.state.value} onChange={(e) => field.handleChange(e.target.value)} /></label>}</form.Field>
          <form.Field name="categoria_id">{(field) => <label className="block text-sm">Categoría *
            <select className={inputClass} required value={field.state.value || ''} onChange={(e) => field.handleChange(Number(e.target.value))}>
              <option value="">Seleccionar categoría</option>
              {categorias.filter((c) => c.activo || c.id === editing?.categoria_id).map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
            </select>{categoriesError && <span className="text-red-600">No se pudieron cargar las categorías.</span>}</label>}</form.Field>
          <form.Field name="precio_base">{(field) => <label className="block text-sm">Precio ($) *<input className={inputClass} type="number" min="0" step="0.01" required value={field.state.value} onChange={(e) => field.handleChange(Number(e.target.value))} /></label>}</form.Field>
          <form.Field name="stock">{(field) => <label className="block text-sm">Stock *<input className={inputClass} type="number" min="0" step="1" required value={field.state.value} onChange={(e) => field.handleChange(Number(e.target.value))} /></label>}</form.Field>
          <form.Field name="imagen_url">{(field) => <label className="block text-sm">URL de imagen<input className={inputClass} type="url" value={field.state.value ?? ''} onChange={(e) => field.handleChange(e.target.value)} placeholder="https://..." /></label>}</form.Field>
          <form.Field name="disponible">{(field) => <label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={field.state.value} onChange={(e) => field.handleChange(e.target.checked)} /> Disponible para la venta</label>}</form.Field>
          <div className="flex justify-end gap-3 border-t pt-4"><button type="button" onClick={closeModal} className="rounded border px-4 py-2">Cancelar</button>
            <button type="submit" disabled={createMutation.isPending || updateMutation.isPending} className="rounded bg-indigo-600 px-4 py-2 text-white disabled:opacity-50">{editing ? 'Guardar cambios' : 'Crear producto'}</button></div>
        </form>
      </div>
    </div>}
  </div>;
}
export default ProductsPage;