import { useState } from 'react';
import { useForm } from '@tanstack/react-form';
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
  const [error, setError] = useState('');

  const total = items.reduce(
    (sum, item) => sum + item.producto.precio_base * item.cantidad,
    0
  );

  const form = useForm({
    defaultValues: {
      direccion_entrega: '',
      forma_pago: 'EFECTIVO' as FormaPago,
      notas: '',
    },
    onSubmit: async ({ value }) => {
      setError('');
      if (create.isPending) return;
      if (items.length === 0) {
        setError('El carrito est? vac?o.');
        return;
      }
      const direccion = value.direccion_entrega.trim();
      if (direccion.length < 5 || direccion.length > 200) {
        setError('La direcci?n debe tener entre 5 y 200 caracteres.');
        return;
      }
      try {
        const pedido = await create.mutateAsync({
          items: items.map(({ producto, cantidad }) => ({
            producto_id: producto.id,
            cantidad,
          })),
          forma_pago: value.forma_pago,
          direccion_entrega: direccion,
          notas: value.notas.trim() || null,
        });
        clear();
        navigate('/pedidos', {
          replace: true,
          state: { creado: pedido.id },
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : 'No se pudo crear el pedido.');
      }
    },
  });

  if (items.length === 0) {
    return (
      <main className="mx-auto max-w-4xl space-y-5 px-4 py-8">
        <h1 className="text-2xl font-bold">Confirmar pedido</h1>
        <p>El carrito est? vac?o.</p>
        <Link to="/products" className="text-indigo-700 underline">Volver al cat?logo</Link>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-4xl space-y-6 px-4 py-8 text-slate-900">
      <h1 className="text-2xl font-bold">Confirmar pedido</h1>
      <section className="rounded-xl border bg-white p-5">
        <h2 className="mb-3 text-lg font-semibold">Resumen de la compra</h2>
        <ul className="space-y-2">
          {items.map(({ producto, cantidad }) => (
            <li key={producto.id} className="flex justify-between gap-3 text-sm">
              <span>{producto.nombre} x {cantidad}</span>
              <strong>{money(producto.precio_base * cantidad)}</strong>
            </li>
          ))}
        </ul>
        <p className="mt-4 border-t pt-3 text-right text-xl font-bold">
          Total estimado: {money(total)}
        </p>
        <Link to="/carrito" className="mt-3 inline-block text-sm text-indigo-700 underline">
          Modificar carrito
        </Link>
      </section>

      <form
        onSubmit={(event) => {
          event.preventDefault();
          event.stopPropagation();
          void form.handleSubmit();
        }}
        className="space-y-4 rounded-xl border bg-white p-5"
      >
        <h2 className="text-lg font-semibold">Datos de entrega</h2>
        <form.Field
          name="direccion_entrega"
          validators={{ onChange: ({ value }) => {
            const n = value.trim().length;
            return n < 5 || n > 200 ? 'La direcci?n debe tener entre 5 y 200 caracteres.' : undefined;
          } }}
        >
          {(field) => (
            <label className="block text-sm">
              Direcci?n de entrega
              <input
                className="mt-1 w-full rounded border p-2"
                value={field.state.value}
                onChange={(event) => field.handleChange(event.target.value)}
                onBlur={field.handleBlur}
                required minLength={5} maxLength={200}
              />
              {field.state.meta.errors.length > 0 && (
                <span className="block text-xs text-red-700">
                  {field.state.meta.errors.filter(Boolean).join(', ')}
                </span>
              )}
            </label>
          )}
        </form.Field>
        <form.Field name="forma_pago">
          {(field) => (
            <label className="block text-sm">
              Forma de pago
              <select
                className="mt-1 w-full rounded border p-2"
                value={field.state.value}
                onChange={(event) => field.handleChange(event.target.value as FormaPago)}
              >
                <option value="EFECTIVO">Efectivo</option>
                <option value="TRANSFERENCIA">Transferencia</option>
              </select>
            </label>
          )}
        </form.Field>
        <form.Field name="notas">
          {(field) => (
            <label className="block text-sm">
              Notas (opcional)
              <textarea
                className="mt-1 w-full rounded border p-2"
                value={field.state.value}
                onChange={(event) => field.handleChange(event.target.value)}
                onBlur={field.handleBlur}
              />
            </label>
          )}
        </form.Field>
        {error && <p role="alert" className="text-red-700">{error}</p>}
        <form.Subscribe selector={(state) => [state.canSubmit, state.isSubmitting] as const}>
          {([canSubmit, isSubmitting]) => (
            <button
              type="submit"
              disabled={!canSubmit || isSubmitting || create.isPending}
              className="rounded-lg bg-indigo-600 px-5 py-2 font-semibold text-white disabled:opacity-50"
            >
              {isSubmitting || create.isPending ? 'Procesando...' : 'Confirmar pedido'}
            </button>
          )}
        </form.Subscribe>
      </form>
    </main>
  );
}
