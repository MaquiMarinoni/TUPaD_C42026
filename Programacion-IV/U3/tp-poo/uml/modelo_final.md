```mermaid
classDiagram
    class Figura {
        #_nombre: str
        #_color: str
        #_construida: bool
        +area() float
    }

    class Exportable {
        <<Protocol>>
        +exportar() str
    }

    class Poligono {
        <<ABC>>
        #_lados: list
        #_observaciones: list
        +lados_esperados()* int
        +perimetro() float
        +area() float
        +exportar() str
    }

    class Taller {
        -_poligonos: list
        +recibir(poligono)
        +restaurar(poligono)
        +inventario() tuple
    }

    class Lado {
        -_longitud: float
        -_etiqueta: Etiqueta
        +longitud() float
        +etiqueta() Etiqueta
    }

    class Etiqueta {
        <<dataclass frozen>>
        +texto: str
    }

    class Triangulo
    class Cuadrado
    class Pentagono
    class Hexagono

    class PlanoCAD {
        <<Libreria Externa>>
        +exportar() str
    }

    %% Relaciones de Herencia Nominal
    Figura <|-- Poligono
    Poligono <|-- Triangulo
    Poligono <|-- Cuadrado
    Poligono <|-- Pentagono
    Poligono <|-- Hexagono

    %% Contrato Estructural (Duck Typing)
    Exportable <|.. Poligono : cumple
    Exportable <|.. PlanoCAD : cumple

    %% Relaciones Estructurales con Multiplicidad
    Taller "1" o-- "0..*" Poligono : Agregación
    Poligono "1" *-- "3..*" Lado : Composición
    Lado "1" --> "0..1" Etiqueta : Asociación