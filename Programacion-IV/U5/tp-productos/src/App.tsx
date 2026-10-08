import { Navbar } from './components/Navbar';
import { ProductoForm } from './components/ProductoForm';
import { ProductoList } from './components/ProductoList';
import type { Producto } from './types/producto';

const PRODUCTOS_INICIALES: Producto[] = [
  {
    id: 1,
    nombre: 'Silla de Oficina Ergonómica',
    categoria: 'MUE-01',
    precio: 150.50,
    stock: 20,
    stock_minimo: 5,
    activo: true,
  },
  {
    id: 2,
    nombre: 'Escritorio Gamer Regulable',
    categoria: 'MUE-02',
    precio: 320.00,
    stock: 2,
    stock_minimo: 5,
    activo: true,
  },
  {
    id: 3,
    nombre: 'Monitor IPS 27" QHD',
    categoria: 'TEC-01',
    precio: 285.99,
    stock: 12,
    stock_minimo: 4,
    activo: false,
  },
];

export function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
      <Navbar />

      <main className="flex-1 max-w-5xl w-full mx-auto px-4 py-8">
        <ProductoForm />
        <ProductoList productos={PRODUCTOS_INICIALES} />
      </main>

      <footer className="border-t border-gray-200 bg-white py-4 text-center text-xs text-gray-400">
        Trabajo práctico UN 5 • Programación IV • UTN
      </footer>
    </div>
  );
}

export default App;