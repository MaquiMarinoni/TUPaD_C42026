
import { useAdminUsers } from '../hooks/useAdminUsers';
import {
  LoadingState,
  ErrorState,
} from '@/shared/components/StatusStates';

export function AdminUsersPage() {
  const { query, mutation } = useAdminUsers();

  if (query.isLoading) {
    return <LoadingState message="Cargando usuarios..." />;
  }

  if (query.isError) {
    return (
      <ErrorState
        message={query.error.message}
        onRetry={() => void query.refetch()}
      />
    );
  }

  return (
    <section className="mx-auto max-w-6xl p-6 sm:py-8">
      <h1 className="text-2xl font-bold">
        Administración de usuarios
      </h1>

      <p className="my-3 text-sm text-slate-600">
        Consultá las cuentas y activá o desactivá su acceso.
      </p>

      {mutation.isError && (
        <p role="alert" className="my-3 text-red-700">
          {mutation.error.message}
        </p>
      )}

      <div className="overflow-x-auto rounded-xl border bg-white">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50">
            <tr>
              {[
                'Nombre',
                'Email',
                'Roles vigentes',
                'Estado',
                'Acciones',
              ].map((title) => (
                <th key={title} className="p-4">
                  {title}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {query.data?.map((user) => (
              <tr key={user.id} className="border-t">
                <td className="p-4">
                  {user.nombre} {user.apellido}
                </td>

                <td className="p-4">{user.email}</td>

                <td className="p-4">
                  {user.roles.join(', ')}
                </td>

                <td className="p-4">
                  {user.deleted_at ? 'Inactivo' : 'Activo'}
                </td>

                <td className="p-4">
                  <button
                    disabled={mutation.isPending}
                    onClick={() =>
                      mutation.mutate({
                        id: user.id,
                        active: Boolean(user.deleted_at),
                      })
                    }
                    className="rounded-lg border px-3 py-2 text-indigo-700 disabled:opacity-50"
                  >
                    {user.deleted_at ? 'Activar' : 'Desactivar'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

