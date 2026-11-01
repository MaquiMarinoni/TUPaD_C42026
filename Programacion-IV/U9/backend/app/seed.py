import json
from sqlmodel import Session, select

from app.categoria.model import Categoria
from app.core.database import engine
from app.ingrediente.model import Ingrediente
from app.producto.model import Producto, ProductoCategoria, ProductoIngrediente
from app.unidad_medida.model import UnidadMedida


def run_catalog_seed() -> None:
    with Session(engine) as session:
        # 1. Seed de Unidades de Medida (Catálogo solo lectura)
        if not session.exec(select(UnidadMedida)).first():
            unidades_iniciales = [
                UnidadMedida(id=1, nombre="kilogramo", simbolo="kg", tipo="masa"),
                UnidadMedida(id=2, nombre="gramo", simbolo="g", tipo="masa"),
                UnidadMedida(id=3, nombre="litro", simbolo="L", tipo="volumen"),
                UnidadMedida(id=4, nombre="mililitro", simbolo="mL", tipo="volumen"),
                UnidadMedida(id=5, nombre="pieza", simbolo="u", tipo="unidad"),
                UnidadMedida(id=6, nombre="docena", simbolo="doc", tipo="unidad"),
                UnidadMedida(id=7, nombre="metro cuadrado", simbolo="m²", tipo="area"),
            ]
            session.add_all(unidades_iniciales)
            session.commit()

        # 2. Seed de Categorías iniciales
        if not session.exec(select(Categoria)).first():
            categorias_iniciales = [
                Categoria(nombre="Hamburguesas", descripcion="Hamburguesas caseras y gourmet"),
                Categoria(nombre="Pizzas", descripcion="Pizzas a la piedra y media masa"),
                Categoria(nombre="Bebidas", descripcion="Gaseosas, aguas saborizadas y cervezas"),
                Categoria(nombre="Postres", descripcion="Helados, tortas y postres caseros"),
                Categoria(nombre="Ensaladas", descripcion="Opciones frescas y saludables"),
                Categoria(nombre="Papas Fritas", descripcion="Porciones de papas con distintos toppings"),
            ]
            session.add_all(categorias_iniciales)
            session.commit()

        # 3. Seed de Ingredientes iniciales
        if not session.exec(select(Ingrediente)).first():
            ingredientes_iniciales = [
                Ingrediente(nombre="Medallón de carne", descripcion="Carne vacuna 150g", unidad_medida_id=2),
                Ingrediente(nombre="Queso Cheddar", descripcion="Fetas de cheddar", unidad_medida_id=2),
                Ingrediente(nombre="Pan de papa", descripcion="Pan artesanal brioche", unidad_medida_id=5),
                Ingrediente(nombre="Mozzarella", descripcion="Queso mozzarella rallado", unidad_medida_id=2),
            ]
            session.add_all(ingredientes_iniciales)
            session.commit()

        # 4. Seed de Productos iniciales con sus relaciones
        if not session.exec(select(Producto)).first():
            p1 = Producto(
                nombre="Hamburguesa Doble Cheddar",
                descripcion="Doble medallón de carne con cuádruple cheddar y pan de papa",
                precio_base=9500.0,
                imagenes_url=json.dumps(["https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500"]),
                disponible=True,
            )
            p2 = Producto(
                nombre="Pizza Napolitana",
                descripcion="Salsa de tomate, mozzarella, rodajas de tomate fresco y ajo",
                precio_base=11200.0,
                imagenes_url=json.dumps(["https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=500"]),
                disponible=True,
            )
            session.add_all([p1, p2])
            session.commit()
            session.refresh(p1)
            session.refresh(p2)

            session.add_all([
                ProductoCategoria(producto_id=p1.id, categoria_id=1, es_principal=True),
                ProductoCategoria(producto_id=p2.id, categoria_id=2, es_principal=True),
                ProductoIngrediente(producto_id=p1.id, ingrediente_id=1, cantidad=300),
                ProductoIngrediente(producto_id=p1.id, ingrediente_id=2, cantidad=80),
                ProductoIngrediente(producto_id=p1.id, ingrediente_id=3, cantidad=1),
                ProductoIngrediente(producto_id=p2.id, ingrediente_id=4, cantidad=250),
            ])
            session.commit()


def run_seed() -> None:
    from app.core.config import settings
    from app.core.security import hash_password
    from app.modules.usuarios.model import Usuario, Rol, UsuarioRol
    from app.modules.usuarios.schema import UserCreate
    from app.pedidos.models import EstadoPedido, FormaPago
    with Session(engine) as session:
        for nombre, descripcion in [("admin", "Administración"), ("user", "Usuario del sistema")]:
            if session.exec(select(Rol).where(Rol.nombre == nombre)).first() is None:
                session.add(Rol(nombre=nombre, descripcion=descripcion))
        for i, codigo in enumerate(["PENDIENTE", "CONFIRMADO", "EN_PREP", "EN_CAMINO", "ENTREGADO", "CANCELADO"], 1):
            if session.get(EstadoPedido, codigo) is None:
                session.add(EstadoPedido(codigo=codigo, descripcion=codigo.replace("_", " ").capitalize(), orden=i, es_terminal=i >= 5))
        if session.get(FormaPago, "EFECTIVO") is None:
            session.add(FormaPago(codigo="EFECTIVO", descripcion="Efectivo"))
        session.commit()
        if settings.ADMIN_EMAIL or settings.ADMIN_PASSWORD:
            data = UserCreate(nombre="Admin", apellido="FoodStore", email=settings.ADMIN_EMAIL, password=settings.ADMIN_PASSWORD)
            email = str(data.email).lower()
            # Nunca promueve una cuenta existente ni restablece su contraseña al reiniciar.
            if session.exec(select(Usuario).where(Usuario.email == email)).first() is None:
                user = Usuario(nombre=data.nombre, apellido=data.apellido, email=email, password_hash=hash_password(data.password))
                session.add(user)
                session.flush()
                role = session.exec(select(Rol).where(Rol.nombre == "admin")).one()
                session.add(UsuarioRol(usuario_id=user.id, rol_id=role.id))
                session.commit()
    run_catalog_seed()


if __name__ == "__main__":
    from app.core.database import create_db_and_tables
    create_db_and_tables()
    run_seed()
