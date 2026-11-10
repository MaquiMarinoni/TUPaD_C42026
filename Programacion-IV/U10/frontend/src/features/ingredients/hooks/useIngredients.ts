
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { axiosInstance, listAll } from '@/shared/api/api';
import { useNotificationStore } from '@/store/notificationStore';
import type { Ingrediente, IngredienteFormData } from '../types/ingrediente';

interface Opciones {
  onSaved?: () => void;
  onSaveError?: (error: Error) => void;
  onDeleted?: () => void;
  onDeleteError?: (error: Error) => void;
}

export function useIngredients(options: Opciones = {}) {
  const queryClient = useQueryClient();
  const showNotification = useNotificationStore(
    (state) => state.showNotification
  );

  const queryKey = ['ingredientes'];

  const query = useQuery<Ingrediente[], Error>({
    queryKey,
    queryFn: () => listAll<Ingrediente>('/ingredientes/'),
  });

  const createMutation = useMutation({
    mutationFn: async (payload: IngredienteFormData) => {
      const response = await axiosInstance.post<Ingrediente>(
        '/ingredientes/',
        payload
      );
      return response.data;
    },

    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey });

      showNotification(
        'Ingrediente creado correctamente',
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
      payload: IngredienteFormData;
    }) => {
      const response = await axiosInstance.put<Ingrediente>(
        `/ingredientes/${id}`,
        payload
      );
      return response.data;
    },

    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey });

      showNotification(
        'Ingrediente actualizado correctamente',
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
      await axiosInstance.delete(`/ingredientes/${id}`);
    },

    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey });

      showNotification(
        'Ingrediente eliminado correctamente',
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
