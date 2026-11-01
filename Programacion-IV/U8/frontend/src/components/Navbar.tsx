import React from 'react';
import { NavLink } from 'react-router-dom';
import { Layers, Package, UtensilsCrossed, Store } from 'lucide-react';

export const Navbar: React.FC = () => {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `inline-flex items-center gap-2 rounded-lg px-3.5 py-2 text-sm font-medium transition-colors ${
      isActive
        ? 'bg-indigo-600 text-white shadow-xs'
        : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
    }`;

  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/95 backdrop-blur-xs">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3.5 sm:px-6">
        <NavLink to="/categorias" className="flex items-center gap-2.5 text-slate-900 font-bold text-lg">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-600 text-white shadow-xs">
            <Store className="h-5 w-5" />
          </div>
          <span>FoodStore Admin</span>
        </NavLink>

        <nav className="flex items-center gap-1.5">
          <NavLink to="/categorias" className={linkClass}>
            <Layers className="h-4 w-4" />
            <span>Categorías</span>
          </NavLink>
          <NavLink to="/productos" className={linkClass}>
            <Package className="h-4 w-4" />
            <span>Productos</span>
          </NavLink>
          <NavLink to="/ingredientes" className={linkClass}>
            <UtensilsCrossed className="h-4 w-4" />
            <span>Ingredientes</span>
          </NavLink>
        </nav>
      </div>
    </header>
  );
};

export default Navbar;
