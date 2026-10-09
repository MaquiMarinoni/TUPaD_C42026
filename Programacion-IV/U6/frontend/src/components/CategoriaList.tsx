
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
      <div className="text-center py-16 bg-white rounded-xl border-2 border-dashed border-gray-200 p-8 shadow-sm">
        <h3 className="mt-3 text-base font-semibold text-gray-900">No hay categorías registradas</h3>
        <p className="mt-1 text-sm text-gray-500">
          Comenzá agregando una categoría nueva con el botón superior.
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {categorias.map((categoria) => (
        <CategoriaCard
          key={categoria.id}
          categoria={categoria}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
};