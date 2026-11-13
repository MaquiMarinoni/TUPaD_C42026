export type EstadoPedido = 'PENDIENTE' | 'EN_PREPARACION' | 'ENTREGADO' | 'CANCELADO';
export type FormaPago = 'EFECTIVO' | 'TRANSFERENCIA';
export interface PedidoCrear {
  items: { producto_id: number; cantidad: number }[];
  forma_pago: FormaPago;
  direccion_entrega: string;
  notas: string | null;
}
export interface DetallePedido { id: number; producto_id: number; cantidad: number; nombre_producto: string; precio_unitario: number; subtotal: number }
export interface Pedido {
  id: number; usuario_id: number; estado: EstadoPedido; forma_pago: FormaPago;
  direccion_entrega: string; notas: string | null; total: number;
  created_at: string; updated_at: string; items: DetallePedido[];
}
export interface PedidosPaginados { total: number; items: Pedido[] }
