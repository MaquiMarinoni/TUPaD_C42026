import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { axiosInstance } from '@/shared/api/api';
import type { EstadoPedido, Pedido, PedidoCrear, PedidosPaginados } from '../types/pedido';
export function useOrders() {
  const client = useQueryClient();
  const query = useQuery<Pedido[]>({
    queryKey: ['pedidos'],
    queryFn: async () => {
      const result: Pedido[] = [];
      let skip = 0;
      while (true) {
        const { data } = await axiosInstance.get<PedidosPaginados>('/pedidos', { params: { skip, limit: 100 } });
        result.push(...data.items);
        if (!data.items.length || result.length >= data.total) break;
        skip += data.items.length;
      }
      return result;
    },
  });
  const invalidate = () => client.invalidateQueries({ queryKey: ['pedidos'] });
  const create = useMutation({ mutationFn: async (payload: PedidoCrear) => (await axiosInstance.post<Pedido>('/pedidos', payload)).data, onSuccess: invalidate });
  const changeStatus = useMutation({ mutationFn: async ({ id, estado }: { id: number; estado: EstadoPedido }) => (await axiosInstance.patch<Pedido>(`/pedidos/${id}/estado`, { estado })).data, onSuccess: invalidate });
  const cancel = useMutation({ mutationFn: async (id: number) => (await axiosInstance.patch<Pedido>(`/pedidos/${id}/cancelar`)).data, onSuccess: invalidate });
  return { ...query, create, changeStatus, cancel };
}
