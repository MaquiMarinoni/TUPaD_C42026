    // src/components/CategoriaCard.tsx
    // src/components/CategoriaCard.tsx
import type { Categoria } from "../types/categoria";

    interface CategoriaCardProps {
    categoria: Categoria;
    onEdit: (categoria: Categoria) => void;
    onDelete: (id: number) => void;
    }

    export const CategoriaCard = ({ categoria, onEdit, onDelete }: CategoriaCardProps) => {
    return (
        <tr className="border-b border-gray-200 hover:bg-gray-50 transition-colors">
        <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
            {categoria.id}
        </td>
        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800">
            {categoria.nombre}
        </td>
        <td className="px-6 py-4 text-sm text-gray-600 max-w-md break-words">
            {categoria.descripcion}
        </td>
        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2 text-right">
            <button
            type="button"
            onClick={() => onEdit(categoria)}
            className="inline-flex items-center px-3 py-1.5 border border-amber-500 text-amber-600 hover:bg-amber-50 rounded-md text-xs font-semibold uppercase tracking-wider transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-500 focus:ring-offset-1"
            >
            Editar
            </button>
            <button
            type="button"
            onClick={() => onDelete(categoria.id)}
            className="inline-flex items-center px-3 py-1.5 border border-red-500 text-red-600 hover:bg-red-50 rounded-md text-xs font-semibold uppercase tracking-wider transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-1"
            >
            Eliminar
            </button>
        </td>
        </tr>
    );
    };