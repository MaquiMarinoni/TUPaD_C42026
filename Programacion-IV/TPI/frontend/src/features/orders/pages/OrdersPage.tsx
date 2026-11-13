import { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useAuthStore } from '@/features/auth';
import { useOrders } from '../hooks/useOrders';
import type { EstadoPedido } from '../types/pedido';
const money = (n: number) => '$' + n.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
export function OrdersPage() {
  const isAdmin = useAuthStore((s) => s.user?.role === 'admin');
  const { data = [], isLoading, error, refetch, changeStatus, cancel } = useOrders();
  const location = useLocation();
  const creado = (location.state as { creado?: number } | null)?.creado;
  const [message, setMessage] = useState('');
  async function setStatus(id: number, estado: EstadoPedido) {
    setMessage('');
    try { await changeStatus.mutateAsync({ id, estado }); }
    catch (err) { setMessage(err instanceof Error ? err.message : 'No se pudo actualizar el estado.'); }
  }
  async function cancelOrder(id: number) {
    setMessage('');
    if (!window.confirm(`Cancelar el pedido #${id}?`)) return;
    try { await cancel.mutateAsync(id); }
    catch (err) { setMessage(err instanceof Error ? err.message : 'No se pudo cancelar el pedido.'); }
  }
  return <main className="mx-auto max-w-5xl space-y-5 px-4 py-8 text-slate-900">
    <h1 className="text-2xl font-bold">{isAdmin ? 'Gestión de pedidos' : 'Mis pedidos'}</h1>
    {creado && <p className="rounded-lg border border-green-200 bg-green-50 p-3 text-green-800">Pedido #{creado} creado correctamente.</p>}
    {message && <p role="alert" className="rounded-lg bg-red-50 p-3 text-red-700">{message}</p>}
    {isLoading ? <p>Cargando pedidos...</p> : error ? <div><p role="alert">{error.message}</p><button onClick={() => void refetch()} className="underline">Reintentar</button></div> : !data.length ? <p>No hay pedidos registrados.</p> : data.map((pedido) => <section key={pedido.id} className="space-y-3 rounded-xl border bg-white p-5">
      <div className="flex flex-wrap justify-between gap-2"><div><h2 className="font-bold">Pedido #{pedido.id}</h2><p className="text-sm text-slate-600">{new Date(pedido.created_at).toLocaleString('es-AR')} | {pedido.estado} | {pedido.forma_pago}</p></div><strong>{money(pedido.total)}</strong></div>
      <p className="text-sm">Entrega: {pedido.direccion_entrega}</p>
      <ul className="list-inside list-disc text-sm">{pedido.items.map((item) => <li key={item.id}>{item.nombre_producto} - Cantidad: {item.cantidad} - Subtotal: {money(item.subtotal)}</li>)}</ul>
      {pedido.notas && <p className="text-sm">Notas: {pedido.notas}</p>}
      <div className="flex flex-wrap gap-2">
        {isAdmin && pedido.estado === 'PENDIENTE' && <button className="rounded border px-3 py-2" disabled={changeStatus.isPending} onClick={() => void setStatus(pedido.id, 'EN_PREPARACION')}>Iniciar preparaci?n</button>}
        {isAdmin && pedido.estado === 'EN_PREPARACION' && <button className="rounded border px-3 py-2" disabled={changeStatus.isPending} onClick={() => void setStatus(pedido.id, 'ENTREGADO')}>Marcar entregado</button>}
        {pedido.estado === 'PENDIENTE' && <button className="rounded border border-red-200 px-3 py-2 text-red-700" disabled={cancel.isPending} onClick={() => void cancelOrder(pedido.id)}>Cancelar</button>}
      </div>
    </section>)}
  </main>;
}
