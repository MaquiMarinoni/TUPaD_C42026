
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { axiosInstance, listAll } from '@/shared/api/api';
import { useNotificationStore } from '@/store/notificationStore';
import type { Producto, ProductoFormData } from '../types/producto';

interface Opciones {
  onSaved?: () => void;
  onSaveError?: (error: Error) => void;
  onDeleted?: () => void;
  onDeleteError?: (error: Error) => void;
}

export function useProducts(options: Opciones = {}) {
  const queryClient = useQueryClient();
  const showNotification = useNotificationStore(
    (state) => state.showNotification
  );

  const queryKey = ['productos'];

  const query = useQuery<Producto[], Error>({
    queryKey,
    queryFn: () => listAll<Producto>('/productos/'),
  });

  const createMutation = useMutation({
    mutationFn: async (payload: ProductoFormData) => {
      const response = await axiosInstance.post<Producto>(
        '/productos/',
        payload
      );
      return response.data;
    },

    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey });

      showNotification(
        'Producto creado correctamente',
        'success'
      );

      options.onSaved?.();
    },

    onError: (error: Error) => {
      showNotification(error.message, 'error');
      options.onSaveError?.(error);
    },
  });

  const updateMutation = useMutation({
    mutationFn: async ({
      id,
      payload,
    }: {
      id: number;
      payload: ProductoFormData;
    }) => {
      const response = await axiosInstance.put<Producto>(
        `/productos/${id}`,
        payload
      );
      return response.data;
    },

    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey });

      showNotification(
        'Producto actualizado correctamente',
        'success'
      );

      options.onSaved?.();
    },

    onError: (error: Error) => {
      showNotification(error.message, 'error');
      options.onSaveError?.(error);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await axiosInstance.delete(`/productos/${id}`);
    },

    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey });

      showNotification(
        'Producto eliminado correctamente',
        'success'
      );

      options.onDeleted?.();
    },

    onError: (error: Error) => {
      showNotification(error.message, 'error');
      options.onDeleteError?.(error);
    },
  });

  return {
    ...query,
    createMutation,
    updateMutation,
    deleteMutation,
  };
}
