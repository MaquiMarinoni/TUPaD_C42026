
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { axiosInstance } from '@/shared/api/api';
import { useNotificationStore } from '@/store/notificationStore';
import type { UsuarioAuth } from '../types/auth.types';

interface CambioEstadoUsuario {
  id: number;
  active: boolean;
}

export function useAdminUsers() {
  const queryClient = useQueryClient();
  const showNotification = useNotificationStore(
    (state) => state.showNotification
  );

  const query = useQuery<UsuarioAuth[], Error>({
    queryKey: ['usuarios'],
    queryFn: async () => {
      const response = await axiosInstance.get<UsuarioAuth[]>(
        '/auth/admin/usuarios'
      );
      return response.data;
    },
  });

  const mutation = useMutation({
    mutationFn: async ({ id, active }: CambioEstadoUsuario) => {
      const accion = active ? 'activar' : 'desactivar';

      await axiosInstance.post(
        `/auth/admin/usuarios/${id}/${accion}`
      );
    },

    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ['usuarios'],
      });

      showNotification(
        'Estado del usuario actualizado',
        'success'
      );
    },

    onError: (error: Error) => {
      showNotification(error.message, 'error');
    },
  });

  return {
    query,
    mutation,
  };
}
