
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { axiosInstance } from '@/shared/api/api';
import { useNotificationStore } from '@/store/notificationStore';
import type { Categoria, CategoriaFormData } from '../types/categoria';

interface Opciones {
  onSaved?: () => void;
  onSaveError?: (error: Error) => void;
  onDeleted?: () => void;
  onDeleteError?: (error: Error) => void;
}

type RespuestaCategorias =
  | Categoria[]
  | { total: number; items: Categoria[] };

export function useCategories(options: Opciones = {}) {
  const queryClient = useQueryClient();
  const showNotification = useNotificationStore(
    (state) => state.showNotification
  );

  const queryKey = ['categorias'];

  const query = useQuery<Categoria[], Error>({
    queryKey,
    queryFn: async () => {
      const response = await axiosInstance.get<RespuestaCategorias>(
        '/categorias'
      );

      return Array.isArray(response.data)
        ? response.data
        : response.data.items;
    },
  });

  const createMutation = useMutation({
    mutationFn: async (payload: CategoriaFormData) => {
      const response = await axiosInstance.post<Categoria>(
        '/categorias',
        payload
      );
      return response.data;
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey });
      showNotification('Categoría creada correctamente', 'success');
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
      payload: CategoriaFormData;
    }) => {
      const response = await axiosInstance.put<Categoria>(
        `/categorias/${id}`,
        payload
      );
      return response.data;
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey });
      showNotification('Categoría actualizada correctamente', 'success');
      options.onSaved?.();
    },
    onError: (error: Error) => {
      showNotification(error.message, 'error');
      options.onSaveError?.(error);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await axiosInstance.delete(`/categorias/${id}`);
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey });
      showNotification('Categoría eliminada correctamente', 'success');
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
