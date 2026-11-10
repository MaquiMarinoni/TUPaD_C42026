
# Trabajo Práctico – Unidad 10
## Programación IV – FoodStore

**Alumna:** Macarena Marinoni  
**Carrera:** Tecnicatura Universitaria en Programación a Distancia – UTN

## 1. Descripción

Este trabajo continúa el frontend desarrollado en la Unidad 9.

Se reorganizó el código utilizando una arquitectura por features, agrupando los archivos de cada dominio en carpetas independientes.

También se implementaron rutas protegidas según la sesión y el rol del usuario, custom hooks para las operaciones de datos y stores globales de interfaz con Zustand.

Se conserva el funcionamiento del CRUD de categorías, productos e ingredientes y la autenticación mediante el backend de la Unidad 9.

## 2. Tecnologías utilizadas

- React y TypeScript
- Vite
- React Router
- Zustand
- TanStack Query
- Axios
- Tailwind CSS
- pnpm

## 3. Estructura del proyecto

```text
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── store/
│   │   ├── types/
│   │   ├── pages/
│   │   └── index.ts
│   ├── categories/
│   ├── products/
│   └── ingredients/
├── shared/
│   ├── components/
│   └── api/
├── store/
│   ├── themeStore.ts
│   └── notificationStore.ts
├── routes/
│   ├── AppRouter.tsx
│   └── ProtectedRoute.tsx
├── App.tsx
└── main.tsx
```

Las features de categorías, productos e ingredientes contienen sus propias carpetas de componentes, hooks, tipos y páginas, además de un archivo `index.ts`.

Las importaciones entre features se realizan mediante sus barrel exports. Los elementos compartidos se ubican en `shared/`, mientras que las rutas se organizan en `routes/`.

El alias `@/` apunta a la carpeta `src/`.

## 4. Funcionalidades

### Autenticación y autorización

La aplicación permite registrar usuarios, iniciar sesión y cerrar sesión.

La sesión se verifica mediante `GET /api/v1/auth/me`. El store de autenticación no utiliza persistencia local.

Las rutas protegidas utilizan `ProtectedRoute` y `Outlet`:

- `/login`: acceso público.
- `/register`: acceso público.
- `/unauthorized`: acceso público.
- `/categories`: requiere sesión.
- `/products`: requiere sesión.
- `/ingredientes`: requiere sesión.
- `/admin/users`: requiere rol admin.

El interceptor de Axios gestiona las respuestas 401 y 403.

### Custom hooks

- `useAuth`: autenticación.
- `useCategories`: CRUD de categorías.
- `useProducts`: CRUD de productos.
- `useIngredients`: CRUD de ingredientes.
- `useAdminUsers`: administración de usuarios.

Los hooks encapsulan la interacción con la API. Las consultas y mutaciones utilizan TanStack Query.

### Estado global de interfaz

Se implementaron dos stores con Zustand:

- `themeStore`: permite alternar entre modo claro y oscuro. La preferencia se guarda mediante `persist`.
- `notificationStore`: administra las notificaciones de la interfaz.

Las operaciones de alta, modificación y eliminación muestran mensajes que se ocultan automáticamente después de tres segundos.

## 5. Requisitos de ejecución

Se necesita:

- Node.js compatible con Vite 8.
- pnpm.
- Backend de la Unidad 9 en ejecución.

El frontend utiliza por defecto la API:

`http://localhost:8000/api/v1`

El backend debe estar iniciado antes de probar el inicio de sesión y las operaciones del catálogo.

## 6. Instalación

Abrir una terminal dentro de la carpeta del frontend y ejecutar:

```powershell
pnpm install
```

Iniciar el proyecto:

```powershell
pnpm dev
```

Abrir en el navegador:

`http://localhost:5173`

Para verificar la compilación:

```powershell
pnpm build
```

## 7. Pruebas funcionales

Para comprobar la aplicación:

1. Iniciar sesión con un usuario válido.
2. Recargar la página y comprobar la recuperación de la sesión.
3. Acceder a las rutas de categorías, productos e ingredientes.
4. Con rol admin, crear, editar y eliminar registros.
5. Comprobar las notificaciones de las operaciones.
6. Alternar el tema y verificar que persiste al recargar.
7. Comprobar la redirección al login cuando no existe sesión.
8. Con rol user, intentar acceder a `/admin/users` y verificar la redirección a `/unauthorized`.
9. Comprobar que el frontend compila sin errores.

## 8. Consideraciones

El backend FastAPI de la Unidad 9 se reutiliza sin modificaciones.
La autenticación utiliza una cookie HttpOnly. El frontend no almacena el JWT en localStorage.
El proyecto se entrega sin `node_modules` ni archivos de compilación generados.
