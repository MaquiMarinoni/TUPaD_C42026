// src/App.tsx
import { useState, useEffect } from "react";
import type { Categoria, CategoriaFormData } from "./types/categoria";
import { Navbar } from "./components/Navbar";
import { CategoriaList } from "./components/CategoriaList";
import { CategoriaModal } from "./components/CategoriaModal";

// URL base de la API FastAPI
const API_URL = "http://localhost:8000/categorias";

export const App = () => {
  // 1. Estados principales
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [categoriaToEdit, setCategoriaToEdit] = useState<Categoria | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // 2. Cargar categorías al montar el componente (GET /categorias)
  const fetchCategorias = async () => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const response = await fetch(API_URL);
      if (!response.ok) {
        throw new Error(`Error en el servidor: ${response.status}`);
      }
      const data: Categoria[] = await response.json();
      setCategorias(data);
    } catch (error) {
      console.warn("Backend no disponible aún o error de conexión:", error);
      setErrorMessage("No se pudo conectar con el servidor backend (FastAPI en :8000).");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCategorias();
  }, []);

  // 3. Abrir modal para crear
  const handleOpenCreateModal = () => {
    setCategoriaToEdit(null);
    setIsModalOpen(true);
  };

  // 4. Abrir modal para editar
  const handleOpenEditModal = (categoria: Categoria) => {
    setCategoriaToEdit(categoria);
    setIsModalOpen(true);
  };

  // 5. Cerrar modal
  const handleCloseModal = () => {
    setIsModalOpen(false);
    setCategoriaToEdit(null);
  };

  // 6. Operaciones CRUD hacia el backend
  const handleCreate = async (data: CategoriaFormData) => {
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("No se pudo crear la categoría.");
      }

      const nuevaCategoria: Categoria = await response.json();
      setCategorias((prev) => [...prev, nuevaCategoria]);
      handleCloseModal();
    } catch (error) {
      alert("Error al crear categoría. Asegurate de que el backend esté ejecutándose.");
      console.error(error);
    }
  };

  const handleUpdate = async (id: number, data: CategoriaFormData) => {
    try {
      const response = await fetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("No se pudo actualizar la categoría.");
      }

      const categoriaActualizada: Categoria = await response.json();
      setCategorias((prev) =>
        prev.map((cat) => (cat.id === id ? categoriaActualizada : cat))
      );
      handleCloseModal();
    } catch (error) {
      alert("Error al actualizar categoría.");
      console.error(error);
    }
  };

  const handleDelete = async (id: number) => {
    const confirmacion = window.confirm("¿Seguro que deseás eliminar esta categoría?");
    if (!confirmacion) return;

    try {
      const response = await fetch(`${API_URL}/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("No se pudo eliminar la categoría.");
      }

      setCategorias((prev) => prev.filter((cat) => cat.id !== id));
    } catch (error) {
      alert("Error al eliminar la categoría del backend.");
      console.error(error);
    }
  };

  // 7. Enrutador del submit del modal
  const handleSaveModal = (data: CategoriaFormData) => {
    if (categoriaToEdit) {
      handleUpdate(categoriaToEdit.id, data);
    } else {
      handleCreate(data);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Encabezado y botón de acción */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
          <div>
            <h2 className="text-2xl font-extrabold text-gray-900 tracking-tight">
              Categorías
            </h2>
            <p className="text-sm text-gray-500 mt-1">
              Administrá los rubros del catálogo de Food Store.
            </p>
          </div>

          <button
            type="button"
            onClick={handleOpenCreateModal}
            className="inline-flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-lg shadow-sm transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            <span className="mr-1.5 text-lg font-bold leading-none">+</span> Añadir Categoría
          </button>
        </div>

        {/* Notificación si el backend aún no está iniciado */}
        {errorMessage && (
          <div className="mb-6 p-4 rounded-lg bg-amber-50 border border-amber-200 text-amber-800 text-sm flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span>⚠️</span>
              <span>
                <strong>Aviso:</strong> {errorMessage} Pasaremos al backend en el próximo paso para conectar todo.
              </span>
            </div>
            <button
              onClick={fetchCategorias}
              className="text-xs bg-amber-200 hover:bg-amber-300 text-amber-900 font-semibold px-2 py-1 rounded"
            >
              Reintentar
            </button>
          </div>
        )}

        {/* Estado de carga o Lista de categorías */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-indigo-600 border-t-transparent"></div>
            <p className="mt-2 text-sm text-gray-500">Cargando categorías...</p>
          </div>
        ) : (
          <CategoriaList
            categorias={categorias}
            onEdit={handleOpenEditModal}
            onDelete={handleDelete}
          />
        )}
      </main>

      {/* Modal de alta/edición */}
      <CategoriaModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSubmit={handleSaveModal}
        categoriaToEdit={categoriaToEdit}
      />
    </div>
  );
};

export default App;