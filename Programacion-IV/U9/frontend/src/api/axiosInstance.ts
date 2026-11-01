import axios from 'axios';
import { useAuthStore } from '../store/authStore';
import type { ApiErrorResponse, PaginatedResponse } from '../types/auth.types';

export const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  withCredentials: true,
});

// La cookie la envía el navegador. No se lee el token desde JavaScript.
axiosInstance.interceptors.request.use((config) => config);

axiosInstance.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (axios.isAxiosError<ApiErrorResponse>(error)) {
      const detail = error.response?.data.detail;

      // FastAPI devuelve un texto o una lista de errores de validación.
      if (typeof detail === 'string') {
        error.message = detail;
      } else if (Array.isArray(detail)) {
        error.message = detail.map((item) => item.msg).join(', ');
      } else {
        error.message = 'No se pudo conectar con el servidor.';
      }

      const status = error.response?.status;
      const path = error.config?.url?.split('?')[0];
      const esLogin = path === '/auth/token';
      const esConsultaSesion = path === '/auth/me';
      const sesionVencida = status === 401 && !esLogin && !esConsultaSesion;
      const cuentaDesactivada = status === 400 && detail === 'Cuenta de usuario desactivada';

      if (sesionVencida || cuentaDesactivada) {
        useAuthStore.getState().clearSession();
      }
    }

    return Promise.reject(error);
  },
);

// Las tablas paginan en el frontend; por eso se consultan todas las páginas de la API.
export async function listAll<T>(path: string): Promise<T[]> {
  const items: T[] = [];
  let total = 0;

  do {
    const response = await axiosInstance.get<PaginatedResponse<T>>(path, {
      params: { offset: items.length, limit: 100 },
    });
    const pagina = response.data;

    items.push(...pagina.items);
    total = pagina.total;

    if (pagina.items.length === 0) {
      break;
    }
  } while (items.length < total);

  return items;
}
