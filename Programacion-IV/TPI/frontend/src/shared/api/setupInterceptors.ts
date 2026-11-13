
import axios from 'axios';
import { axiosInstance } from './api';
import { useAuthStore } from '@/features/auth';
import { useNotificationStore } from '@/store/notificationStore';
import type { ApiErrorResponse } from '@/features/auth';

axiosInstance.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (axios.isAxiosError<ApiErrorResponse>(error)) {
      const status = error.response?.status;
      const detail = error.response?.data?.detail;
      const path = error.config?.url?.split('?')[0];

      if (typeof detail === 'string') {
        error.message = detail;
      } else if (Array.isArray(detail)) {
        error.message = detail.map((item) => item.msg).join(', ');
      } else {
        error.message = 'No se pudo conectar con el servidor.';
      }

      if (
        status === 401 &&
        path !== '/auth/token' &&
        path !== '/auth/me'
      ) {
        useAuthStore.getState().clearSession();
      }

      if (status === 400 && detail === 'Cuenta de usuario desactivada') {
        useAuthStore.getState().clearSession();
      }

      if (status === 403) {
        useNotificationStore
          .getState()
          .showNotification('Acceso denegado', 'error');
      }
    }

    return Promise.reject(error);
  }
);
