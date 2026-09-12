"""Módulo de Dominio: Figuras, Polígonos y Taller."""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Protocol
from libreria_externa import PlanoCAD 

class Exportable(Protocol):
    def exportar(self) -> str:
        ...

@dataclass(frozen=True)
class Etiqueta:
    texto: str

class Figura:
    def __init__(self, nombre, color):
        self._nombre = nombre
        self._color = color
        self._construida = True  

    def area(self) -> float:
        return 0.0

class Lado:
    def __init__(self, longitud, etiqueta=None):
        self.longitud = longitud
        self._etiqueta = etiqueta

    @property
    def longitud(self):
        return self._longitud

    @longitud.setter
    def longitud(self, valor):
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = valor

    @property
    def etiqueta(self):
        return self._etiqueta

class Poligono(Figura, ABC):
    def __init__(self, nombre, color, lados=None, observaciones=None):
        super().__init__(nombre, color)
        self._lados = lados if lados is not None else []
        self._observaciones = observaciones if observaciones is not None else []
        
        if self._lados and len(self._lados) != self.lados_esperados():
            raise ValueError(f"Error: {nombre} esperaba {self.lados_esperados()} lados, pero recibió {len(self._lados)}.")

    @abstractmethod
    def lados_esperados(self):
        pass

    def perimetro(self) -> float:
        return sum(l.longitud for l in self._lados)

    def area(self) -> float:
        return 0.0

    def agregar_observacion(self, texto):
        self._observaciones.append(texto)

    def lados(self):
        return tuple(self._lados)
        
    def exportar(self) -> str:
        return f"Polígono: {self._nombre} | Color: {self._color} | Lados: {len(self._lados)}"

class Taller:
    def __init__(self):
        self._poligonos = []

    def recibir(self, poligono):
        self._poligonos.append(poligono)

    def restaurar(self, poligono):
        poligono._observaciones.clear()

    def inventario(self):
        return tuple(self._poligonos)

class Triangulo(Poligono):
    def __init__(self, nombre="triángulo", color="negro", lados=None):
        super().__init__(nombre, color, lados)

    def lados_esperados(self):
        return 3

class Cuadrado(Poligono):
    def __init__(self, nombre="cuadrado", color="negro", lados=None):
        super().__init__(nombre, color, lados)

    def lados_esperados(self):
        return 4

class Pentagono(Poligono):
    def __init__(self, nombre="pentágono", color="negro", lados=None):
        super().__init__(nombre, color, lados)

    def lados_esperados(self):
        return 5

class Hexagono(Poligono):
    def __init__(self, nombre="hexágono", color="negro", lados=None):
        super().__init__(nombre, color, lados)

    def lados_esperados(self):
        return 6

def fabricar_poligono_regular(nombre, color, medida, cantidad):
    lados_generados = [Lado(medida) for _ in range(cantidad)]
    
    if cantidad == 3:
        return Triangulo(nombre, color, lados_generados)
    elif cantidad == 4:
        return Cuadrado(nombre, color, lados_generados)
    elif cantidad == 5:
        return Pentagono(nombre, color, lados_generados)
    elif cantidad == 6:
        return Hexagono(nombre, color, lados_generados)
    else:
        raise ValueError(f"No hay una clase específica para un polígono de {cantidad} lados.")

def exportar_todo(items: list[Exportable]) -> list[str]:
    return [item.exportar() for item in items]