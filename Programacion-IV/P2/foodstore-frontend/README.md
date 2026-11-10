# Food Store — Frontend

**Programación IV — Parcial 2**

**Estudiante:** Marinoni Macarena

## 1. Descripción

Este proyecto implementa la interfaz web de administración de productos de Food Store.

Fue desarrollado utilizando React, TypeScript, Vite y Tailwind CSS 4.

La aplicación consume la API REST del backend mediante `fetch` nativo y permite administrar el catálogo de productos.

## 2. Requisitos previos

Para ejecutar el proyecto se necesita:

- Node.js y npm.
- Backend de Food Store instalado y funcionando.
- PostgreSQL configurado según las instrucciones del README del backend.

## 3. Instalación

Abrir una terminal dentro de la carpeta `foodstore-frontend`.

Instalar las dependencias:

```bash
npm install
```

## 4. Ejecución

Primero iniciar el backend siguiendo las instrucciones de su README.

El backend debe estar disponible en:

`http://127.0.0.1:8000`

Luego, desde la carpeta del frontend, ejecutar:

```bash
npm run dev
```

Abrir la aplicación en:

`http://localhost:5173`

## 5. Funcionalidades

Desde la interfaz se pueden realizar las siguientes operaciones:

- Visualizar los productos activos del catálogo.
- Crear productos mediante un formulario modal.
- Editar nombre, descripción, precio, unidad de venta, stock y disponibilidad.
- Pausar o habilitar la venta de un producto.
- Anular productos mediante baja lógica.
- Consultar el precio y stock con el símbolo de su unidad de medida.
- Identificar productos con y sin stock.
- Visualizar mensajes de error, estados de carga y listados vacíos.

El selector de unidades de medida obtiene sus opciones desde la API.

## 6. Estructura del proyecto

```text
foodstore-frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── ProductoCard.tsx
│   │   ├── ProductoList.tsx
│   │   └── ProductoModal.tsx
│   ├── types/
│   │   ├── categoria.ts
│   │   ├── producto.ts
│   │   └── unidadMedida.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── index.html
├── package.json
├── package-lock.json
├── vite.config.ts
├── tsconfig.json
├── tsconfig.app.json
└── README.md
```

## 7. Implementación técnica

La aplicación utiliza componentes funcionales con propiedades tipadas mediante interfaces TypeScript.

El estado del catálogo se administra desde `App.tsx` utilizando `useState`.

La carga inicial de productos y unidades se realiza mediante `useEffect`.

Los componentes reciben los datos y las funciones de operación mediante props.

Las peticiones HTTP se realizan utilizando `fetch` nativo, sin Axios ni bibliotecas externas de manejo de estado.

Los estilos están implementados mediante clases utilitarias de Tailwind CSS 4.

## 8. Compilación

Para verificar que el frontend compile correctamente:

```bash
npm run build
```

La aplicación utiliza TypeScript con la opción `strict` habilitada.

## 9. Consideraciones

El frontend administra exclusivamente los productos.

La gestión de categorías y las relaciones entre productos y categorías se demuestran mediante los archivos `.http` incluidos en el backend, de acuerdo con la consigna.

El frontend requiere que la API se encuentre ejecutándose para obtener y modificar la información del catálogo.