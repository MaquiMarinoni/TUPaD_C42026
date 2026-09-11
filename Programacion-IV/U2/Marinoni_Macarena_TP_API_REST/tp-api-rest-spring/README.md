# Sistema de Gestión de Pedidos - API REST 🛒

Trabajo Práctico N.º 2 - Programación IV - Spring Boot

## 📋 Descripción

API REST para un sistema de gestión de pedidos desarrollada con Spring Boot.

El proyecto implementa una arquitectura en capas para administrar usuarios, categorías, productos y pedidos, utilizando Spring Data JPA para la persistencia de datos y DTOs con Records para la transferencia de información.

La API permite realizar operaciones mediante distintos métodos HTTP, incorpora validaciones de datos, manejo centralizado de excepciones y documentación interactiva con Swagger/OpenAPI.

## 🏗️ Arquitectura

El proyecto utiliza una arquitectura en capas:

```text
com.gestion.pedidos/
├── entity/              # Entidades JPA
│   ├── Usuario
│   ├── Pedido
│   ├── DetallePedido
│   ├── Producto
│   └── Categoria
│
├── dto/                 # Data Transfer Objects (Records)
│   ├── usuario/
│   ├── pedido/
│   ├── detallepedido/
│   ├── producto/
│   └── categoria/
│
├── repository/          # Acceso a datos con Spring Data JPA
│   ├── UsuarioRepository
│   ├── PedidoRepository
│   ├── DetallePedidoRepository
│   ├── ProductoRepository
│   └── CategoriaRepository
│
├── service/             # Lógica de negocio
│   ├── UsuarioService
│   ├── PedidoService
│   ├── ProductoService
│   └── CategoriaService
│
├── controller/          # Endpoints de la API REST
│   ├── UsuarioController
│   ├── PedidoController
│   ├── ProductoController
│   └── CategoriaController
│
└── exception/           # Manejo centralizado de excepciones
    └── AdviceController
```

## ✨ Características principales

### 1. API REST

La aplicación expone endpoints REST para trabajar con:

- Usuarios
- Categorías
- Productos
- Pedidos

Se utilizan los métodos HTTP:

- `GET` para consultas.
- `POST` para creación de recursos.
- `PUT` para actualización.
- `PATCH` para actualización parcial de productos.
- `DELETE` para eliminación lógica.

### 2. Arquitectura en capas

La aplicación separa responsabilidades mediante:

```text
Controller
    ↓
Service
    ↓
Repository
    ↓
Base de datos
```

Los Controllers reciben las solicitudes HTTP, los Services contienen la lógica de negocio y los Repositories realizan el acceso a los datos.

### 3. Inyección de dependencias

Se utiliza inyección de dependencias por constructor mediante Lombok:

```java
@RequiredArgsConstructor
```

junto con los estereotipos correspondientes de Spring, como:

```java
@Service
@Repository
@RestController
@ControllerAdvice
```

### 4. DTOs con Records

Los datos recibidos y enviados por la API se manejan mediante DTOs implementados como Records de Java.

Ejemplo:

```java
public record ProductoCreate(
        String nombre,
        String descripcion,
        Double precio,
        Integer stock,
        Long categoriaId
) {
}
```

Esto permite separar las entidades JPA de la información expuesta por la API.

### 5. Validaciones

Se utiliza Bean Validation para validar los datos recibidos al crear productos.

Entre las validaciones implementadas se encuentran:

- Nombre obligatorio.
- Precio obligatorio y mayor a cero.
- Stock obligatorio y no negativo.
- Categoría obligatoria.

Ejemplo:

```java
@NotBlank(message = "El nombre es obligatorio")
String nombre,
