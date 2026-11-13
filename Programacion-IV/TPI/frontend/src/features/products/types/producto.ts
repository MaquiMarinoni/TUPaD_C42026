
export interface Producto {
  id: number;
  categoria_id: number;
  nombre: string;
  descripcion: string | null;
  precio_base: number;
  imagen_url: string | null;
  stock: number;
  disponible: boolean;
  activo: boolean;
  categoria: { id: number; nombre: string; descripcion: string | null; activo: boolean };
}

export interface ProductoFormData {
  categoria_id: number;
  nombre: string;
  descripcion: string;
  precio_base: number;
  imagen_url: string | null;
  stock: number;
  disponible: boolean;
}
