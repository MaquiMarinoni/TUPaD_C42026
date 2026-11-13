# Frontend - Food Store

Interfaz React/TypeScript del Trabajo Pr?ctico Integrador de Programaci?n IV.

**Alumna:** Macarena Marinoni

## Tecnolog?as

React, TypeScript, Vite, Tailwind CSS 4, React Router, TanStack Query/Form/Table, Zustand, Axios y pnpm.

## Instalaci?n y ejecuci?n (desde `Frontend`)

Primero iniciar el backend en `http://localhost:8000`.

```powershell
pnpm install --frozen-lockfile
pnpm dev
```

Abrir `http://localhost:5173`.

## Compilaci?n

```powershell
pnpm build
```

## Rutas principales

| Ruta | Acceso | Funci?n |
| --- | --- | --- |
| `/categories` | P?blico | Categor?as |
| `/products` | P?blico | Cat?logo de productos |
| `/carrito` | P?blico | Carrito |
| `/login` | P?blico | Inicio de sesi?n |
| `/register` | P?blico | Registro |
| `/checkout` | Autenticado | Confirmaci?n de pedido |
| `/pedidos` | Autenticado | Historial de pedidos |
| `/admin/resumen` | Administrador | Resumen administrativo |
| `/admin/users` | Administrador | Gesti?n de usuarios |

`/categorias` y `/productos` redirigen a las rutas equivalentes en ingl?s.

## Funcionalidades

- Cat?logo p?blico, b?squeda, filtros y paginaci?n.
- Carrito persistente, actualizaci?n de cantidades y checkout protegido.
- Autenticaci?n y control de acceso seg?n rol.
- Historial y gesti?n de pedidos.
- Administraci?n de usuarios, productos, categor?as y stock desde la interfaz.
- Panel administrativo, notificaciones y modo claro/oscuro.

## Verificaciones realizadas

Se comprobaron manualmente cat?logo, carrito, autenticaci?n, checkout, pedidos, funciones administrativas y visualizaci?n en modo oscuro. La compilaci?n `pnpm build` finaliz? correctamente.

Consultar `../Backend/README.md` para preparar PostgreSQL y ejecutar la API.
