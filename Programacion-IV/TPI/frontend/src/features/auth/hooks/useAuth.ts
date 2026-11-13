import { useAuthStore } from '../store/authStore';
import { axiosInstance } from '@/shared/api/api';
import { useNotificationStore } from '@/store/notificationStore';
import type { RegisterData, UsuarioAuth } from '../types/auth.types';

export function useAuth() {
  const user = useAuthStore((state) => state.user);
  const loading = useAuthStore((state) => state.loading);
  const login = useAuthStore((state) => state.login);
  const logout = useAuthStore((state) => state.logout);
  const checkSession = useAuthStore((state) => state.checkSession);

  const register = async (data: RegisterData) => {
    try {
      await axiosInstance.post<UsuarioAuth>('/auth/register', data);

      useNotificationStore.getState().showNotification(
        'Cuenta creada correctamente',
        'success'
      );
    } catch (error) {
      useNotificationStore.getState().showNotification(
        error instanceof Error ? error.message : 'Error al registrar',
        'error'
      );
      throw error;
    }
  };

  return {
    user,
    loading,
    login,
    logout,
    register,
    checkSession,
    isAdmin: user?.role === 'admin',
  };
}