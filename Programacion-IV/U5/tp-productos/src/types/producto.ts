export type Producto = {
  id: number;
  nombre: string;
  categoria: string;
  precio: number;
  stock: number;
  stock_minimo: number;
  activo: boolean;
};