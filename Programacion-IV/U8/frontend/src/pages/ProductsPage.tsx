import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import type { Producto, ProductoFormData } from "../types/producto";
import type { Categoria } from "../types/categoria";

const PRODUCTOS_URL = "http://localhost:8000/productos";
const CATEGORIAS_URL = "http://localhost:8000/categorias";

const fetchProductos = async (): Promise<Producto[]> => {
  const res = await fetch(`${PRODUCTOS_URL}/?offset=0&limit=100`);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Error al obtener productos" }));
    throw new Error(err.detail || "Error al obtener productos");
  }
  const data = await res.json();
  return Array.isArray(data) ? data : data.items;
};

const fetchCategorias = async (): Promise<Categoria[]> => {
  const res = await fetch(`${CATEGORIAS_URL}/?offset=0&limit=100`);
  if (!res.ok) {
    throw new Error("Error al obtener categorías");
  }
  const data = await res.json();
  return Array.isArray(data) ? data : data.items;
};

export const ProductsPage = () => {
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [productoToEdit, setProductoToEdit] = useState<Producto | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);

  // Estados del formulario modal de Producto
  const [nombre, setNombre] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [precioBase, setPrecioBase] = useState("0");
  const [imagenUrl, setImagenUrl] = useState("");
  const [disponible, setDisponible] = useState(true);
  const [selectedCatIds, setSelectedCatIds] = useState<number[]>([]);

  const {
    data: productos = [],
    isLoading,
    isError,
    error,
  } = useQuery<Producto[], Error>({
    queryKey: ["productos"],
    queryFn: fetchProductos,
  });

  const { data: categorias = [] } = useQuery<Categoria[], Error>({
    queryKey: ["categorias"],
    queryFn: fetchCategorias,
  });

  useEffect(() => {
    if (productoToEdit) {
      setNombre(productoToEdit.nombre);
      setDescripcion(productoToEdit.descripcion);
      setPrecioBase(String(productoToEdit.precio_base));
      setImagenUrl(productoToEdit.imagenes_url?.[0] || "");
      setDisponible(productoToEdit.disponible);
      setSelectedCatIds(productoToEdit.categoria_ids || []);
    } else {
      setNombre("");
      setDescripcion("");
      setPrecioBase("0");
      setImagenUrl("");
      setDisponible(true);
      setSelectedCatIds(categorias[0] ? [categorias[0].id] : []);
    }
  }, [productoToEdit, isModalOpen, categorias]);

  const createMutation = useMutation({
    mutationFn: async (data: ProductoFormData) => {
      const res = await fetch(`${PRODUCTOS_URL}/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Error al crear el producto" }));
        throw new Error(
          typeof err.detail === "string" ? err.detail : "Verificá los datos del producto (al menos 1 categoría)"
        );
      }
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["productos"] });
      setActionError(null);
      setIsModalOpen(false);
    },
    onError: (err: Error) => setActionError(err.message),
  });

  const updateMutation = useMutation({
    mutationFn: async ({ id, data }: { id: number; data: ProductoFormData }) => {
      const res = await fetch(`${PRODUCTOS_URL}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Error al actualizar el producto" }));
        throw new Error(typeof err.detail === "string" ? err.detail : "Error al actualizar el producto");
      }
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["productos"] });
      setActionError(null);
      setIsModalOpen(false);
    },
    onError: (err: Error) => setActionError(err.message),
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      const res = await fetch(`${PRODUCTOS_URL}/${id}`, { method: "DELETE" });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Error al eliminar el producto" }));
        throw new Error(err.detail || "Error al eliminar el producto");
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["productos"] });
      setActionError(null);
    },
    onError: (err: Error) => setActionError(err.message),
  });

  const toggleCategoria = (catId: number) => {
    setSelectedCatIds((prev) =>
      prev.includes(catId) ? prev.filter((id) => id !== catId) : [...prev, catId]
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!nombre.trim()) return;
    if (selectedCatIds.length === 0) {
      setActionError("Debés seleccionar al menos una categoría para el producto (RN-19)");
      return;
    }

    const payload: ProductoFormData = {
      nombre: nombre.trim(),
      descripcion: descripcion.trim(),
      precio_base: Number(precioBase) || 0,
      imagenes_url: imagenUrl.trim() ? [imagenUrl.trim()] : [],
      disponible,
      categoria_ids: selectedCatIds,
    };

    if (productoToEdit) {
      updateMutation.mutate({ id: productoToEdit.id, data: payload });
    } else {
      createMutation.mutate(payload);
    }
  };

  const getCategoriaNombres = (ids?: number[]) => {
    if (!ids || ids.length === 0) return [];
    return categorias.filter((c) => ids.includes(c.id));
  };

  return (
    <main className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Catálogo de Productos</h2>
          <p className="text-sm text-gray-500 mt-1">
            Gestioná los productos y sus categorías asociadas ({productos.length} registrados)
          </p>
        </div>

        <button
          type="button"
          onClick={() => {
            setActionError(null);
            setProductoToEdit(null);
            setIsModalOpen(true);
          }}
          className="inline-flex items-center justify-center px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-lg shadow-sm transition-colors"
        >
          + Nuevo producto
        </button>
      </div>

      {actionError && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center justify-between text-red-700 text-sm">
          <span>{actionError}</span>
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
          <p className="text-gray-500 text-sm font-medium">Cargando productos...</p>
        </div>
      ) : isError ? (
        <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
          <p className="font-semibold mb-1">Error al cargar productos:</p>
          <code>{error?.message}</code>
        </div>
      ) : productos.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-xl border-2 border-dashed border-gray-200 p-8 shadow-sm">
          <h3 className="mt-3 text-base font-semibold text-gray-900">No hay productos registrados</h3>
          <p className="mt-1 text-sm text-gray-500">
            Comenzá agregando un producto nuevo con el botón superior.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {productos.map((prod) => {
            const catsAsociadas = getCategoriaNombres(prod.categoria_ids);
            return (
              <div
                key={prod.id}
                className="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow overflow-hidden flex flex-col justify-between"
              >
                <div>
                  {prod.imagenes_url?.[0] && (
                    <img
                      src={prod.imagenes_url[0]}
                      alt={prod.nombre}
                      className="w-full h-44 object-cover border-b border-gray-100"
                    />
                  )}
                  <div className="p-5">
                    <div className="flex items-start justify-between gap-2">
                      <h3 className="text-lg font-bold text-gray-900">{prod.nombre}</h3>
                      <span
                        className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                          prod.disponible
                            ? "bg-green-100 text-green-800"
                            : "bg-gray-100 text-gray-600"
                        }`}
                      >
                        {prod.disponible ? "Disponible" : "Sin stock"}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mt-2">
                      {prod.descripcion || "Sin descripción"}
                    </p>
                    <p className="text-xl font-extrabold text-indigo-600 mt-3">
                      ${prod.precio_base.toLocaleString("es-AR")}
                    </p>
                    {catsAsociadas.length > 0 && (
                      <div className="flex flex-wrap gap-1.5 mt-3">
                        {catsAsociadas.map((c) => (
                          <span
                            key={c.id}
                            className="px-2 py-0.5 bg-indigo-50 text-indigo-700 rounded text-xs font-medium"
                          >
                            {c.nombre}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                <div className="px-5 py-3 bg-gray-50 border-t border-gray-100 flex justify-end gap-2">
                  <button
                    type="button"
                    onClick={() => {
                      setActionError(null);
                      setProductoToEdit(prod);
                      setIsModalOpen(true);
                    }}
                    className="px-3 py-1.5 text-xs font-semibold text-indigo-600 hover:bg-indigo-50 rounded-md transition-colors"
                  >
                    Editar
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      if (window.confirm(`¿Eliminar el producto "${prod.nombre}"?`)) {
                        deleteMutation.mutate(prod.id);
                      }
                    }}
                    className="px-3 py-1.5 text-xs font-semibold text-red-600 hover:bg-red-50 rounded-md transition-colors"
                  >
                    Eliminar
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
          <div className="bg-white rounded-xl shadow-2xl max-w-md w-full overflow-hidden border border-gray-100">
            <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
              <h2 className="text-lg font-bold text-gray-800">
                {productoToEdit ? "Editar Producto" : "Nuevo Producto"}
              </h2>
              <button
                type="button"
                onClick={() => setIsModalOpen(false)}
                className="text-gray-400 hover:text-gray-600 text-2xl leading-none"
              >
                &times;
              </button>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">
                  Nombre del producto
                </label>
                <input
                  type="text"
                  required
                  value={nombre}
                  onChange={(e) => setNombre(e.target.value)}
                  placeholder="Ej: Hamburguesa Doble Cheddar"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">
                  Descripción
                </label>
                <textarea
                  rows={2}
                  value={descripcion}
                  onChange={(e) => setDescripcion(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-1">
                    Precio base ($)
                  </label>
                  <input
                    type="number"
                    min="0"
                    step="0.01"
                    required
                    value={precioBase}
                    onChange={(e) => setPrecioBase(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div className="flex items-end pb-2">
                  <label className="inline-flex items-center gap-2 text-sm font-medium text-gray-700 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={disponible}
                      onChange={(e) => setDisponible(e.target.checked)}
                      className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                    />
                    Disponible
                  </label>
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">
                  URL de imagen (opcional)
                </label>
                <input
                  type="url"
                  value={imagenUrl}
                  onChange={(e) => setImagenUrl(e.target.value)}
                  placeholder="https://..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">
                  Categorías asociadas (mínimo 1)
                </label>
                <div className="flex flex-wrap gap-2 max-h-28 overflow-y-auto p-2 border border-gray-200 rounded-md">
                  {categorias.map((cat) => {
                    const active = selectedCatIds.includes(cat.id);
                    return (
                      <button
                        key={cat.id}
                        type="button"
                        onClick={() => toggleCategoria(cat.id)}
                        className={`px-2.5 py-1 rounded-full text-xs font-medium transition-colors ${
                          active
                            ? "bg-indigo-600 text-white"
                            : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                        }`}
                      >
                        {cat.nombre}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="pt-4 flex justify-end space-x-3 border-t border-gray-100">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-md shadow-sm"
                >
                  Guardar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </main>
  );
};

export default ProductsPage;