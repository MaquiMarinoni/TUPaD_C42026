import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import type { Categoria, CategoriaFormData } from "../types/categoria";
import { CategoriaList } from "../components/CategoriaList";
import { CategoriaModal } from "../components/CategoriaModal";

const API_URL = "http://localhost:8000/categorias";

const fetchCategorias = async (): Promise<Categoria[]> => {
  const res = await fetch(`${API_URL}/?offset=0&limit=100`);
  if (!res.ok) {
    const errData = await res.json().catch(() => ({ detail: "Error al obtener las categorías" }));
    throw new Error(JSON.stringify({ detail: errData.detail || "Error al obtener las categorías" }));
  }
  const data = await res.json();
  return Array.isArray(data) ? data : data.items;
};

export const CategoriasPage = () => {
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [categoriaToEdit, setCategoriaToEdit] = useState<Categoria | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);

  const {
    data: categorias = [],
    isLoading,
    isError,
    error,
  } = useQuery<Categoria[], Error>({
    queryKey: ["categorias"],
    queryFn: fetchCategorias,
  });

  const createMutation = useMutation({
    mutationFn: async (formData: CategoriaFormData) => {
      const res = await fetch(`${API_URL}/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Error al crear la categoría" }));
        throw new Error(err.detail || "Error al crear la categoría");
      }
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["categorias"] });
      setActionError(null);
      handleCloseModal();
    },
    onError: (err: Error) => {
      setActionError(err.message);
    },
  });

  const updateMutation = useMutation({
    mutationFn: async ({ id, data }: { id: number; data: CategoriaFormData }) => {
      const res = await fetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Error al actualizar la categoría" }));
        throw new Error(err.detail || "Error al actualizar la categoría");
      }
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["categorias"] });
      setActionError(null);
      handleCloseModal();
    },
    onError: (err: Error) => {
      setActionError(err.message);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      const res = await fetch(`${API_URL}/${id}`, {
        method: "DELETE",
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Error al eliminar la categoría" }));
        throw new Error(err.detail || "Error al eliminar la categoría");
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["categorias"] });
      setActionError(null);
    },
    onError: (err: Error) => {
      setActionError(err.message);
    },
  });

  const handleOpenCreate = () => {
    setActionError(null);
    setCategoriaToEdit(null);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (categoria: Categoria) => {
    setActionError(null);
    setCategoriaToEdit(categoria);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setCategoriaToEdit(null);
  };

  const handleSubmitModal = (formData: CategoriaFormData) => {
    if (categoriaToEdit) {
      updateMutation.mutate({ id: categoriaToEdit.id, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  const handleDelete = (id: number) => {
    if (window.confirm("¿Estás segura de que deseás eliminar esta categoría?")) {
      deleteMutation.mutate(id);
    }
  };

  return (
    <main className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Gestión de Categorías</h2>
          <p className="text-sm text-gray-500 mt-1">
            Administrá las categorías disponibles en el catálogo ({categorias.length} registradas)
          </p>
        </div>

        <button
          type="button"
          onClick={handleOpenCreate}
          className="inline-flex items-center justify-center px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-lg shadow-sm transition-colors"
        >
          + Nueva categoría
        </button>
      </div>

      {actionError && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center justify-between text-red-700 text-sm">
          <span>{`{"detail": "${actionError}"}`}</span>
          <button
            type="button"
            onClick={() => setActionError(null)}
            className="text-red-500 hover:text-red-700 font-bold ml-4"
          >
            &times;
          </button>
        </div>
      )}

      {isLoading ? (
        <div className="text-center py-16 bg-white rounded-xl border border-gray-100 shadow-sm">
          <p className="text-gray-500 text-sm font-medium">Cargando categorías...</p>
        </div>
      ) : isError ? (
        <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
          <p className="font-semibold mb-1">Error al conectar con el servidor:</p>
          <code>{error?.message}</code>
        </div>
      ) : (
        <CategoriaList
          categorias={categorias}
          onEdit={handleOpenEdit}
          onDelete={handleDelete}
        />
      )}

      <CategoriaModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSubmit={handleSubmitModal}
        categoriaToEdit={categoriaToEdit}
      />
    </main>
  );
};

export default CategoriasPage;