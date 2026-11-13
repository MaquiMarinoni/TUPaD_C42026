import { create } from 'zustand';
import { axiosInstance } from '@/shared/api/api';
import { queryClient } from '@/shared/api/queryClient';
import type { UsuarioAuth } from '../types/auth.types';

interface AuthState {
  user: UsuarioAuth | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  checkSession: () => Promise<void>;
  clearSession: () => void;
}

let sessionVersion = 0;
let checking: Promise<void> | null = null;

export const useAuthStore = create<AuthState>()((set) => ({
  user: null,
  loading: true,

  clearSession: () => {
    sessionVersion++;
    void queryClient.cancelQueries();
    queryClient.clear();
    set({ user: null, loading: false });
  },

  login: async (username, password) => {
    const version = ++sessionVersion;
    set({ loading: true });

    try {
      const form = new URLSearchParams({
        username,
        password,
      });

      await axiosInstance.post('/auth/token', form, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      const { data } = await axiosInstance.get<UsuarioAuth>('/auth/me');

      if (version === sessionVersion) {
        queryClient.clear();
        set({ user: data });
      }
    } catch (error) {
      if (version === sessionVersion) {
        set({ user: null });
      }
      throw error;
    } finally {
      if (version === sessionVersion) {
        set({ loading: false });
      }
    }
  },

  logout: async () => {
    try {
      await axiosInstance.post('/auth/logout');
    } finally {
      useAuthStore.getState().clearSession();
    }
  },

  checkSession: () => {
    if (checking) return checking;

    const version = sessionVersion;
    set({ loading: true });

    checking = (async () => {
      try {
        const { data } = await axiosInstance.get<UsuarioAuth>('/auth/me');

        if (version === sessionVersion) {
          set({ user: data });
        }
      } catch {
        if (version === sessionVersion) {
          useAuthStore.getState().clearSession();
        }
      } finally {
        if (version === sessionVersion) {
          set({ loading: false });
        }
        checking = null;
      }
    })();

    return checking;
  },
}));