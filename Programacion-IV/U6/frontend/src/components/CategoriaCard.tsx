
    import type { Categoria } from "../types/categoria";

    interface CategoriaCardProps {
    categoria: Categoria;
    onEdit: (categoria: Categoria) => void;
    onDelete: (id: number) => void;
    }

    export const CategoriaCard = ({ categoria, onEdit, onDelete }: CategoriaCardProps) => {
    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 flex flex-col justify-between hover:shadow-md transition-shadow">
        <div>
            <div className="flex justify-between items-center mb-3">
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-indigo-50 text-indigo-700 border border-indigo-100">
                N° {categoria.id}
            </span>
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-1.5">{categoria.nombre}</h3>
            <p className="text-sm text-gray-600 line-clamp-3 leading-relaxed">
            {categoria.descripcion || "Sin descripción proporcionada."}
            </p>
        </div>

        <div className="mt-5 pt-4 border-t border-gray-100 flex justify-end space-x-2">
            <button
            type="button"
            onClick={() => onEdit(categoria)}
            className="inline-flex items-center px-3 py-1.5 border border-amber-500 text-amber-600 hover:bg-amber-50 rounded-lg text-xs font-semibold uppercase tracking-wider transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
            >
            Editar
            </button>
            <button
            type="button"
            onClick={() => onDelete(categoria.id)}
            className="inline-flex items-center px-3 py-1.5 border border-red-500 text-red-600 hover:bg-red-50 rounded-lg text-xs font-semibold uppercase tracking-wider transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500"
            >
            Eliminar
            </button>
        </div>
        </div>
    );
    };