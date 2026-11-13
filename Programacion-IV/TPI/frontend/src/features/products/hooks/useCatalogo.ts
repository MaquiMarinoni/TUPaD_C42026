import { useQuery } from '@tanstack/react-query';
import { axiosInstance } from '@/shared/api/api';
import type { Producto } from '../types/producto';

export interface FiltrosCatalogo {
  skip: number;
  limit: number;
  search?: string;
  categoria_id?: number;
  disponible?: boolean;
}

export interface CatalogoPaginado {
  total: number;
  items: Producto[];
}

export function useCatalogo(filtros: FiltrosCatalogo) {
  return useQuery<CatalogoPaginado, Error>({
    queryKey: [
      'productos',
      'catalogo',
      filtros.skip,
      filtros.limit,
      filtros.search ?? '',
      filtros.categoria_id ?? null,
      filtros.disponible ?? null,
    ],
    queryFn: async () => {
      const { data } = await axiosInstance.get<CatalogoPaginado>(
        '/productos',
        {
          params: {
            skip: filtros.skip,
            limit: filtros.limit,
            search: filtros.search?.trim() || undefined,
            categoria_id: filtros.categoria_id,
            disponible: filtros.disponible,
          },
        }
      );

      return data;
    },
  });
}
