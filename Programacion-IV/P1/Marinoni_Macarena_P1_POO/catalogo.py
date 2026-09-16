
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

# --- Excepciones de Dominio ---

class ErrorCatalogo(ValueError):
    """Excepción base para los errores de la aplicación de catálogo."""
    pass

class ErrorValidacionCatalogo(ErrorCatalogo):
    """Lanzada cuando fallan las validaciones de datos o invariantes del catálogo."""
    pass


# --- Modelado del Catálogo ---

@dataclass(frozen=True)
class UnidadMedida:
    nombre: str
    simbolo: str
    tipo: str


class Categoria:
    """Agrupa productos del catálogo."""

    def __init__(self, nombre: str, descripcion: str = "") -> None:
        if not nombre or not nombre.strip():
            raise ErrorValidacionCatalogo("El nombre de la categoría no puede estar vacío.")
        self._nombre: str = nombre.strip()
        self._descripcion: str = descripcion.strip() if descripcion else ""

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion

    def __repr__(self) -> str:
        return f"Categoria(nombre='{self._nombre}')"

class ProductoCategoria:
    """Vínculo de clasificación entre un Producto y una Categoria."""

    def __init__(self, categoria: Categoria, es_principal: bool = False) -> None:
        if not isinstance(categoria, Categoria):
            raise ErrorValidacionCatalogo("La clasificación requiere una instancia válida de Categoria.")
        self._categoria: Categoria = categoria
        self._es_principal: bool = bool(es_principal)

    @property
    def categoria(self) -> Categoria:
        return self._categoria

    @property
    def es_principal(self) -> bool:
        return self._es_principal

    def _marcar_principal(self, valor: bool) -> None:
        """Método protegido para que el Producto dueño gestione el invariante de principal."""
        self._es_principal = bool(valor)

    def __repr__(self) -> str:
        return f"ProductoCategoria(categoria='{self._categoria.nombre}', es_principal={self._es_principal})"

class Producto(ABC):
    """Clase base abstracta del catálogo."""

    def __init__(
        self,
        nombre: str,
        precio_base: float,
        stock_cantidad: float,
        categoria_principal: Categoria,
        unidad_venta: UnidadMedida | None = None,
    ) -> None:
        if not nombre or not nombre.strip():
            raise ErrorValidacionCatalogo("El nombre del producto no puede estar vacío.")
        if precio_base < 0:
            raise ErrorValidacionCatalogo("El precio base no puede ser negativo.")
        if stock_cantidad < 0:
            raise ErrorValidacionCatalogo("El stock no puede ser negativo.")
        if not isinstance(categoria_principal, Categoria):
            raise ErrorValidacionCatalogo("Debe proporcionar una Categoria principal válida.")
        if unidad_venta is not None and not isinstance(unidad_venta, UnidadMedida):
            raise ErrorValidacionCatalogo("La unidad de venta debe ser una instancia de UnidadMedida o None.")

        self._nombre: str = nombre.strip()
        self._precio_base: float = float(precio_base)
        self._stock_cantidad: float = float(stock_cantidad)
        self._habilitado: bool = True
        self._unidad_venta: UnidadMedida | None = unidad_venta

        # Composición: el todo fabrica internamente la parte
        self._clasificaciones: list[ProductoCategoria] = [
            ProductoCategoria(categoria_principal, es_principal=True)
        ]

    # --- Properties de Solo Lectura y Estado Derivado ---

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @property
    def unidad_venta(self) -> UnidadMedida | None:
        return self._unidad_venta

    @property
    def disponible(self) -> bool:
        return self._habilitado and self._stock_cantidad > 0

    @property
    def precio_publicado(self) -> str:
        if self._unidad_venta is not None:
            return f"$ {self._precio_base:.2f}/{self._unidad_venta.simbolo}"
        return f"$ {self._precio_base:.2f}"

    # --- Gestión de Estado de Habilitación ---

    def habilitar(self) -> None:
        self._habilitado = True

    def deshabilitar(self) -> None:
        self._habilitado = False

    # --- Gestión de Clasificaciones (Composición e Invariante) ---

    def clasificar_en(self, categoria: Categoria, es_principal: bool = False) -> None:
        if not isinstance(categoria, Categoria):
            raise ErrorValidacionCatalogo("Se requiere una instancia válida de Categoria.")

        # Validar duplicados
        for pc in self._clasificaciones:
            if pc.categoria == categoria:
                raise ErrorValidacionCatalogo(
                    f"El producto ya se encuentra clasificado en la categoría '{categoria.nombre}'."
                )

        if es_principal:
            for pc in self._clasificaciones:
                if pc.es_principal:
                    pc._marcar_principal(False)

        nuevo_vinculo = ProductoCategoria(categoria, es_principal=es_principal)
        self._clasificaciones.append(nuevo_vinculo)

    def categorias(self) -> tuple[ProductoCategoria, ...]:
        """Retorno protegido: copia inmutable en tupla."""
        return tuple(self._clasificaciones)

    def categoria_principal(self) -> Categoria:
        for pc in self._clasificaciones:
            if pc.es_principal:
                return pc.categoria
        raise ErrorCatalogo("Estado inconsistente: el producto no posee categoría principal.")

    # --- Contrato y Exportación ---

    def exportar(self) -> str:
        return f"PRODUCTO|{self._nombre}|{self.precio_publicado}|disp={self.disponible}"

    @abstractmethod
    def precio_final(self, cantidad: float) -> float:
        """Cálculo polimórfico del precio según la subclase."""
        pass
class ProductoSimple(Producto):
    """Producto comercializado por pieza o unidad entera."""

    def precio_final(self, cantidad: float = 1.0) -> float:
        if cantidad <= 0:
            raise ErrorValidacionCatalogo("La cantidad solicitada debe ser mayor a cero.")
        return round(self._precio_base * cantidad, 2)


class ProductoPorPeso(Producto):
    """Producto comercializado por peso (admite cantidades fraccionarias)."""

    def precio_final(self, cantidad: float) -> float:
        if cantidad <= 0:
            raise ErrorValidacionCatalogo("La cantidad por peso debe ser mayor a cero.")
        return round(self._precio_base * cantidad, 2)

class ProductoCombo(Producto):
    """Agrupa entre 2 y N productos preexistentes aplicando un descuento."""

    def __init__(
        self,
        nombre: str,
        categoria_principal: Categoria,
        componentes: list[Producto],
        descuento: float = 0.10,
    ) -> None:
        if not componentes or len(componentes) < 2:
            raise ErrorValidacionCatalogo("Un combo debe contener al menos 2 productos componentes.")
        
        for comp in componentes:
            if not isinstance(comp, Producto):
                raise ErrorValidacionCatalogo("Todos los componentes de un combo deben ser instancias de Producto.")

        if not (0.0 <= descuento < 1.0):
            raise ErrorValidacionCatalogo("El descuento debe ser un valor decimal entre 0.0 y 1.0 (excluyente).")

        self._componentes: list[Producto] = list(componentes)
        self._descuento: float = float(descuento)

        # El precio base se deriva de la suma de los precios base con el descuento aplicado
        suma_base = sum(comp.precio_base for comp in self._componentes)
        precio_base_combo = round(suma_base * (1.0 - self._descuento), 2)

        super().__init__(
            nombre=nombre,
            precio_base=precio_base_combo,
            stock_cantidad=1.0,
            categoria_principal=categoria_principal,
            unidad_venta=None,
        )

    def componentes(self) -> tuple[Producto, ...]:
        """Retorno inmutable de los componentes agregados."""
        return tuple(self._componentes)

    def precio_final(self, cantidad: float = 1.0) -> float:
        if cantidad <= 0:
            raise ErrorValidacionCatalogo("La cantidad de combos solicitada debe ser mayor a cero.")
        return round(self._precio_base * cantidad, 2)

class ProductoDestacado:
    """Envoltorio que otorga visibilidad de vidriera a un Producto mediante composición."""

    def __init__(self, producto: Producto, orden_vidriera: int) -> None:
        if not isinstance(producto, Producto):
            raise ErrorValidacionCatalogo("El objeto a destacar debe ser una instancia de Producto.")
        if orden_vidriera <= 0:
            raise ErrorValidacionCatalogo("El orden de vidriera debe ser un entero positivo.")

        self._producto: Producto = producto
        self._orden_vidriera: int = int(orden_vidriera)

    @property
    def producto(self) -> Producto:
        return self._producto

    @property
    def orden_vidriera(self) -> int:
        return self._orden_vidriera

    # Delegación transparente de la interfaz de Producto
    @property
    def nombre(self) -> str:
        return self._producto.nombre

    @property
    def precio_base(self) -> float:
        return self._producto.precio_base

    @property
    def precio_publicado(self) -> str:
        return self._producto.precio_publicado

    @property
    def disponible(self) -> bool:
        return self._producto.disponible

    def precio_final(self, cantidad: float = 1.0) -> float:
        return self._producto.precio_final(cantidad)

    def exportar(self) -> str:
        return f"DESTACADO|orden={self._orden_vidriera}|{self._producto.exportar()}"

    def __repr__(self) -> str:
        return f"ProductoDestacado(producto={self._producto.nombre}, orden={self._orden_vidriera})"

class Exportable(Protocol):
    """Contrato estructural para objetos que pueden exportarse a texto."""

    def exportar(self) -> str:
        ...


def exportar_catalogo(elementos: list[Exportable]) -> list[str]:
    """Exporta de forma polimórfica una colección homogénea o heterogénea de elementos Exportable."""
    if not isinstance(elementos, list):
        raise ErrorValidacionCatalogo("La colección de elementos debe ser una lista.")

    resultado: list[str] = []
    for elem in elementos:
        # Validación defensiva en runtime de cumplimiento del protocolo
        if not hasattr(elem, "exportar") or not callable(getattr(elem, "exportar")):
            raise ErrorValidacionCatalogo(f"El objeto {elem!r} no cumple el contrato Exportable.")
        resultado.append(elem.exportar())

    return resultado