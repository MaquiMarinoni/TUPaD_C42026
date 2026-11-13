
import axios from 'axios';
import type { PaginatedResponse } from '@/features/auth';

export const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  withCredentials: true,
});

export async function listAll<T>(path: string): Promise<T[]> {
  const items: T[] = [];
  let total = 0;

  do {
    const response = await axiosInstance.get<PaginatedResponse<T>>(path, {
      params: {
        offset: items.length,
        limit: 100,
      },
    });

    const pagina = response.data;

    items.push(...pagina.items);
    total = pagina.total;

    if (pagina.items.length === 0) break;

  } while (items.length < total);

  return items;
}
