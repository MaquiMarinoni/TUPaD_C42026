import { useCartStore } from '@/features/cart/store/cartStore';
import { useEffect, useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '@/features/auth';
import { useThemeStore } from '@/store/themeStore';

export function Navbar() {
  const { user, logout } = useAuth();

  const cartCount = useCartStore((state) =>
    state.items.reduce((sum, item) => sum + item.cantidad, 0)
  );

  const { darkMode, toggleTheme } = useThemeStore();

  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
  }, [darkMode]);

  async function closeSession() {
    setBusy(true);
    setError('');

    try {
      await logout();
      navigate('/products', { replace: true });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'No se pudo cerrar la sesion.'
      );
    } finally {
      setBusy(false);
    }
  }

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `rounded-lg px-3 py-2 text-sm font-medium ${
      isActive
        ? 'bg-indigo-50 text-indigo-700'
        : 'text-slate-600 hover:bg-slate-100'
    }`;

  return (
    <header className="border-b border-slate-200 bg-white">
      <nav
        aria-label="Navegacion principal"
        className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-6 py-4"
      >
        <Link
          to="/products"
          className="text-lg font-bold text-slate-900"
        >
          FoodStore
        </Link>

        <div className="flex flex-wrap items-center gap-1">
          <NavLink to="/products" className={linkClass}>
            Productos
          </NavLink>

          <NavLink to="/categories" className={linkClass}>
            Categorias
          </NavLink>

          <NavLink to="/carrito" className={linkClass}>
            Carrito ({cartCount})
          </NavLink>

          {user && (
            <NavLink to="/pedidos" className={linkClass}>
              Pedidos
            </NavLink>
          )}

          {user?.role === 'admin' && (
            <>
              <NavLink to="/admin/resumen" className={linkClass}>
                Resumen
              </NavLink>

              <NavLink to="/admin/users" className={linkClass}>
                Usuarios
              </NavLink>
            </>
          )}
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={toggleTheme}
            className="rounded-lg border border-slate-300 px-3 py-2 text-sm"
            aria-label="Cambiar tema"
          >
            {darkMode ? 'Modo claro' : 'Modo oscuro'}
          </button>

          {user ? (
            <>
              <div className="px-2 text-sm">
                <p className="font-semibold text-slate-900">
                  {user.full_name}
                </p>

                <p className="text-xs text-slate-500">
                  {user.role || 'Sin roles vigentes'}
                </p>
              </div>

              <button
                type="button"
                onClick={() => void closeSession()}
                disabled={busy}
                className="rounded-lg border border-slate-300 px-3 py-2 text-sm disabled:opacity-50"
              >
                {busy ? 'Cerrando...' : 'Cerrar sesion'}
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login" className={linkClass}>
                Ingresar
              </NavLink>

              <NavLink to="/register" className={linkClass}>
                Registrarse
              </NavLink>
            </>
          )}
        </div>
      </nav>

      {error && (
        <p role="alert" className="px-6 pb-3 text-sm text-red-700">
          {error}
        </p>
      )}
    </header>
  );
}
