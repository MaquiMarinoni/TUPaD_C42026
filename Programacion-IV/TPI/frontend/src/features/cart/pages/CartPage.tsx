import { Link } from 'react-router-dom';
import { useCartStore } from '../store/cartStore';

const money = (value: number) =>
  '$' + value.toLocaleString('es-AR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

export function CartPage() {
  const items = useCartStore((state) => state.items);
  const changeQuantity = useCartStore((state) => state.changeQuantity);
  const remove = useCartStore((state) => state.remove);

  const total = items.reduce(
    (sum, item) =>
      sum + item.producto.precio_base * item.cantidad,
    0
  );

  return (
    <main className="mx-auto max-w-4xl space-y-6 px-4 py-8 text-slate-900">
      <h1 className="text-2xl font-bold">
        Carrito de compras
      </h1>

      {items.length === 0 ? (
        <div className="rounded-xl border bg-white p-6">
          <p>No hay productos en el carrito.</p>
          <Link
            to="/products"
            className="mt-3 inline-block text-indigo-700 underline"
          >
            Ver catalogo
          </Link>
        </div>
      ) : (
        <>
          <div className="space-y-3">
            {items.map(({ producto, cantidad }) => (
              <div
                key={producto.id}
                className="flex flex-wrap items-center justify-between gap-3 rounded-xl border bg-white p-4"
              >
                <div>
                  <p className="font-semibold">
                    {producto.nombre}
                  </p>
                  <p className="text-sm text-slate-600">
                    {money(producto.precio_base)} por unidad
                  </p>
                  <p className="text-sm text-slate-600">
                    Stock: {producto.stock}
                  </p>
                </div>

                <div className="flex flex-wrap items-center gap-3">
                  <label className="text-sm">
                    Cantidad
                    <input
                      className="ml-2 w-20 rounded border p-2"
                      type="number"
                      min={1}
                      max={producto.stock}
                      value={cantidad}
                      onChange={(event) =>
                        changeQuantity(
                          producto.id,
                          Number(event.target.value)
                        )
                      }
                    />
                  </label>

                  <strong>
                    {money(producto.precio_base * cantidad)}
                  </strong>

                  <button
                    type="button"
                    className="rounded border px-3 py-2 text-red-700"
                    onClick={() => remove(producto.id)}
                  >
                    Quitar
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="rounded-xl border bg-white p-5">
            <p className="text-right text-xl font-bold">
              Total estimado: {money(total)}
            </p>

            <div className="mt-4 flex flex-wrap justify-end gap-3">
              <Link
                to="/products"
                className="rounded-lg border px-5 py-2"
              >
                Seguir comprando
              </Link>

              <Link
                to="/checkout"
                className="rounded-lg bg-indigo-600 px-5 py-2 font-semibold text-white"
              >
                Continuar con el pedido
              </Link>
            </div>
          </div>
        </>
      )}
    </main>
  );
}
