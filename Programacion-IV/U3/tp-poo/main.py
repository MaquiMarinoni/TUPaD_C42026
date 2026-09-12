import figuras
from libreria_externa import PlanoCAD

def main():
    print("--- 1. CONSTRUCCIÓN DE DOMINIO ---")
    
    # Asociación (0..1): Etiquetas independientes que existen por sí solas
    eti_techo = figuras.Etiqueta("Lado Superior")
    eti_base = figuras.Etiqueta("Lado Inferior")

    # Composición (*--): Los Lados nacen dentro del Polígono. 
    # Su ciclo de vida está atado al de la figura.
    triangulo = figuras.Triangulo("Triángulo A", "Rojo", [
        figuras.Lado(3, eti_techo), figuras.Lado(4), figuras.Lado(5)
    ])
    cuadrado = figuras.Cuadrado("Cuadrado B", "Azul", [
        figuras.Lado(2, eti_base), figuras.Lado(2), figuras.Lado(2), figuras.Lado(2)
    ])
    
    # Factory Function (Rediseño de jerarquía)
    pentagono = figuras.fabricar_poligono_regular("Pentágono C", "Verde", 5, 5)
    hexagono = figuras.fabricar_poligono_regular("Hexágono D", "Amarillo", 4, 6)

    # Agregación (o--): El Taller recibe objetos que ya fueron construidos afuera
    mi_taller = figuras.Taller()
    for p in [triangulo, cuadrado, pentagono, hexagono]:
        mi_taller.recibir(p)
        
    print(f"[Inventario] Taller inicializado con {len(mi_taller.inventario())} polígonos.")

    print("\n--- 2. DEMOSTRACIÓN DE AGREGACIÓN ---")
    # Destruimos el Taller para demostrar que los polígonos sobreviven
    del mi_taller
    print(f"El Taller fue destruido (del mi_taller). ¿Sobrevive el Cuadrado? Sí, su nombre sigue siendo: '{cuadrado._nombre}'")

    print("\n--- 3. EXPORTACIÓN CONTRATO ESTRUCTURAL (Protocol) ---")
    mi_plano = PlanoCAD("Planta Baja", "1:100")
    
    # Mezclamos nuestros Polígonos con un objeto de una librería externa
    elementos = [triangulo, cuadrado, pentagono, hexagono, mi_plano]
    resultados = figuras.exportar_todo(elementos)
    for r in resultados:
        print(r)

    print("\n--- 4. DEMOSTRACIÓN DE FALLA TEMPRANA (ABC) ---")
    class FiguraRota(figuras.Poligono):
        # Subclase que NO implementa lados_esperados()
        pass 
    
    try:
        f = FiguraRota("Figura Rota", "Gris", [])
    except TypeError as e:
        print(f"[Éxito] Python impidió la construcción (reventó al instanciar): \n{e}")

if __name__ == "__main__":
    main()