import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { axiosInstance } from '../api/axiosInstance';
import { queryClient } from '../api/queryClient';
import type { UsuarioAuth, MensajeResponse } from '../types/auth.types';

interface AuthState {
  user: UsuarioAuth | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  checkSession: () => Promise<void>;
  clearSession: () => void;
}
let sessionVersion = 0;
let checking: Promise<void> | null = null;

export const useAuthStore = create<AuthState>()(persist((set) => ({
  user: null,
  loading: true,
  clearSession: () => {
    sessionVersion++;
    void queryClient.cancelQueries();
    queryClient.clear();
    set({ user: null, loading: false });
  },
  login: async (email, password) => {
    const version = ++sessionVersion;
    set({ loading: true });
    try {
      const form = new URLSearchParams({ username: email, password });
      await axiosInstance.post<MensajeResponse>('/auth/token', form);
      const { data } = await axiosInstance.get<UsuarioAuth>('/auth/me');
      if (version === sessionVersion) {
        queryClient.clear();
        set({ user: data });
      }
    } catch (error) {
      if (version === sessionVersion) set({ user: null });
      throw error;
    } finally {
      if (version === sessionVersion) set({ loading: false });
    }
  },
  logout: async () => {
    await axiosInstance.post<MensajeResponse>('/auth/logout');
    useAuthStore.getState().clearSession();
  },
  checkSession: () => {
    if (checking) return checking;
    const version = sessionVersion;
    set({ loading: true });
    checking = (async () => {
      try {
        const { data } = await axiosInstance.get<UsuarioAuth>('/auth/me');
        if (version === sessionVersion) set({ user: data });
      } catch {
        if (version === sessionVersion) useAuthStore.getState().clearSession();
      } finally {
        if (version === sessionVersion) set({ loading: false });
        checking = null;
      }
    })();
    return checking;
  },
}), { name: 'foodstore-u9-auth', partialize: (state) => ({ user: state.user }) }));
