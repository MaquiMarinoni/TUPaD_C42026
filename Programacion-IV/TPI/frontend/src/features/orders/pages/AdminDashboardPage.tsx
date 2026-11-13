import { useQuery } from '@tanstack/react-query';
import { axiosInstance } from '@/shared/api/api';

interface PedidoResumen {
  total_pedidos: number;
  pendientes: number;
  en_preparacion: number;
  entregados: number;
  cancelados: number;
  pedidos_hoy: number;
  ingresos_entregados: number;
}

const money = new Intl.NumberFormat('es-AR', {
  style: 'currency',
  currency: 'ARS',
});

export function AdminDashboardPage() {
  const { data, isLoading, isError, error, refetch, isFetching } =
    useQuery<PedidoResumen, Error>({
      queryKey: ['admin', 'pedidos', 'resumen'],
      queryFn: async () =>
        (await axiosInstance.get<PedidoResumen>('/pedidos/resumen')).data,
      staleTime: 30_000,
    });

  const cards = data ? [
    { title: 'Pendientes', value: data.pendientes },
    { title: 'En preparaci?n', value: data.en_preparacion },
    { title: 'Entregados', value: data.entregados },
    { title: 'Cancelados', value: data.cancelados },
    { title: 'Pedidos de hoy', value: data.pedidos_hoy },
    { title: 'Ingresos entregados', value: money.format(data.ingresos_entregados) },
  ] : [];

  return (
    <main className="mx-auto max-w-6xl space-y-6 px-6 py-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">
            Resumen administrativo
          </h1>
          <p className="mt-1 text-sm text-slate-600">
            Indicadores generales de pedidos de FoodStore.
          </p>
        </div>
        <button
          type="button"
          onClick={() => void refetch()}
          disabled={isFetching}
          className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
        >
          {isFetching ? 'Actualizando...' : 'Actualizar datos'}
        </button>
      </div>

      {isLoading && <p role="status">Cargando indicadores...</p>}

      {isError && (
        <p role="alert" className="text-red-700">
          No se pudo cargar el resumen: {error.message}
        </p>
      )}

      {data && (
        <>
          <section className="rounded-xl border border-indigo-200 bg-indigo-50 p-5">
            <h2 className="text-sm font-medium text-indigo-700">
              Total de pedidos registrados
            </h2>
            <p className="mt-2 text-3xl font-bold text-indigo-900">
              {data.total_pedidos}
            </p>
          </section>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {cards.map((card) => (
              <section
                key={card.title}
                className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
              >
                <h2 className="text-sm font-medium text-slate-600">
                  {card.title}
                </h2>
                <p className="mt-3 text-2xl font-bold text-slate-900">
                  {card.value}
                </p>
              </section>
            ))}
          </div>
        </>
      )}
    </main>
  );
}
