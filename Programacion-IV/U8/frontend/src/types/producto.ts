export interface Producto {
  id: number;
  nombre: string;
  descripcion: string;
  precio_base: number;
  imagenes_url: string[];
  disponible: boolean;
  categoria_ids?: number[];
}

export interface ProductoFormData {
  nombre: string;
  descripcion: string;
  precio_base: number;
  imagenes_url: string[];
  disponible: boolean;
  categoria_ids: number[];
}