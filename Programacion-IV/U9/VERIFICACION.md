# Verificación de Unidad 9

La implementación se verificó el 1 de noviembre de 2026 en un entorno Linux con Python 3.12 y Node 24. La ejecución en la PC Windows debe confirmarse después de sincronizar el repositorio y completar el archivo .env.

| Verificación | Resultado |
|---|---|
| API: `python -m pytest -q` | 18 pruebas aprobadas |
| Frontend: `pnpm build` | Compilación TypeScript y Vite aprobada |
| Frontend: `pnpm lint` | Sin errores ni advertencias |
| Navegador Chromium: registro y credenciales inválidas | Aprobado |
| Navegador: login, perfil, recarga y logout | Aprobado |
| Navegador: user sin botones de escritura y ruta admin denegada | Aprobado |
| Navegador: cookie HttpOnly y persistencia sin token ni contraseña | Aprobado |
| Navegador: CRUD de categorías como admin | Aprobado |
| Navegador: activación/desactivación de usuarios | Aprobado |
| Navegador: cookie ausente e interceptor 401 | Redirección al login aprobada |
| Navegador: alta, edición y baja de productos con categorías | Aprobado |
| Navegador: ingredientes conservados y acceso en pantalla móvil | Aprobado |

Las pruebas de navegador se ejecutaron contra frontend y backend reales con una base SQLite temporal y cuentas de prueba. Se revisaron visualmente las pantallas de acceso y administración de usuarios. No se utiliza la base de U8.

La compilación muestra un aviso de optimización de Vite por un paquete JavaScript mayor a 500 kB. Las pruebas de API muestran un aviso de deprecación de AnyIO en TestClient. Ninguno impide ejecutar o compilar el proyecto.

## Límites de alcance

No se implementan inventario, stock, direcciones de entrega ni pantallas de pedidos nuevas. Se protege y adapta el backend de pedidos existente. El proyecto mantiene la funcionalidad de ingredientes acordada y sigue el PDF detallado para autenticación y roles.

## Historial de avances

1. Copia completa de U8 a U9.
2. Autenticación, roles, pedidos y pruebas de backend.
3. Frontend autenticado, guía de VS Code y preparación de entrega.

## Revisión de legibilidad

Se separaron los campos de login y registro, las consultas de usuarios y los pasos de creación de pedidos. Se reemplazaron condiciones encadenadas por variables intermedias y se ordenó el formato de los archivos de autenticación. Se conservaron los endpoints, las validaciones, los permisos y la configuración.

Después de esta revisión se ejecutaron nuevamente las 18 pruebas de backend, la compilación y el análisis del frontend. También se comprobó el flujo de registro, login, recarga, roles, CRUD de categorías, administración de usuarios y logout en Chromium con una base de prueba nueva. No se generaron ZIP en esta revisión.
