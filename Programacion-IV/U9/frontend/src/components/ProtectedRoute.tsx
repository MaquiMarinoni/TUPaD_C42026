import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { LoadingState } from './StatusStates';

export function ProtectedRoute({ allowedRoles }: { allowedRoles?: string[] }) {
  const { user, loading } = useAuthStore();
  if (loading) return <LoadingState message="Verificando sesión..." />;
  if (!user) return <Navigate to="/login" replace />;
  if (allowedRoles) {
    const tienePermiso = allowedRoles.some((role) => user.roles.includes(role));
    if (!tienePermiso) {
      return <Navigate to="/unauthorized" replace />;
    }
  }
  return <Outlet />;
}
