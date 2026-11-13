from app.core.security import hash_password
from app.models.categoria import Categoria
from app.models.producto import Producto
from app.models.usuario import Usuario
from app.uow.unit_of_work import UnitOfWork


CATEGORIAS = [
    ("Bebidas", "Bebidas sin alcohol"),
    ("Almacen", "Productos de almacen"),
    ("Panaderia", "Productos de panaderia"),
]

PRODUCTOS = [
    ("Agua mineral 500 ml", "Bebidas", 1200, 40),
    ("Gaseosa cola 1.5 L", "Bebidas", 2800, 25),
    ("Jugo de naranja 1 L", "Bebidas", 2300, 20),
    ("Arroz 1 kg", "Almacen", 1900, 30),
    ("Fideos 500 g", "Almacen", 1500, 35),
    ("Aceite de girasol 900 ml", "Almacen", 3500, 18),
    ("Pan lactal", "Panaderia", 3200, 15),
    ("Galletitas dulces", "Panaderia", 1700, 28),
]


def ejecutar_seed():
    with UnitOfWork() as uow:
        admin = uow.usuarios.get_by_username("admin")

        if admin is None:
            admin = Usuario(
                username="admin",
                full_name="Administrador Food Store",
                email="admin@foodstore.example.com",
                hashed_password=hash_password("Admin1234!"),
                role="admin",
                disabled=False,
            )
            uow.usuarios.add(admin)
            print("Administrador creado")
        else:
            print("Administrador ya existente")

        categorias = {}

        for nombre, descripcion in CATEGORIAS:
            categoria = uow.categorias.get_by_nombre(nombre)

            if categoria is None:
                categoria = Categoria(
                    nombre=nombre,
                    descripcion=descripcion,
                    activo=True,
                )
                uow.categorias.add(categoria)
                print(f"Categoria creada: {nombre}")

            categorias[nombre] = categoria.id

        for nombre, categoria_nombre, precio, stock in PRODUCTOS:
            categoria_id = categorias[categoria_nombre]

            existente = uow.session.query(Producto).filter(
                Producto.nombre == nombre,
                Producto.categoria_id == categoria_id,
            ).first()

            if existente is None:
                producto = Producto(
                    nombre=nombre,
                    categoria_id=categoria_id,
                    descripcion=f"Producto {nombre}",
                    precio_base=precio,
                    stock=stock,
                    disponible=True,
                    activo=True,
                )
                uow.productos.add(producto)
                print(f"Producto creado: {nombre}")

    print("Seed finalizado correctamente")


if __name__ == "__main__":
    ejecutar_seed()
