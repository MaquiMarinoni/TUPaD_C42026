# Food Store — Frontend (React + TypeScript)

Aplicación web desarrollada como Trabajo Práctico de la Unidad 6.

La aplicación implementa el **CRUD completo de Categorías** para el catálogo de Food Store, consumiendo una API REST desarrollada en FastAPI mediante `fetch` nativo del navegador, con diseño responsivo basado en tarjetas (*cards*) estilizadas con Tailwind CSS.

---

## Tecnologías utilizadas

- **React 18 / 19**
- **TypeScript**
- **Vite**
- **Tailwind CSS v3**
- **Fetch Nativo**

---

## Arquitectura de Componentes

- **`App.tsx`**: Componente contenedor que centraliza el estado global con `useState` (lista de categorías, estado del modal, categoría en edición y estados de carga/error) y los efectos secundarios con `useEffect` para la carga inicial (`GET /categorias`).
- **`src/types/categoria.ts`**: Definición de la `interface Categoria` y el tipo derivado `CategoriaFormData`.
- **`src/components/Navbar.tsx`**: Barra de navegación superior con identidad visual de la aplicación.
- **`src/components/CategoriaList.tsx`**: Componente puro que renderiza el grid responsivo de categorías o un estado vacío amigable.
- **`src/components/CategoriaCard.tsx`**: Tarjeta individual para cada categoría con sus datos, identificador y botones de acción (Editar y Eliminar).
- **`src/components/CategoriaModal.tsx`**: Formulario modal controlado para alta y modificación de categorías.
- **`src/components/Footer.tsx`**: Pie de página institucional modularizado.

---

## Instrucciones de Instalación y Ejecución

### Prerrequisitos
- **Node.js** (versión 18 o superior).
- Gestor de paquetes **pnpm** (o npm / yarn).
- Tener el backend de FastAPI en ejecución en `http://localhost:8000`.

### Pasos para iniciar:

Posicionarse en el directorio del frontend y ejecutar en terminal:

```bash
   pnpm install
   pnpm dev 
```

   Abrir el navegador web en http://localhost:5173