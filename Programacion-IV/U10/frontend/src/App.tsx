
import { useEffect } from 'react';
import { useAuthStore } from '@/features/auth';
import { Navbar } from '@/shared/components/Navbar';
import { Toast } from '@/shared/components/Toast';
import { AppRouter } from '@/routes/AppRouter';

export default function App() {
  useEffect(() => {
    void useAuthStore.getState().checkSession();
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
      <Navbar />

      <main className="flex-1">
        <AppRouter />
      </main>

      <Toast />
    </div>
  );
}
