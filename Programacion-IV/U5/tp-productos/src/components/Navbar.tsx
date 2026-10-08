export const Navbar = () => {
  return (
    <header className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <span className="text-2xl" role="img" aria-label="caja de productos">
          </span>
          <div>
            <h1 className="text-xl font-bold text-gray-800 tracking-tight">
              TP Productos
            </h1>
            <p className="text-xs text-gray-500">
              Gestor de catálogo • Persistencia SQLModel & UI React
            </p>
          </div>
        </div>

      </div>
    </header>
  );
};