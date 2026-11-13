
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { axiosInstance } from '@/shared/api/api';
import { useNotificationStore } from '@/store/notificationStore';
import type { Producto, ProductoFormData } from '../types/producto';

interface Opciones {
  enabled?: boolean;
  onSaved?: () => void;
  onSaveError?: (error: Error) => void;
  onDeleted?: () => void;
  onDeleteError?: (error: Error) => void;
}

interface ProductosPaginados {
  total: number;
  items: Producto[];
}

export function useProducts(options: Opciones = {}) {
  const queryClient = useQueryClient();
  const showNotification = useNotificationStore(
    (state) => state.showNotification
  );

  const queryKey = ['productos'];

  const query = useQuery<Producto[], Error>({
    queryKey,
    enabled: options.enabled ?? true,
    queryFn: async () => {
      const limit = 100;
      let skip = 0;
      const productos: Producto[] = [];

      while (true) {
        const response = await axiosInstance.get<ProductosPaginados>(
          '/productos',
          { params: { limit, skip } }
        );

        const pagina = response.data;
        productos.push(...pagina.items);

        if (pagina.items.length === 0 || productos.length >= pagina.total) {
          break;
        }

        skip += pagina.items.length;
      }

      return productos;
    },
  });

  const createMutation = useMutation({
    mutationFn: async (payload: ProductoFormData) => {
      const response = await axiosInstance.post<Producto>(
        '/productos',
        payload
      );
      return response.data;
    },

    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey });
      showNotification('Producto creado correctamente', 'success');
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
      showNotification('Producto actualizado correctamente', 'success');
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
      showNotification('Producto eliminado correctamente', 'success');
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
