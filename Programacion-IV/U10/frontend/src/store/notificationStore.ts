
import { create } from 'zustand';

type NotificationType = 'success' | 'error' | 'info';

interface NotificationState {
  message: string;
  visible: boolean;
  type: NotificationType;
  id: number;
  showNotification: (message: string, type?: NotificationType) => void;
  hideNotification: () => void;
}

export const useNotificationStore = create<NotificationState>()((set) => ({
  message: '',
  visible: false,
  type: 'info',
  id: 0,

  showNotification: (message, type = 'success') =>
    set((state) => ({
      message,
      type,
      visible: true,
      id: state.id + 1,
    })),

  hideNotification: () => set({ visible: false }),
}));
