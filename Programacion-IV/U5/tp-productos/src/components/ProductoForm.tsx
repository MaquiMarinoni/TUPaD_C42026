    export const ProductoForm = () => {
    return (
        <section className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
        <div className="flex items-center space-x-2 mb-6">
            <span className="text-lg" role="img" aria-label="formulario">
            </span>
            <h2 className="text-base font-bold text-gray-800">
            Nuevo Producto
            </h2>
        </div>

        <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="md:col-span-2">
                <label
                htmlFor="nombre"
                className="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1"
                >
                Nombre del Producto
                </label>
                <input
                id="nombre"
                name="nombre"
                type="text"
                placeholder="Ej. Silla de Oficina Ergonómica"
                className="w-full px-3.5 py-2 rounded-lg border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                />
            </div>

            <div>
                <label
                htmlFor="categoria"
                className="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1"
                >
                Categoría (AAA-00)
                </label>
                <input
                id="categoria"
                name="categoria"
                type="text"
                placeholder="Ej. MUE-01"
                className="w-full px-3.5 py-2 rounded-lg border border-gray-300 text-sm font-mono uppercase focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                />
            </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
                <label
                htmlFor="precio"
                className="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1"
                >
                Precio ($)
                </label>
                <input
                id="precio"
                name="precio"
                type="number"
                step="0.01"
                min="0.01"
                placeholder="150.50"
                className="w-full px-3.5 py-2 rounded-lg border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                />
            </div>

            <div>
                <label
                htmlFor="stock"
                className="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1"
                >
                Stock Actual
                </label>
                <input
                id="stock"
                name="stock"
                type="number"
                min="0"
                placeholder="20"
                className="w-full px-3.5 py-2 rounded-lg border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                />
            </div>

            <div>
                <label
                htmlFor="stock_minimo"
                className="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1"
                >
                Stock Mínimo
                </label>
                <input
                id="stock_minimo"
                name="stock_minimo"
                type="number"
                min="0"
                placeholder="5"
                className="w-full px-3.5 py-2 rounded-lg border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                />
            </div>
            </div>

            <div className="pt-2 flex justify-end">
            <button
                type="submit"
                className="px-5 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold shadow-sm transition-colors cursor-pointer"
            >
                Agregar Producto
            </button>
            </div>
        </form>
        </section>
    );
    };