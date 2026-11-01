export interface Producto {
  id: number;
  nombre: string;
  descripcion: string;
  precio_base: number;
  disponible: boolean;
  imagenes_url?: string[];
  categoria_ids?: number[];
}

export interface ProductoFormData {
  categoria_ids: number[];
  nombre: string;
  descripcion: string;
  precio_base: number;
  disponible: boolean;
}
