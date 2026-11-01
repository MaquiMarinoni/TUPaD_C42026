import { Link, useLocation } from "react-router-dom";

interface NavbarProps {
  totalCategorias?: number;
}

export const Navbar = ({ totalCategorias }: NavbarProps) => {
  const location = useLocation();
  const isCategorias =
    location.pathname.startsWith("/categorias") || location.pathname === "/";
  const isProductos = location.pathname.startsWith("/productos");

  return (
    <header className="bg-indigo-600 text-white shadow-md">
      <div className="max-w-6xl mx-auto px-4 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex items-center gap-3">
          <span className="text-2xl font-extrabold bg-white text-indigo-600 w-10 h-10 rounded-lg flex items-center justify-center shadow-sm">
            FS
          </span>
          <div>
            <h1 className="text-xl font-bold tracking-tight">FoodStore Admin</h1>
            <p className="text-indigo-100 text-xs">Panel de Gestión de Catálogo</p>
          </div>
        </div>

        <nav className="flex items-center gap-2">
          <Link
            to="/categorias"
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              isCategorias
                ? "bg-white text-indigo-700 shadow-sm"
                : "text-indigo-100 hover:bg-indigo-500"
            }`}
          >
            Categorías
            {typeof totalCategorias === "number" && (
              <span className="ml-2 bg-indigo-100 text-indigo-800 px-2 py-0.5 rounded-full text-xs font-bold">
                {totalCategorias}
              </span>
            )}
          </Link>

          <Link
            to="/productos"
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              isProductos
                ? "bg-white text-indigo-700 shadow-sm"
                : "text-indigo-100 hover:bg-indigo-500"
            }`}
          >
            Productos
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Navbar;