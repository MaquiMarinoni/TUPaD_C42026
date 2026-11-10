
import type { UnidadMedida } from './unidadMedida'
import type { CategoriaProducto } from './categoria'

export interface Producto {
  id: number
  nombre: string
  descripcion: string | null
  precio_base: string
  unidad_venta_id: number
  unidad_venta: UnidadMedida
  stock_cantidad: string
  disponible: boolean
  activo: boolean
  anulado_at: string | null
  categorias: CategoriaProducto[]
  hay_stock: boolean
}

export interface ProductoFormData {
  nombre: string
  descripcion: string | null
  precio_base: number
  unidad_venta_id: number
  stock_cantidad: number
  disponible: boolean
}
