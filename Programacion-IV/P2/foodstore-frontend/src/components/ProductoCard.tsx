import type { Producto } from '../types/producto'

interface ProductoCardProps {
  producto: Producto
  onEditar: (producto: Producto) => void
  onDisponibilidad: (producto: Producto) => void
  onAnular: (producto: Producto) => void
  procesando: boolean
}

export function ProductoCard({
  producto, onEditar, onDisponibilidad, onAnular, procesando
}: ProductoCardProps) {
  const precio = Number(producto.precio_base).toLocaleString('es-AR', {
    minimumFractionDigits: 2, maximumFractionDigits: 2
  })
  const stock = Number(producto.stock_cantidad).toLocaleString('es-AR', {
    maximumFractionDigits: 3
  })
  const simbolo = producto.unidad_venta.simbolo

  return (
    <article className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-3 flex items-start justify-between gap-3">
        <div>
          <h3 className="text-lg font-bold text-slate-800">{producto.nombre}</h3>
          <p className="mt-1 text-sm text-slate-500">{producto.descripcion || 'Sin descripción'}</p>
        </div>
        <span className="shrink-0 rounded bg-slate-100 px-2 py-1 text-xs text-slate-600">#{producto.id}</span>
      </div>

      <p className="text-xl font-semibold text-emerald-700">$ {precio} / {simbolo}</p>
      <p className="mt-1 text-sm text-slate-600">Stock: {stock} {simbolo}</p>

      <div className="mt-3 flex flex-wrap gap-2 text-xs font-medium">
        <span className={`rounded-full px-3 py-1 ${producto.disponible ? 'bg-green-100 text-green-800' : 'bg-amber-100 text-amber-800'}`}>
          {producto.disponible ? 'Venta habilitada' : 'Venta pausada'}
        </span>
        <span className={`rounded-full px-3 py-1 ${producto.hay_stock ? 'bg-blue-100 text-blue-800' : 'bg-red-100 text-red-700'}`}>
          {producto.hay_stock ? 'Con stock' : 'Sin stock'}
        </span>
      </div>

      <div className="mt-5 flex flex-wrap gap-2 border-t border-slate-100 pt-4">
        <button disabled={procesando} onClick={() => onEditar(producto)}
          className="rounded-lg bg-slate-100 px-3 py-2 text-sm hover:bg-slate-200 disabled:opacity-50">
          Editar
        </button>
        <button disabled={procesando} onClick={() => onDisponibilidad(producto)}
          className="rounded-lg bg-blue-50 px-3 py-2 text-sm text-blue-800 hover:bg-blue-100 disabled:opacity-50">
          {producto.disponible ? 'Pausar venta' : 'Habilitar venta'}
        </button>
        <button disabled={procesando} onClick={() => onAnular(producto)}
          className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700 hover:bg-red-100 disabled:opacity-50">
          Anular
        </button>
      </div>
    </article>
  )
}
