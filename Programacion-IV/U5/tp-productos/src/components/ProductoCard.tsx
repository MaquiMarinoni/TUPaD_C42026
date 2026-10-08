    import type { Producto } from '../types/producto';

    type ProductoCardProps = {
    producto: Producto;
    };

    export const ProductoCard = ({ producto }: ProductoCardProps) => {
    const bajoStock = producto.stock < producto.stock_minimo;

    return (
        <tr className="border-b border-gray-100 hover:bg-gray-50/80 transition-colors">
        <td className="py-3.5 px-4 text-xs font-semibold text-gray-400">
            #{producto.id}
        </td>
        <td className="py-3.5 px-4 text-sm font-medium text-gray-900">
            {producto.nombre}
        </td>
        <td className="py-3.5 px-4">
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-mono font-semibold bg-indigo-50 text-indigo-700 border border-indigo-100">
            {producto.categoria}
            </span>
        </td>
        <td className="py-3.5 px-4 text-sm font-semibold text-gray-800">
            ${producto.precio.toFixed(2)}
        </td>
        <td className="py-3.5 px-4 text-sm">
            <div className="flex items-center space-x-2">
            <span className="font-medium text-gray-800">{producto.stock} u.</span>
            <span className="text-xs text-gray-400">
                (mín: {producto.stock_minimo})
            </span>
            {bajoStock && (
                <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-red-50 text-red-700 border border-red-200">
                Bajo stock
                </span>
            )}
            </div>
        </td>
        <td className="py-3.5 px-4 text-sm">
            {producto.activo ? (
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                Activo
            </span>
            ) : (
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-gray-100 text-gray-500 border border-gray-200">
                Inactivo
            </span>
            )}
        </td>
        </tr>
    );
    };