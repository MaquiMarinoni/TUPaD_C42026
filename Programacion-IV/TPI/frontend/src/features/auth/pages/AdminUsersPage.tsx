
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
        Consultá las cuentas y administrá su acceso al sistema.
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
                'Usuario',
                'Nombre completo',
                'Email',
                'Rol',
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
                <td className="p-4">{user.username}</td>

                <td className="p-4">{user.full_name}</td>

                <td className="p-4">{user.email}</td>

                <td className="p-4">{user.role}</td>

                <td className="p-4">
                  {user.disabled ? 'Inactivo' : 'Activo'}
                </td>

                <td className="p-4">
                  <button
                    type="button"
                    disabled={mutation.isPending}
                    onClick={() =>
                      mutation.mutate({
                        id: user.id,
                        disabled: !user.disabled,
                      })
                    }
                    className="rounded-lg border px-3 py-2 text-indigo-700 disabled:opacity-50"
                  >
                    {user.disabled ? 'Activar' : 'Desactivar'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {query.data?.length === 0 && (
          <p className="p-6 text-center text-sm text-slate-500">
            No hay usuarios registrados.
          </p>
        )}
      </div>
    </section>
  );
}
