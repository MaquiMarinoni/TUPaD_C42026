<div align="center">

## Unidad 03 - Practica 2
# Testing Práctico y Contratos

<br><br><br>

**Comisión 15**  
**Marinoni, Macarena** &lt;marinonimacarena@gmail.com&gt;  
Tecnicatura Universitaria en Programación - Universidad Tecnológica Nacional  
Metodología de Sistemas II  
Profesor: Videla, Flavia  
Tutor: Lobos, Diego  
30/09/2026  

</div>

<div style="page-break-after: always;"></div>

<div style="page-break-after: always;"></div>

## ÍNDICE
- [1. Implementación del Patrón AAA](#1-implementación-del-patrón-aaa)
- [2. Diseño de Dobles de Prueba (Stubs y Mocks)](#2-diseño-de-dobles-de-prueba-stubs-y-mocks)
- [3. Análisis de Cobertura](#3-análisis-de-cobertura)

<div style="page-break-after: always;"></div>

## 1. Implementación del patrón AAA

Para garantizar la calidad interna de nuestro software, es fundamental contar con pruebas automatizadas que aseguren la testabilidad y el bajo acoplamiento de los componentes. Omitir la escritura de tests es un "atajo" que genera deuda técnica inmediata, incrementando la fragilidad del sistema y los costos de mantenimiento a futuro. Adicionalmente, contar con una suite de pruebas es la regla fundamental para aplicar técnicas de refactoring seguro sin alterar el comportamiento del sistema.

A continuación, se presenta una función lógica para calcular precios y su correspondiente prueba unitaria estructurada bajo el patrón AAA (Arrange, Act, Assert).

```python
# Función lógica del dominio
def calcular_precio_final(precio_base, descuento):
    if descuento < 0 or descuento > 100:
        raise ValueError("El descuento debe estar entre 0 y 100")
    return precio_base - (precio_base * (descuento / 100))

# Suite de pruebas unitarias
def test_calcular_precio_final_exitoso():
    # 1. ARRANGE 
    # Establece el estado inicial y los parámetros requeridos.
    precio = 1000.0
    descuento_aplicado = 20.0
    resultado_esperado = 800.0

    # 2. ACT 
    # Ejecuta la función especifica que queremos validar.
    resultado_obtenido = calcular_precio_final(precio, descuento_aplicado)

    # 3. ASSERT
    # Valida que el comportamiento observado coincida con el esperado.
    assert resultado_obtenido == resultado_esperado, "El cálculo del precio final es incorrecto"
```

## 2. Diseño de dobles de prueba (Stubs y Mocks)

Para garantizar el aislamiento atómico absoluto del componente bajo examen frente a dependencias de infraestructura (como una API de pagos externa) y evitar pruebas de integración inestables, la ingeniería de software recurre al diseño de Dobles de Prueba (Test Doubles). La elección entre un Stub y un Mock depende estrictamente del objetivo de la validación:

*   **Stub (Simuladores de estado e inyección de datos indirectos):** Es un objeto simulado de estructura estática que proporciona respuestas preconfiguradas o "enlatadas" ante las llamadas del componente bajo prueba. 
    *   *Justificación según arquitectura:* Es necesario implementarlo cuando la dependencia actúa como proveedora de información. Su propósito es simular estados de la infraestructura (ej. inyectar un estado de "fondos insuficientes" desde la API) para evaluar de forma indirecta cómo reacciona la lógica interna, sin interactuar físicamente con la red.
*   **Mock (Verificadores de comportamiento y auditoría de interacciones):** Es un doble de prueba dinámico diseñado específicamente para auditar e inspeccionar el comportamiento y el protocolo de interacción del componente. 
    *   *Justificación según arquitectura:* Es indispensable cuando se necesita validar las reglas de comunicación hacia el exterior. El Mock registra activamente qué métodos invocó el componente y con qué parámetros exactos (ej. auditar que la orden de cobro a la API se envió una sola vez y con el monto correcto). La aseveración final interroga al Mock para certificar el protocolo, no el estado.

## 3. Análisis de cobertura

En el laboratorio profesional de software, la medición de la cobertura del código es vital para asegurar la calidad interna. Sin embargo, existe una diferencia crítica en el rigor de las métricas empleadas:

*   **Statement coverage (Cobertura de sentencias o líneas):** Esta métrica calcula la proporción matemática entre el número de líneas de código fuente ejecutables que fueron recorridas al menos una vez por alguna prueba y el total de líneas del proyecto. Asumir que un alto porcentaje de sentencias garantiza la ausencia de bugs es un error metodológico, ya que una línea puede ejecutarse de forma exitosa con un dato específico pero fallar catastróficamente ante un caso de borde no contemplado por la suite de pruebas.
*   **Branch coverage (Cobertura de ramas o caminos condicionales):** Representa un criterio de control significativamente más riguroso y seguro para el laboratorio. Esta métrica no evalúa líneas físicas, sino que analiza todos los caminos condicionales y bifurcaciones lógicas posibles dentro de las estructuras de control del software (como sentencias *if*, *else* o bloques *switch*).

### Diseño de casos de prueba

A continuación, se presenta una función con una estructura condicional compleja que calcula el descuento de un cliente, seguida de los casos de prueba necesarios para recorrer exhaustivamente todas sus ramas lógicas.

```python
# Funcion con estructura condicional compleja
def calcular_descuento(cliente_es_vip, monto_compra):
    if cliente_es_vip and monto_compra >= 10000:
        # Rama 1: Cumple ambas condiciones máximas
        return monto_compra * 0.70  
    elif cliente_es_vip or monto_compra >= 10000:
        # Rama 2: Cumple al menos una de las dos condiciones
        return monto_compra * 0.85  
    else:
        # Rama 3: No cumple ninguna condición
        return monto_compra         

# ==========================================
# SUITE DE PRUEBAS (Branch Coverage 100%)
# ==========================================

def test_descuento_rama_1_vip_y_alto_monto():
    # Cubre el 'if' principal (Ambas condiciones Verdaderas)
    assert calcular_descuento(True, 15000) == 10500.0

def test_descuento_rama_2_solo_vip():
    # Cubre el 'elif' siendo VIP pero con monto bajo
    assert calcular_descuento(True, 5000) == 4250.0

def test_descuento_rama_2_solo_alto_monto():
    # Cubre el 'elif' por monto alto sin ser VIP
    assert calcular_descuento(False, 12000) == 10200.0

def test_descuento_rama_3_ninguna_condicion():
    # Cubre el 'else' (Ninguna condición se cumple)
    assert calcular_descuento(False, 3000) == 3000.0    