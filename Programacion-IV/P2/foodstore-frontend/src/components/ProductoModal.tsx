import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import type { Producto, ProductoFormData } from '../types/producto'
import type { UnidadMedida } from '../types/unidadMedida'

interface ProductoModalProps {
  producto: Producto | null
  unidades: UnidadMedida[]
  onGuardar: (datos: ProductoFormData) => Promise<void>
  onCerrar: () => void
  error: string | null
  guardando: boolean
}

const inicial: ProductoFormData = {
  nombre: '', descripcion: '', precio_base: 0,
  unidad_venta_id: 0, stock_cantidad: 0, disponible: true
}

export function ProductoModal({
  producto, unidades, onGuardar, onCerrar, error, guardando
}: ProductoModalProps) {
  const [form, setForm] = useState<ProductoFormData>(inicial)

  useEffect(() => {
    if (producto) {
      setForm({
        nombre: producto.nombre,
        descripcion: producto.descripcion,
        precio_base: Number(producto.precio_base),
        unidad_venta_id: producto.unidad_venta_id,
        stock_cantidad: Number(producto.stock_cantidad),
        disponible: producto.disponible
      })
    } else {
      setForm({ ...inicial, unidad_venta_id: unidades[0]?.id ?? 0 })
    }
  }, [producto, unidades])

  async function enviar(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    await onGuardar({ ...form, nombre: form.nombre.trim() })
  }

  const inputClass = 'mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-emerald-600 focus:outline-none focus:ring-1 focus:ring-emerald-600'

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/50 p-4">
      <section role="dialog" aria-modal="true" aria-label="Formulario de producto"
        className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-xl">
        <h2 className="mb-5 text-xl font-bold">{producto ? 'Editar producto' : 'Nuevo producto'}</h2>
        <form onSubmit={enviar} className="space-y-4">
          <label className="block text-sm font-medium">
            Nombre
            <input className={inputClass} required minLength={3}
              value={form.nombre} onChange={e => setForm({ ...form, nombre: e.target.value })} />
          </label>
          <label className="block text-sm font-medium">
            Descripción
            <textarea className={inputClass} rows={2}
              value={form.descripcion ?? ''}
              onChange={e => setForm({ ...form, descripcion: e.target.value })} />
          </label>
          <div className="grid grid-cols-2 gap-4">
            <label className="block text-sm font-medium">
              Precio base
              <input className={inputClass} type="number" step="0.01" min="0" required
                value={form.precio_base}
                onChange={e => setForm({ ...form, precio_base: Number(e.target.value) })} />
            </label>
            <label className="block text-sm font-medium">
              Stock
              <input className={inputClass} type="number"
                step={unidades.find(u => u.id === form.unidad_venta_id)?.tipo === 'contable' ? '1' : '0.001'}
                min="0" required value={form.stock_cantidad}
                onChange={e => setForm({ ...form, stock_cantidad: Number(e.target.value) })} />
            </label>
          </div>
          <label className="block text-sm font-medium">
            Unidad de venta
            <select className={inputClass} required value={form.unidad_venta_id}
              onChange={e => setForm({ ...form, unidad_venta_id: Number(e.target.value) })}>
              {unidades.map(u => (
                <option value={u.id} key={u.id}>{u.nombre} ({u.simbolo})</option>
              ))}
            </select>
          </label>
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" checked={form.disponible}
              onChange={e => setForm({ ...form, disponible: e.target.checked })} />
            Disponible para la venta
          </label>
          {error && <p role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
          <div className="flex justify-end gap-3 pt-3">
            <button type="button" onClick={onCerrar} disabled={guardando}
              className="rounded-lg border px-4 py-2 hover:bg-slate-100 disabled:opacity-50">Cancelar</button>
            <button type="submit" disabled={guardando || unidades.length === 0}
              className="rounded-lg bg-emerald-700 px-4 py-2 font-medium text-white hover:bg-emerald-800 disabled:opacity-50">
              {guardando ? 'Guardando...' : 'Guardar'}
            </button>
          </div>
        </form>
      </section>
    </div>
  )
}
