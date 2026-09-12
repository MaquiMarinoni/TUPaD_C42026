"""parte1_diagnostico.py — El dominio Figura / Polígono / Lado, funcionando.

⚠️ Este módulo corre de punta a punta sin lanzar un solo traceback. No tiene bugs
de sintaxis: tiene ACENTO DE JAVA.

Contiene exactamente 8 java-ismos de DISEÑO. Siete están en el checklist de la
Actividad 4; el octavo no está en ese checklist y hay que encontrarlo con criterio,
no con la lista.

Además hay ruido sintáctico (punto y coma al final de línea, comparaciones contra
True, concatenación con + donde iría un f-string). Ese ruido también se limpia, pero
NO cuenta dentro de los 8.

Tu trabajo (Parte 1): encontrarlos, listarlos en informe.md y corregirlos, cada uno
justificado con la inversión conceptual que lo explica.
"""

import math #parte 1
from dataclasses import dataclass #parte 2
from abc import ABC, abstractmethod #parte 3
from typing import Protocol #parte 4
from libreria_externa import PlanoCAD #parte 4

class Exportable(Protocol):
    def exportar(self) -> str:
        ... # Los puntos suspensivos indican que es solo la firma

def exportar_todo(items: list[Exportable]) -> list[str]:
    # Recorre la lista y llama al método exportar() de cada elemento
    return [item.exportar() for item in items]

@dataclass(frozen=True)
class Etiqueta:
    texto: str

class Figura:
    def __init__(self, nombre, color):
        self._nombre = nombre
        self._color = color
        self._construida = True   # marca de que Figura.__init__ realmente corrió

    # >>> getters preventivos SIN lógica (ceremonia de Java) <<<
    def getNombre(self):
        return self._nombre

    def getColor(self):
        return self._color

    def area(self):
        return 0.0


class Lado:
    # Relación de Asociación (0..1) con Etiqueta
    def __init__(self, longitud, etiqueta=None):
        # usa la property para que valide
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


class Poligono(Figura, ABC): # Agregamos herencia de ABC

    def __init__(self, nombre, color, lados=None, observaciones=None):
        super().__init__(nombre, color)
        self._lados = lados if lados is not None else []
        self._observaciones = observaciones if observaciones is not None else []

    # Convertimos el método en un contrato obligatorio
    @abstractmethod
    def lados_esperados(self):
        """Devuelve la cantidad de lados representada por la instancia."""
        return len(self._lados)

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
        # Agregación: 0..* (arranca vacío)
        self._poligonos = []

    def recibir(self, poligono):
        self._poligonos.append(poligono)

    def restaurar(self, poligono):
        # se limpian las observaciones
        poligono._observaciones.clear()

    def inventario(self):
        # Copia defensiva: devuelve una tupla inmutable
        return tuple(self._poligonos)

# >>> sobrecarga de constructor estilo Java: un __init__ con ramas isinstance <<<
class Triangulo(Poligono):
    # usa argumentos por defecto en lugar de *args y ramas condicionales
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

    """Polígono de N lados de igual longitud.

    ⚠️ PARTE 3 — esta clase NO es uno de los 8 java-ismos de la Parte 1.

    Se modeló heredando de Poligono para poder guardarla en la misma lista que
    los demás polígonos y recorrerla con un único tipo común. En Java esa
    herencia hacía falta; en Python no. Si su lugar en la jerarquía lo justifica
    el dominio («un polígono regular ES-UN polígono») o solamente la ceremonia
    del compilador es, exactamente, la decisión que se te pide tomar, justificar
    e IMPLEMENTAR en la Parte 3.
    """
def fabricar_poligono_regular(nombre, color, medida, cantidad):
    """Reemplazo de la clase PoligonoRegular por una Factory Function"""
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


if __name__ == "__main__":
    activo = True
    if activo:
        # prueba asociación (Etiqueta -> Lado)
        eti_base = Etiqueta("Base inferior")
        l1 = Lado(3, eti_base)
        l2 = Lado(4)
        l3 = Lado(5)
        
        # 2prueba composición (Triangulo instanciando/recibiendo sus lados)
        t = Triangulo("Triángulo", "rojo", [l1, l2, l3])
        c = Cuadrado("Cuadrado", "azul", [Lado(2), Lado(2), Lado(2), Lado(2)])
        # reemplaza la instanciación de la clase por el llamado a la fábrica
        r = fabricar_poligono_regular("Pentágono Regular", "verde", 4, 5)
        print(f"Perímetro del pentágono (vía factory): {r.perimetro()}")
        
        c.agregar_observacion("revisar el vértice A")
        
        # prueba agregación (Taller)
        mi_taller = Taller()
        mi_taller.recibir(t)
        mi_taller.recibir(c)
        mi_taller.recibir(r)
        
        # prueba la copia defensiva y la restauración
        print(f"Inventario del taller: {len(mi_taller.inventario())} polígonos")
        print(f"Observaciones del Cuadrado (ANTES): {c._observaciones}")
        print(f"Inventario final del taller: {len(mi_taller.inventario())} polígonos")
        
        mi_taller.restaurar(c)
        print(f"Observaciones del Cuadrado (DESPUÉS de restaurar): {c._observaciones}")

        # DEMOSTRACIÓN PARTE 3: Falla Temprana por contrato ABC
        print("\n--- Probando Falla Temprana (ABC) ---")
        class HeptagonoDefectuoso(Poligono):
            # Olvidamos implementar lados_esperados() a propósito
            pass
        
        try:
            # Esto debe fallar al intentar construir la instancia
            h_roto = HeptagonoDefectuoso("Heptágono Roto", "Gris", [])
        except TypeError as e:
            print(f"Falla Temprana exitosa. Python impidió la creación: {e}")

        """PARTE 4: Demostración de Protocol (Duck Typing)"""
        print("\n--- Probando Exportar Todo (Protocol) ---")
        mi_plano = PlanoCAD("Planta Baja", "1:50")

        # arma lista de exportables (objetos que no son familia, pero cumplen el contrato)
        elementos_mezclados = [c, mi_plano] # 'c' es el cuadrado que ya tiene

        print("\n--- Exportando Elementos ---")
        resultados = exportar_todo(elementos_mezclados)
        for res in resultados:
            print(res)