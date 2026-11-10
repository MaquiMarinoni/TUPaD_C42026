import { useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

export function Navbar() {
  const { user, logout } = useAuthStore();
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const navigate = useNavigate();
  async function closeSession() {
    setBusy(true);
    setError('');
    try {
      await logout();
      navigate('/login', { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No se pudo cerrar la sesión.');
    } finally {
      setBusy(false);
    }
  }
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `rounded-lg px-3 py-2 text-sm font-medium ${isActive ? 'bg-indigo-50 text-indigo-700' : 'text-slate-600 hover:bg-slate-100'}`;
  return (
    <header className="border-b border-slate-200 bg-white">
      <nav
        aria-label="Navegación principal"
        className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-6 py-4"
      >
        <Link to={user ? '/categories' : '/login'} className="text-lg font-bold text-slate-900">
          FoodStore
        </Link>
        {user ? (
          <>
            <div className="flex flex-wrap gap-1">
              <NavLink to="/categories" className={linkClass}>
                Categorías
              </NavLink>
              <NavLink to="/products" className={linkClass}>
                Productos
              </NavLink>
              <NavLink to="/ingredientes" className={linkClass}>
                Ingredientes
              </NavLink>
              {user.roles.includes('admin') && (
                <NavLink to="/admin/users" className={linkClass}>
                  Usuarios
                </NavLink>
              )}
            </div>
            <div className="flex flex-wrap items-center gap-3 text-sm">
              <div>
                <p className="font-semibold">
                  {user.nombre} {user.apellido}
                </p>
                <p className="text-xs text-slate-500">
                  {user.roles.join(', ') || 'Sin roles vigentes'}
                </p>
              </div>
              <button
                onClick={() => void closeSession()}
                disabled={busy}
                className="rounded-lg border px-3 py-2 disabled:opacity-50"
              >
                {busy ? 'Cerrando...' : 'Cerrar sesión'}
              </button>
            </div>
          </>
        ) : (
          <div className="flex gap-2">
            <NavLink to="/login" className={linkClass}>
              Ingresar
            </NavLink>
            <NavLink to="/register" className={linkClass}>
              Registrarse
            </NavLink>
          </div>
        )}
      </nav>
      {error && (
        <p role="alert" className="px-6 pb-3 text-sm text-red-700">
          {error}
        </p>
      )}
    </header>
  );
}
