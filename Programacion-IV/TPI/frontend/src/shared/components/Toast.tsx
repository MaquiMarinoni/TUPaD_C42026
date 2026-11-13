
import { useEffect } from 'react';
import { useNotificationStore } from '@/store/notificationStore';

export function Toast() {
  const { message, visible, type, id, hideNotification } =
    useNotificationStore();

  useEffect(() => {
    if (!visible) return;

    const timeout = setTimeout(() => {
      hideNotification();
    }, 3000);

    return () => clearTimeout(timeout);
  }, [visible, id, hideNotification]);

  if (!visible) return null;

  const styles = {
    success: 'bg-green-600',
    error: 'bg-red-600',
    info: 'bg-blue-600',
  };

  return (
    <div
      role={type === 'error' ? 'alert' : 'status'}
      className={`fixed bottom-5 right-5 z-50 rounded-lg px-5 py-3 text-white shadow-lg ${styles[type]}`}
    >
      {message}
    </div>
  );
}
