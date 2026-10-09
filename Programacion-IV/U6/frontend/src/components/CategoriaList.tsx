    // src/components/CategoriaList.tsx
    import type { Categoria } from "../types/categoria";
    import { CategoriaCard } from "./CategoriaCard";

    interface CategoriaListProps {
    categorias: Categoria[];
    onEdit: (categoria: Categoria) => void;
    onDelete: (id: number) => void;
    }

    export const CategoriaList = ({ categorias, onEdit, onDelete }: CategoriaListProps) => {
    if (categorias.length === 0) {
        return (
        <div className="text-center py-12 bg-white rounded-lg border border-dashed border-gray-300 shadow-sm">
            <span className="text-4xl">📂</span>
            <h3 className="mt-2 text-sm font-semibold text-gray-900">No hay categorías registradas</h3>
            <p className="mt-1 text-sm text-gray-500">
            Comenzá agregando una categoría nueva con el botón superior.
            </p>
        </div>
        );
    }

    return (
        <div className="overflow-x-auto bg-white rounded-lg shadow border border-gray-200">
        <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-100">
            <tr>
                <th scope="col" className="px-6 py-3.5 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">
                NÚMERO
                </th>
                <th scope="col" className="px-6 py-3.5 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">
                NOMBRE
                </th>
                <th scope="col" className="px-6 py-3.5 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">
                DESCRIPCIÓN
                </th>
                <th scope="col" className="px-6 py-3.5 text-right text-xs font-bold text-gray-600 uppercase tracking-wider">
                ACCIONES
                </th>
            </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
            {categorias.map((categoria) => (
                <CategoriaCard
                key={categoria.id}
                categoria={categoria}
                onEdit={onEdit}
                onDelete={onDelete}
                />
            ))}
            </tbody>
        </table>
        </div>
    );
    };