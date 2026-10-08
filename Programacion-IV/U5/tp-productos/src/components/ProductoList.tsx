    import type { Producto } from '../types/producto';
    import { ProductoCard } from './ProductoCard';

    type ProductoListProps = {
    productos: Producto[];
    };

    export const ProductoList = ({ productos }: ProductoListProps) => {
    return (
        <section className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
            <div className="flex items-center space-x-2">
            <span className="text-lg" role="img" aria-label="listado">
                📋
            </span>
            <h2 className="text-base font-bold text-gray-800">
                Productos ({productos.length})
            </h2>
            </div>
        </div>

        <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
            <thead>
                <tr className="bg-gray-50/70 border-b border-gray-100 text-[11px] font-bold uppercase tracking-wider text-gray-400">
                <th className="py-3 px-4">ID</th>
                <th className="py-3 px-4">Nombre</th>
                <th className="py-3 px-4">Categoría</th>
                <th className="py-3 px-4">Precio</th>
                <th className="py-3 px-4">Stock</th>
                <th className="py-3 px-4">Estado</th>
                </tr>
            </thead>
            <tbody>
                {productos.map((prod) => (
                <ProductoCard key={prod.id} producto={prod} />
                ))}
            </tbody>
            </table>
        </div>
        </section>
    );
    };