
export interface Categoria {
  id: number
  nombre: string
  descripcion: string | null
  activo: boolean
  anulado_at: string | null
}

export interface CategoriaProducto extends Categoria {
  es_principal: boolean
}
