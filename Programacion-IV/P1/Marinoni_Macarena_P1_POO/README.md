# Evaluación Parcial 1: Programación IV (POO Avanzada)
**Estudiante:** Macarena Marinoni   
**Fecha:** 16/09/2026  


## 1. Introducción
El presente proyecto implementa el núcleo del catálogo en memoria para el comercio **Food Store**. 
Food Store es un comercio que necesita informatizar su catálogo. Vende productos por pieza (una botella, un paquete), productos por peso (fiambres, verdura) y combos que agrupan productos ya existentes con un descuento. Cada producto se clasifica en una o más categorías (Bebidas, Gaseosas, Fiambrería) y una de esas clasificaciones es la principal: la que determina dónde aparece el producto en el menú.
El sistema de caja del local ya existe y lo provee un tercero. Ese sistema genera sus propias fichas de punto de venta y no se puede modificar, pero el catálogo debe poder exportarse en una sola operación incluyendo tanto los productos propios como esas fichas externas.


## 2. Decisiones de Diseño y Fundamentación Técnica

### 2.1 Encapsulamiento y Manejo de Estado (Requerimiento 1)
* **Convención de Atributos Internos:** Se empleó guion bajo simple (`_nombre`, `_precio_base`, etc.) en lugar de doble guion bajo (`__`). En Python, el doble guion bajo activa el mecanismo de *name mangling*, pensado principalmente para evitar colisiones de identificadores en jerarquías profundas de herencia, y no como un modificador de acceso de seguridad. El uso de guion bajo simple comunica formalmente privacidad y encapsulamiento protegiendo la legibilidad y la extensibilidad del código.
* **Inmutabilidad y Value Objects:** La clase `UnidadMedida` fue definida como `@dataclass(frozen=True)`, garantizando que instancias de unidades físicas (`kg`, `g`, `L`, `u`) permanezcan inmutables en tiempo de ejecución.
* **Exposición Restringida de Atributos:** No se definieron *setters* públicos indiscriminados. La mutación de estado se canaliza mediante métodos de dominio con semántica explícita (`habilitar()`, `deshabilitar()`, `clasificar_en()`). Propiedades como `disponible` o `precio_publicado` se calculan dinámicamente, asegurando que el estado derivado sea siempre consistente.
* **Manejo de Errores:** Se implementó una jerarquía de excepciones de dominio (`ErrorCatalogo` y `ErrorValidacionCatalogo`) que extienden de `ValueError`, asegurando compatibilidad con el manejo estándar de excepciones de Python.


### 2.2 Relaciones Estructurales: Composición vs. Agregación (Requerimiento 2)
* **Composición en `ProductoCategoria`:** La relación entre `Producto` y `ProductoCategoria` es una composición estricta ($1 \rightarrow 1..*$). El vínculo de clasificación no tiene sentido ontológico ni existencia fuera del producto que lo contiene: el ciclo de vida del vínculo está atado indisolublemente a la vida del producto. Además, el método de alternancia `_marcar_principal()` se configuró como protegido para que únicamente el `Producto` dueño pueda coordinar el invariante de que exista **exactamente una categoría principal** en todo momento.
* **Agregación en `ProductoCombo`:** A diferencia de las clasificaciones, los componentes de un combo son productos independientes que existen con anterioridad en el catálogo. Si el combo se da de baja, los productos individuales conservan su ciclo de vida y stock intactos. Por ello, se implementó como agregación ($1 \overset{\circ}{--} 2..*$), validando defensivamente en la construcción la presencia de al menos dos componentes y retornando colecciones protegidas como tuplas (`tuple`).


### 2.3 Resolución del Dilema de Diseño: `ProductoDestacado` (Requerimiento 3)
En el diagrama de partida, `ProductoDestacado` figuraba heredando directamente de `Producto`. Dicha estructura presenta graves fallas de diseño:
1. **Falsa relación «es-un» y rol transitorio:** Estar destacado en vidriera no define la naturaleza intrínseca de un producto, sino un **rol de exhibición temporal**.
2. **Explosión combinatoria:** Si se resolviera por herencia de clases, para destacar un producto por peso o un combo se requeriría crear `ProductoPorPesoDestacado`, `ProductoComboDestacado`, etc., violando el principio abierto/cerrado (OCP).
3. **Rigidez dinámica:** Un producto común no podría comenzar a destacarse o dejar de destacarse en runtime sin destruir y reconstruir el objeto.

**Solución adoptada:** Se implementó el patrón **Envoltorio por Composición (Decorator)**. `ProductoDestacado` contiene una referencia a un `Producto` (`_producto: Producto`) y añade el atributo `_orden_vidriera`. La clase delega transparentemente los métodos del dominio (`nombre`, `precio_final()`, `precio_publicado`) al producto interno y especializa el método `exportar()`.


### 2.4 Contrato Estructural con `Protocol` vs. `ABC` (Requerimiento 4)
Para la exportación polimórfica del catálogo se utilizó `typing.Protocol` en lugar de una clase abstracta tradicional (`abc.ABC`):
* **Tipado Estructural (*Duck Typing* Estático):** La clase provista `FichaPuntoDeVenta` proviene de un módulo externo (`libreria_externa.py`) cerrado a modificación. Si hubiésemos utilizado una clase abstracta `ABC`, habría sido obligatorio modificar `FichaPuntoDeVenta` para que herede nominalmente de ella (`class FichaPuntoDeVenta(Exportable)`), violando las restricciones del examen.
* Al declarar `Exportable` como `Protocol`, cualquier clase que exponga la firma `exportar(self) -> str` cumple automáticamente el contrato sin acoplamiento de herencia, permitiendo que la función `exportar_catalogo(elementos: list[Exportable])` procese productos y fichas externas de manera transparente.


## 3. Instrucciones de Ejecución

1. **Requisitos:** Python 3.12 o superior.
2. **Ejecución del Catálogo y Pruebas:**
   Situarse en el directorio raíz del proyecto y ejecutar:
   ```bash
   python main.py