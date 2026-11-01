import axios from 'axios';
import { useAuthStore } from '../store/authStore';
import type { ApiErrorResponse, PaginatedResponse } from '../types/auth.types';

export const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  withCredentials: true,
});
// El navegador envía la cookie HttpOnly. Este interceptor no lee ni agrega tokens.
axiosInstance.interceptors.request.use((config) => config);
axiosInstance.interceptors.response.use((response) => response, (error: unknown) => {
  if (axios.isAxiosError<ApiErrorResponse>(error)) {
    const detail = error.response?.data.detail;
    error.message = typeof detail === 'string' ? detail : Array.isArray(detail)
      ? detail.map((item) => item.msg).join(', ') : 'No se pudo conectar con el servidor.';
    const path = error.config?.url?.split('?')[0];
    if ((error.response?.status === 401 && path !== '/auth/token' && path !== '/auth/me') ||
        (error.response?.status === 400 && detail === 'Cuenta de usuario desactivada')) {
      useAuthStore.getState().clearSession();
    }
  }
  return Promise.reject(error);
});

// Los listados de U8 usan paginación local; se recuperan todas las páginas de la API.
export async function listAll<T>(path: string): Promise<T[]> {
  const items: T[] = [];
  let total = 0;
  do {
    const { data } = await axiosInstance.get<PaginatedResponse<T>>(path, { params: { offset: items.length, limit: 100 } });
    items.push(...data.items);
    total = data.total;
    if (!data.items.length) break;
  } while (items.length < total);
  return items;
}
