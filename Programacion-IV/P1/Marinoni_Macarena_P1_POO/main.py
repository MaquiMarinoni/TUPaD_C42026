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
)
from libreria_externa import FichaPuntoDeVenta


def main() -> None:
    print("=" * 70)
    print("               FOOD STORE - CATÁLOGO Y DEMOSTRACIÓN")
    print("=" * 70)

    # configuración de Unidades de medida y categorías
    u_unidad = UnidadMedida("Unidad", "u", "conteo")
    u_kg = UnidadMedida("Kilogramo", "kg", "masa")

    cat_almacen = Categoria("Almacén", "Artículos de almacén general")
    cat_bebidas = Categoria("Bebidas", "Gaseosas, jugos y aguas")
    cat_fiambreria = Categoria("Fiambrería", "Embutidos y quesos")
    cat_combos = Categoria("Combos", "Promociones especiales")
    cat_promos = Categoria("Promociones", "Ofertas destacadas")

    # componentes base para combos
    pan = ProductoSimple("Pan Criollo", 1200.0, 50.0, cat_almacen, u_kg)
    salame = ProductoPorPeso("Salame Milán", 15000.0, 8.0, cat_fiambreria, u_kg)

    # catálogo principal
    # Producto 1: Simple
    gaseosa = ProductoSimple("Gaseosa Cola 2.25L", 2500.0, 30.0, cat_bebidas, u_unidad)
    gaseosa.clasificar_en(cat_almacen, es_principal=False)

    # Producto 2: Por Peso
    queso_barra = ProductoPorPeso("Queso Barra", 9200.0, 15.0, cat_fiambreria, u_kg)

    # Producto 3: Simple
    aceite = ProductoSimple("Aceite de Oliva 500ml", 6800.0, 20.0, cat_almacen, u_unidad)

    # Producto 4: Combo (Agregación)
    combo_picada = ProductoCombo(
        nombre="Combo Picada Clásica",
        categoria_principal=cat_combos,
        componentes=[pan, salame],
        descuento=0.15,
    )

    catalogo_comercio: list[Producto] = [gaseosa, queso_barra, aceite, combo_picada]

    print("\n>>> CATÁLOGO DE PRODUCTOS EN MEMORIA")
    print("-" * 70)
    for p in catalogo_comercio:
        print(f"• {p.nombre:25} | Publicado: {p.precio_publicado:15} | Cat. Principal: {p.categoria_principal().nombre}")
        print(f"  Disponible: {p.disponible} | Clasificaciones: {[c.categoria.nombre for c in p.categorias()]}")

    print("\n>>> CÁLCULO POLIMÓRFICO DE PRECIOS FINALES")
    print("-" * 70)
    print(f"• {gaseosa.nombre} (x3 u): $ {gaseosa.precio_final(3.0):.2f}")
    print(f"• {queso_barra.nombre} (x0.350 kg): $ {queso_barra.precio_final(0.350):.2f}")
    print(f"• {aceite.nombre} (x2 u): $ {aceite.precio_final(2):.2f}")
    print(f"• {combo_picada.nombre} (x2 combos): $ {combo_picada.precio_final(2):.2f}")

    print("\n>>> DEMOSTRACIÓN DE DECISIONES DE DISEÑO")
    print("-" * 70)

    # Decisión 1: Composición en ProductoCategoria
    print("1. COMPOSICIÓN (Invariante de categoría principal y protección):")
    print(f"   Categoría principal inicial de gaseosa: {gaseosa.categoria_principal().nombre}")
    # clasifica en una nueva categoría definiéndola como principal
    gaseosa.clasificar_en(cat_promos, es_principal=True)
    print(f"   Nueva categoría principal: {gaseosa.categoria_principal().nombre}")
    print(f"   Total clasificaciones: {[c.categoria.nombre for c in gaseosa.categorias()]}")
    print(f"   Retorno de categorias() es tupla protegida: {type(gaseosa.categorias()).__name__}")

    # demostración del rechazo a duplicados
    try:
        gaseosa.clasificar_en(cat_almacen)
    except ErrorValidacionCatalogo as e:
        print(f"   [OK] Captura de intento de clasificar duplicado: {e}")

    # Decisión 2: agregación en ProductoCombo
    print("\n2. AGREGACIÓN (Los componentes sobreviven al combo y se reagrupan):")
    del combo_picada
    print(f"   Componente pan sigue vivo tras eliminar combo: {pan.nombre} ($ {pan.precio_base:.2f})")
    combo_desayuno = ProductoCombo("Combo Desayuno", cat_combos, [pan, gaseosa], descuento=0.10)
    print(f"   Pan reagrupado en nuevo combo: {combo_desayuno.nombre} | {combo_desayuno.precio_publicado}")

    # Decisión 3: falla temprana al instanciar clase abstracta
    print("\n3. FALLA TEMPRANA (ABC):")
    try:
        Producto("Abstracto", 100.0, 5.0, cat_almacen)  # type: ignore
    except TypeError as e:
        print(f"   [OK] Falla al construir Producto abstracto sin método precio_final: {e}")

    # Decisión 4: vidriera transitoria
    queso_destacado = ProductoDestacado(queso_barra, orden_vidriera=1)
    print(f"\n4. PRODUCTO DESTACADO (Envoltorio Decorador):")
    print(f"   {queso_destacado.nombre} en vidriera con orden {queso_destacado.orden_vidriera}")
    print(f"   Precio publicado delegado: {queso_destacado.precio_publicado}")

    # exportación polimórfica conjunta con FichaPuntoDeVenta
    print("\n>>> EXPORTACIÓN POLIMÓRFICA (Protocol Exportable)")
    print("-" * 70)
    ficha_externa = FichaPuntoDeVenta(codigo="POS-9988", detalle="Caja Central Entrada")
    lote_exportable = [gaseosa, queso_barra, aceite, combo_desayuno, queso_destacado, ficha_externa]

    lineas = exportar_catalogo(lote_exportable)
    for linea in lineas:
        print(f"  [EXPORT] {linea}")

    print("\n" + "=" * 70)
    print("DEMOSTRACIÓN FINALIZADA CON ÉXITO")
    print("=" * 70)


if __name__ == "__main__":
    main()