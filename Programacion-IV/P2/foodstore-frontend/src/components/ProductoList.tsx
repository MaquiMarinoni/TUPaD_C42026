import type { Producto } from '../types/producto'
import { ProductoCard } from './ProductoCard'

interface ProductoListProps {
  productos: Producto[]
  onEditar: (producto: Producto) => void
  onDisponibilidad: (producto: Producto) => void
  onAnular: (producto: Producto) => void
  procesando: boolean
}

export function ProductoList(props: ProductoListProps) {
  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      {props.productos.map(producto => (
        <ProductoCard
          key={producto.id}
          producto={producto}
          onEditar={props.onEditar}
          onDisponibilidad={props.onDisponibilidad}
          onAnular={props.onAnular}
          procesando={props.procesando}
        />
      ))}
    </div>
  )
}
