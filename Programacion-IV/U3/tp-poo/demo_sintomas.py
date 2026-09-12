"""
demo_sintomas.py
Demostración del síntoma: Argumentos por defecto mutables en Poligono (ANTES del arreglo)

Si ejecuto el código original con lados=[] y observaciones=[], ocurriría esto:

from parte1_diagnostico import Poligono

# se crean dos polígonos sin pasarles la lista de observaciones
p1 = Poligono("P1", "rojo")
p2 = Poligono("P2", "azul")

p1.agregar_observacion("El vértice A está roto")

print(p2._observaciones)  # Salida: ['El vértice A está roto']
print(p1._observaciones is p2._observaciones)  # Salida: True
"""

"""
Demostración del Síntoma 2: Falta de copia defensiva en getLados() (ANTES del arreglo)

from parte1_diagnostico import Cuadrado, Lado

c = Cuadrado("Cuadrado", "azul", [Lado(2), Lado(2), Lado(2), Lado(2)])

# El cliente pide los lados y le agrega uno nuevo
lados_expuestos = c.getLados()
lados_expuestos.append(Lado(99))

# El cuadrado original fue mutado y ahora tiene 5 lados
print(len(c._lados))  # Salida: 5
"""