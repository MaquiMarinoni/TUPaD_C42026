
    import { useState, useEffect } from "react";
    import type { Categoria, CategoriaFormData } from "../types/categoria";

    interface CategoriaModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSubmit: (data: CategoriaFormData) => void;
    categoriaToEdit: Categoria | null;
    }

    export const CategoriaModal = ({
    isOpen,
    onClose,
    onSubmit,
    categoriaToEdit,
    }: CategoriaModalProps) => {
    const [nombre, setNombre] = useState("");
    const [descripcion, setDescripcion] = useState("");

    // Sincronizar el formulario cuando cambia categoriaToEdit o cuando se abre el modal
    useEffect(() => {
        if (categoriaToEdit) {
        setNombre(categoriaToEdit.nombre);
        setDescripcion(categoriaToEdit.descripcion);
        } else {
        setNombre("");
        setDescripcion("");
        }
    }, [categoriaToEdit, isOpen]);

    if (!isOpen) return null;

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!nombre.trim()) return;

        onSubmit({
        nombre: nombre.trim(),
        descripcion: descripcion.trim(),
        });
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm transition-opacity">
        <div className="bg-white rounded-xl shadow-2xl max-w-md w-full overflow-hidden border border-gray-100">
            <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
            <h2 className="text-lg font-bold text-gray-800">
                {categoriaToEdit ? "Editar Categoría" : "Añadir Categoría"}
            </h2>
            <button
                type="button"
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600 transition-colors text-2xl leading-none"
            >
                &times;
            </button>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-4">
            <div>
                <label htmlFor="nombre" className="block text-sm font-semibold text-gray-700 mb-1">
                Nombre de la categoría
                </label>
                <input
                id="nombre"
                type="text"
                required
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                placeholder="Ej: Pizzas, Bebidas"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm text-gray-800"
                />
            </div>

            <div>
                <label htmlFor="descripcion" className="block text-sm font-semibold text-gray-700 mb-1">
                Descripción
                </label>
                <textarea
                id="descripcion"
                rows={3}
                value={descripcion}
                onChange={(e) => setDescripcion(e.target.value)}
                placeholder="Breve descripción de la categoría"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm text-gray-800"
                />
            </div>

            <div className="pt-4 flex justify-end space-x-3 border-t border-gray-100">
                <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
                >
                Cancelar
                </button>
                <button
                type="submit"
                className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-md shadow-sm transition-colors"
                >
                Guardar
                </button>
            </div>
            </form>
        </div>
        </div>
    );
    };