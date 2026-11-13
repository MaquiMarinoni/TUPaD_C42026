import { useState, type FormEvent } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCartStore } from '../store/cartStore';
import { useOrders } from '@/features/orders/hooks/useOrders';
import type { FormaPago } from '@/features/orders/types/pedido';

const money = (value: number) =>
  '$' + value.toLocaleString('es-AR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

export function CheckoutPage() {
  const items = useCartStore((state) => state.items);
  const clear = useCartStore((state) => state.clear);

  const { create } = useOrders();
  const navigate = useNavigate();

  const [direccion, setDireccion] = useState('');
  const [pago, setPago] = useState<FormaPago>('EFECTIVO');
  const [notas, setNotas] = useState('');
  const [error, setError] = useState('');

  const total = items.reduce(
    (sum, item) =>
      sum + item.producto.precio_base * item.cantidad,
    0
  );

  async function confirmarPedido(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');

    if (create.isPending) return;

    if (items.length === 0) {
      setError('El carrito esta vacio.');
      return;
    }

    if (direccion.trim().length < 5 || direccion.trim().length > 200) {
      setError('La direccion debe tener entre 5 y 200 caracteres.');
      return;
    }

    try {
      const pedido = await create.mutateAsync({
        items: items.map(({ producto, cantidad }) => ({
          producto_id: producto.id,
          cantidad,
        })),
        forma_pago: pago,
        direccion_entrega: direccion.trim(),
        notas: notas.trim() || null,
      });

      clear();

      navigate('/pedidos', {
        replace: true,
        state: { creado: pedido.id },
      });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'No se pudo crear el pedido.'
      );
    }
  }

  if (items.length === 0) {
    return (
      <main className="mx-auto max-w-4xl space-y-5 px-4 py-8">
        <h1 className="text-2xl font-bold">
          Confirmar pedido
        </h1>
        <p>El carrito esta vacio.</p>
        <Link to="/products" className="text-indigo-700 underline">
          Volver al catalogo
        </Link>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-4xl space-y-6 px-4 py-8 text-slate-900">
      <h1 className="text-2xl font-bold">
        Confirmar pedido
      </h1>

      <section className="rounded-xl border bg-white p-5">
        <h2 className="mb-3 text-lg font-semibold">
          Resumen de la compra
        </h2>

        <ul className="space-y-2">
          {items.map(({ producto, cantidad }) => (
            <li
              key={producto.id}
              className="flex justify-between gap-3 text-sm"
            >
              <span>
                {producto.nombre} x {cantidad}
              </span>
              <strong>
                {money(producto.precio_base * cantidad)}
              </strong>
            </li>
          ))}
        </ul>

        <p className="mt-4 border-t pt-3 text-right text-xl font-bold">
          Total estimado: {money(total)}
        </p>

        <Link
          to="/carrito"
          className="mt-3 inline-block text-sm text-indigo-700 underline"
        >
          Modificar carrito
        </Link>
      </section>

      <form
        onSubmit={(event) => void confirmarPedido(event)}
        className="space-y-4 rounded-xl border bg-white p-5"
      >
        <h2 className="text-lg font-semibold">
          Datos de entrega
        </h2>

        <label className="block text-sm">
          Direccion de entrega
          <input
            className="mt-1 w-full rounded border p-2"
            value={direccion}
            onChange={(event) => setDireccion(event.target.value)}
            required
            minLength={5}
            maxLength={200}
          />
        </label>

        <label className="block text-sm">
          Forma de pago
          <select
            className="mt-1 w-full rounded border p-2"
            value={pago}
            onChange={(event) =>
              setPago(event.target.value as FormaPago)
            }
          >
            <option value="EFECTIVO">Efectivo</option>
            <option value="TRANSFERENCIA">Transferencia</option>
          </select>
        </label>

        <label className="block text-sm">
          Notas (opcional)
          <textarea
            className="mt-1 w-full rounded border p-2"
            value={notas}
            onChange={(event) => setNotas(event.target.value)}
          />
        </label>

        {error && (
          <p role="alert" className="text-red-700">
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={create.isPending}
          className="rounded-lg bg-indigo-600 px-5 py-2 font-semibold text-white disabled:opacity-50"
        >
          {create.isPending
            ? 'Procesando...'
            : 'Confirmar pedido'}
        </button>
      </form>
    </main>
  );
}
