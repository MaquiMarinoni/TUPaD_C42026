# FoodStore frontend — Unidad 9

React + TypeScript + Vite + Tailwind. Se conservan los formularios y tablas de U8. Las peticiones pasan por Axios con credenciales; Zustand persiste solo los datos del usuario. Al abrir la aplicación se confirma la sesión en el servidor.

```powershell
pnpm install --frozen-lockfile
pnpm dev --port 5173 --strictPort
pnpm build
pnpm lint
```

URL: http://localhost:5173. La guía completa, incluida la preparación del backend, está en [README de U9](../README.md).

| Ruta | Acceso |
|---|---|
| `/login`, `/register`, `/unauthorized` | Público |
| `/categories`, `/products`, `/ingredientes` | Sesión activa |
| `/admin/users` | Admin |

Las acciones de escritura solo se muestran al administrador. El backend valida los mismos permisos. Al salir o recibir un 401, se limpia también la caché de TanStack Query para evitar reutilizar datos de otra sesión.
