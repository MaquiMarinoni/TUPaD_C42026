import { useEffect, useState } from 'react'
import { Navbar } from './components/Navbar'
import { ProductoList } from './components/ProductoList'
import { ProductoModal } from './components/ProductoModal'
import type { Producto, ProductoFormData } from './types/producto'
import type { UnidadMedida } from './types/unidadMedida'

const API = 'http://127.0.0.1:8000/api/v1'

async function solicitar<T>(ruta: string, opciones?: RequestInit): Promise<T> {
  const respuesta = await fetch(`${API}${ruta}`, {
    ...opciones,
    headers: { 'Content-Type': 'application/json', ...opciones?.headers }
  })

  if (!respuesta.ok) {
    let mensaje = `Error HTTP ${respuesta.status}`
    try {
      const datos: { detail?: unknown } = await respuesta.json()
      if (typeof datos.detail === 'string') mensaje = datos.detail
    } catch {
      // Se conserva el mensaje HTTP predeterminado
    }
    throw new Error(mensaje)
  }

  if (respuesta.status === 204) return undefined as T
  return respuesta.json() as Promise<T>
}

export default function App() {
  const [productos, setProductos] = useState<Producto[]>([])
  const [unidades, setUnidades] = useState<UnidadMedida[]>([])
  const [modalAbierto, setModalAbierto] = useState(false)
  const [seleccionado, setSeleccionado] = useState<Producto | null>(null)
  const [cargando, setCargando] = useState(true)
  const [procesando, setProcesando] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [errorModal, setErrorModal] = useState<string | null>(null)

  async function cargarCatalogo() {
    // El backend devuelve como máximo 50 productos por consulta.
    const todos: Producto[] = []
    let skip = 0
    while (true) {
      const pagina = await solicitar<Producto[]>(`/productos?skip=${skip}&limit=50`)
      todos.push(...pagina)
      if (pagina.length < 50) break
      skip += 50
    }
    setProductos(todos)
  }

  useEffect(() => {
    let vigente = true
    async function cargar() {
      try {
        const unidadesApi = await solicitar<UnidadMedida[]>('/unidades-medida')
        if (!vigente) return
        setUnidades(unidadesApi)

        const todos: Producto[] = []
        let skip = 0
        while (true) {
          const pagina = await solicitar<Producto[]>(`/productos?skip=${skip}&limit=50`)
          todos.push(...pagina)
          if (pagina.length < 50) break
          skip += 50
        }
        if (vigente) setProductos(todos)
      } catch (e) {
        if (vigente) setError(e instanceof Error ? e.message : 'Error de conexión')
      } finally {
        if (vigente) setCargando(false)
      }
    }
    void cargar()
    return () => { vigente = false }
  }, [])

  function abrirCrear() {
    setSeleccionado(null)
    setErrorModal(null)
    setModalAbierto(true)
  }

  function abrirEditar(producto: Producto) {
    setSeleccionado(producto)
    setErrorModal(null)
    setModalAbierto(true)
  }

  async function guardar(datos: ProductoFormData) {
    setProcesando(true)
    setErrorModal(null)
    try {
      const ruta = seleccionado ? `/productos/${seleccionado.id}` : '/productos'
      await solicitar<Producto>(ruta, {
        method: seleccionado ? 'PUT' : 'POST',
        body: JSON.stringify(datos)
      })
      await cargarCatalogo()
      setModalAbierto(false)
      setSeleccionado(null)
      setError(null)
    } catch (e) {
      setErrorModal(e instanceof Error ? e.message : 'No se pudo guardar')
    } finally {
      setProcesando(false)
    }
  }

  async function cambiarDisponibilidad(producto: Producto) {
    setProcesando(true)
    try {
      await solicitar<Producto>(`/productos/${producto.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          nombre: producto.nombre,
          descripcion: producto.descripcion,
          precio_base: Number(producto.precio_base),
          unidad_venta_id: producto.unidad_venta_id,
          stock_cantidad: Number(producto.stock_cantidad),
          disponible: !producto.disponible
        })
      })
      await cargarCatalogo()
      setError(null)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'No se pudo cambiar la disponibilidad')
    } finally {
      setProcesando(false)
    }
  }

  async function anular(producto: Producto) {
    if (!window.confirm(`¿Anular el producto "${producto.nombre}"?`)) return
    setProcesando(true)
    try {
      await solicitar<void>(`/productos/${producto.id}`, { method: 'DELETE' })
      await cargarCatalogo()
      setError(null)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'No se pudo anular')
    } finally {
      setProcesando(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar cantidad={productos.length} onCrear={abrirCrear} />
      <main className="mx-auto max-w-6xl px-5 py-8">
        <h2 className="mb-5 text-2xl font-bold text-slate-800">Catálogo de productos</h2>

        {error && (
          <div role="alert" className="mb-5 rounded-lg bg-red-50 p-4 text-red-700">
            {error}
            <button onClick={() => {
              setCargando(true)
              void cargarCatalogo().then(() => setError(null))
                .catch(e => setError(e instanceof Error ? e.message : 'Error'))
                .finally(() => setCargando(false))
            }} className="ml-3 font-semibold underline">Reintentar</button>
          </div>
        )}

        {cargando ? (
          <p className="py-10 text-center text-slate-500">Cargando productos...</p>
        ) : productos.length === 0 && !error ? (
          <div className="rounded-xl bg-white p-10 text-center text-slate-500 shadow-sm">
            No hay productos activos. Podés agregar el primero con el botón Nuevo producto.
          </div>
        ) : (
          <ProductoList productos={productos} onEditar={abrirEditar}
            onDisponibilidad={cambiarDisponibilidad} onAnular={anular}
            procesando={procesando} />
        )}
      </main>

      {modalAbierto && (
        <ProductoModal
          producto={seleccionado}
          unidades={unidades}
          onGuardar={guardar}
          onCerrar={() => { setModalAbierto(false); setErrorModal(null) }}
          error={errorModal}
          guardando={procesando}
        />
      )}
    </div>
  )
}
