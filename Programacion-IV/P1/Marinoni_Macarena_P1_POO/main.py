# main.py
"""Demostración integral y validación de Historias de Usuario (HU).

Parcial 1 - Programación IV - UTN
"""

from catalogo import (
    Categoria,
    UnidadMedida,
    Producto,
    ProductoSimple,
    ProductoPorPeso,
    ProductoCombo,
    ProductoDestacado,
    exportar_catalogo,
    ErrorValidacionCatalogo,
    ErrorCatalogo,
)
from libreria_externa import FichaPuntoDeVenta


def probar_hu_01() -> None:
    print("\n" + "=" * 60)
    print("DEMOSTRACIÓN HU-P1-01: MODELADO Y ENCAPSULAMIENTO")
    print("=" * 60)

    # 1. Inmutabilidad de UnidadMedida (frozen dataclass)
    unidad_kg = UnidadMedida(nombre="Kilogramo", simbolo="kg", tipo="masa")
    unidad_u = UnidadMedida(nombre="Unidad", simbolo="u", tipo="conteo")
    print(f"[OK] Unidad de medida inmutable instanciada: {unidad_kg}")

    # 2. Categoría con validación y encapsulamiento
    cat_fiambreria = Categoria("Fiambrería", "Quesos y embutidos")
    print(f"[OK] Categoría creada: {cat_fiambreria.nombre} - {cat_fiambreria.descripcion}")

    # 3. Validación en construcción: nombre vacío
    try:
        Categoria("   ")
    except ErrorValidacionCatalogo as e:
        print(f"[OK] Validación de categoría vacía capturada: {e}")

    # 4. ProductoSimple: validación de stock y precio base
    queso = ProductoPorPeso("Queso Pategrás", 9500.0, 15.0, cat_fiambreria, unidad_kg)
    print(f"[OK] Producto creado: {queso.nombre}")
    print(f"     - Precio publicado: {queso.precio_publicado}")
    print(f"     - Disponible (habilitado y stock > 0): {queso.disponible}")

    # 5. Cálculo dinámico de disponibilidad
    queso.deshabilitar()
    print(f"     - Disponible tras deshabilitar(): {queso.disponible}")
    queso.habilitar()


def probar_hu_02() -> None:
    print("\n" + "=" * 60)
    print("DEMOSTRACIÓN HU-P1-02: RELACIONES ESTRUCTURALES")
    print("=" * 60)

    cat_almacen = Categoria("Almacén")
    cat_bebidas = Categoria("Bebidas")
    cat_promos = Categoria("Promociones")
    u_u = UnidadMedida("Unidad", "u", "conteo")

    # 1. Composición y unicidad de categoría principal
    gaseosa = ProductoSimple("Gaseosa Cola 2L", 2200.0, 30.0, cat_almacen, u_u)
    print(f"[OK] Creado con categoría principal: {gaseosa.categoria_principal().nombre}")

    # Clasificación adicional que pasa a ser la principal
    gaseosa.clasificar_en(cat_bebidas, es_principal=True)
    print(f"[OK] Reclasificado. Nueva categoría principal: {gaseosa.categoria_principal().nombre}")
    print(f"     Total clasificaciones activas: {len(gaseosa.categorias())}")

    # Rechazo a duplicar categoría
    try:
        gaseosa.clasificar_en(cat_bebidas)
    except ErrorValidacionCatalogo as e:
        print(f"[OK] Rechazo a clasificar categoría duplicada: {e}")

    # Colección protegida: tupla inmutable
    try:
        gaseosa.categorias().append("inyeccion_invalida")  # type: ignore
    except AttributeError:
        print("[OK] Las clasificaciones retornan tuple inmutable (protegida contra append)")

    # 2. Agregación en ProductoCombo (requiere >= 2 componentes)
    galletitas = ProductoSimple("Galletitas Dulces", 1300.0, 20.0, cat_almacen, u_u)

    try:
        ProductoCombo("Combo Inválido", cat_promos, [gaseosa])
    except ErrorValidacionCatalogo as e:
        print(f"[OK] Validación de combo con menos de 2 componentes: {e}")

    combo_merienda = ProductoCombo("Combo Merienda", cat_promos, [gaseosa, galletitas], descuento=0.10)
    print(f"[OK] Combo creado exitosamente (Agregación de 2 productos preexistentes)")
    print(f"     - Precio publicado (suma con 10% desc): {combo_merienda.precio_publicado}")
    print(f"     - Componentes agregados: {[p.nombre for p in combo_merienda.componentes()]}")


def probar_hu_03() -> None:
    print("\n" + "=" * 60)
    print("DEMOSTRACIÓN HU-P1-03: HERENCIA, ABC Y DECORADOR")
    print("=" * 60)

    cat_test = Categoria("General")

    # 1. Falla temprana de la clase abstracta (ABC)
    try:
        Producto("Genérico", 100.0, 5.0, cat_test)  # type: ignore
    except TypeError as e:
        print(f"[OK] Falla temprana: No se puede instanciar la clase abstracta Producto: {e}")

    # 2. Polimorfismo de precio_final()
    u_kg = UnidadMedida("Kilogramo", "kg", "masa")
    u_u = UnidadMedida("Unidad", "u", "conteo")
    prod_simple = ProductoSimple("Pan Lactal", 1500.0, 10.0, cat_test, u_u)
    prod_peso = ProductoPorPeso("Jamón Cocido", 12000.0, 8.0, cat_test, u_kg)

    print(f"[OK] Polimorfismo ProductoSimple (2 u): $ {prod_simple.precio_final(2):.2f}")
    print(f"[OK] Polimorfismo ProductoPorPeso (0.250 kg): $ {prod_peso.precio_final(0.250):.2f}")

    # 3. Rol transitorio de vidriera (ProductoDestacado por Composición)
    destacado = ProductoDestacado(prod_peso, orden_vidriera=1)
    print(f"[OK] Producto destacado en vidriera (envoltorio):")
    print(f"     - Nombre delegado: {destacado.nombre}")
    print(f"     - Orden vidriera: {destacado.orden_vidriera}")
    print(f"     - Precio delegado (0.250 kg): $ {destacado.precio_final(0.250):.2f}")


def probar_hu_04() -> None:
    print("\n" + "=" * 60)
    print("DEMOSTRACIÓN HU-P1-04: CONTRATOS Y PROTOCOL")
    print("=" * 60)

    cat = Categoria("General")
    u = UnidadMedida("Unidad", "u", "conteo")
    prod = ProductoSimple("Café Molido", 4500.0, 10.0, cat, u)
    dest = ProductoDestacado(prod, orden_vidriera=2)
    ficha_externa = FichaPuntoDeVenta("POS-8821", "Caja Registradora Sector B")

    # Exportación polimórfica combinando clases del dominio y librería externa no modificada
    lote = [prod, dest, ficha_externa]
    lineas = exportar_catalogo(lote)

    print("[OK] Exportación exitosa de lote heterogéneo cumpliendo Protocol Exportable:")
    for linea in lineas:
        print(f"     -> {linea}")

    # Validación defensiva ante objetos que no cumplen el protocolo
    try:
        exportar_catalogo([prod, 12345])  # type: ignore
    except ErrorValidacionCatalogo as e:
        print(f"[OK] Rechazo a objeto que no cumple el contrato: {e}")


def main() -> None:
    print("INICIANDO SUITE DE VALIDACIÓN - EVALUACIÓN PARCIAL 1 (POO)")
    probar_hu_01()
    probar_hu_02()
    probar_hu_03()
    probar_hu_04()
    print("\n" + "=" * 60)
    print("TODAS LAS HISTORIAS DE USUARIO FUERON VALIDADAS CON ÉXITO")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()