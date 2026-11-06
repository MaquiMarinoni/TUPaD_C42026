# Diagnóstico de la versión inicial

## Versión analizada

- Commit: `c94ebfa`.
- Etiqueta: `estado-inicial`.
- Archivo: `src/main.py`.
- Sistema: Gestión de Solicitudes Académicas.

> Este documento registra el diagnóstico previo al refactoring. Las mejoras se expresan como propuestas porque describen el plan definido sobre la versión inicial. Su implementación final se encuentra documentada en `refactorings.md`.

## Introducción

El sistema base permite registrar solicitudes, asignar responsables,
cambiar estados, consultar información y generar un reporte. Durante
el recorrido manual se comprobó el registro de una solicitud, el rechazo
del inicio de atención sin responsable, la asignación, los cambios de
estado, el bloqueo de reapertura de una solicitud resuelta y la
recuperación de los datos después de reiniciar.

Estos resultados corresponden a los escenarios ejecutados y no
demuestran que todos los casos posibles estén cubiertos. El diagnóstico
siguiente analiza la estructura interna y las oportunidades de mejora.

## D01 — Concentración de responsabilidades

**Ubicación:** clase `SistemaAcademico`.

**Evidencia:** la misma clase contiene la carga del archivo en
`__init__`, las operaciones `registrar`, `asignar` y `cambiar_estado`,
la consulta, el reporte y el menú de consola en `ejecutar`.

**Impacto:** cambios de interfaz, almacenamiento y reglas de negocio
afectan una misma clase.

**Riesgo de mantenimiento:** aumenta la cantidad de motivos por los
que debe modificarse y dificulta revisar los cambios de forma aislada.

**Prioridad:** alta.

**Mejora propuesta:** separar la interfaz de consola, el servicio de
solicitudes y el repositorio de datos, aplicando SRP.

## D02 — Duplicación del procedimiento de guardado

**Ubicación:** métodos `registrar`, `asignar` y `cambiar_estado`.

**Evidencia:** los tres repiten la creación de la carpeta, la escritura
del archivo temporal, la serialización JSON, el reemplazo del archivo
y la actualización de `self.datos`.

```python
self.archivo.parent.mkdir(parents=True, exist_ok=True)
temporal = self.archivo.with_suffix(".tmp")

with temporal.open("w", encoding="utf-8") as archivo:
    json.dump(nuevos_datos, archivo, ensure_ascii=False, indent=4)

temporal.replace(self.archivo)
self.datos = nuevos_datos
```

**Impacto:** una modificación del guardado debe replicarse en tres lugares.

**Riesgo de mantenimiento:** una corrección aplicada solo en uno de los
métodos puede producir comportamientos diferentes entre operaciones.

**Prioridad:** alta.

**Mejora propuesta:** extraer y centralizar el procedimiento de
persistencia, conservando la confirmación en memoria después de
guardar correctamente.

## D03 — Dependencia directa del almacenamiento en archivo

**Ubicación:** `__init__`, `registrar`, `asignar` y `cambiar_estado`.

**Evidencia:** las operaciones utilizan directamente `Path`, `open`,
`json.dump` y `replace`.

**Impacto:** para probar una operación de negocio se necesita gestionar
un archivo o intervenir sus llamadas al sistema de archivos.

**Riesgo de mantenimiento:** cambiar el mecanismo de persistencia obliga
a modificar métodos que también contienen reglas del dominio.

**Prioridad:** alta.

**Mejora propuesta:** recibir un repositorio por constructor. El servicio
dependerá de un contrato pequeño y las pruebas podrán utilizar una
implementación en memoria.

## D04 — Método de interacción extenso

**Ubicación:** método `ejecutar`.

**Evidencia:** contiene el bucle del menú, siete alternativas, lectura
y conversión de entradas, llamadas a operaciones, presentación de
resultados y manejo de errores.

**Impacto:** comprender o modificar una opción requiere recorrer un
método que también contiene todas las demás.

**Riesgo de mantenimiento:** facilita mezclar cambios de distintas
opciones y dificulta probar cada interacción por separado.

**Prioridad:** media.

**Mejora propuesta:** extraer funciones para registrar, asignar, cambiar
estado, consultar y mostrar reportes. El bucle principal quedará a cargo
de seleccionar la operación.

## D05 — Búsqueda duplicada de solicitudes

**Ubicación:** métodos `asignar` y `cambiar_estado`.

**Evidencia:** ambos localizan la solicitud con la misma expresión y
repiten la validación de inexistencia.

```python
solicitud = next(
    (
        s
        for s in self.datos["solicitudes"]
        if s["id"] == solicitud_id
    ),
    None,
)

if solicitud is None:
    raise ValueError("La solicitud no existe.")
```

**Impacto:** el criterio de búsqueda y su error asociado quedan
distribuidos en varios métodos.

**Riesgo de mantenimiento:** futuras modificaciones pueden dejar
mensajes o criterios de búsqueda inconsistentes.

**Prioridad:** media.

**Mejora propuesta:** extraer una operación común de búsqueda por ID
que devuelva la solicitud o informe su inexistencia.

## D06 — Valores del dominio dispersos

**Ubicación:** `registrar`, `asignar`, `cambiar_estado`, `reporte`
y `ejecutar`.

**Evidencia:** estados como `"Pendiente"` y `"Resuelta"` aparecen en
validaciones, condiciones, mensajes y agrupaciones. Los tipos y
prioridades también se repiten entre validaciones y consola.

**Impacto:** no existe una única definición de los valores admitidos.

**Riesgo de mantenimiento:** un error de tipeo o una actualización
incompleta puede generar diferencias entre registro, consulta y reporte.

**Prioridad:** media.

**Mejora propuesta:** centralizar estados, tipos y prioridades mediante
constantes o enumeraciones, conservando los textos almacenados en JSON.

## D07 — Representación de solicitudes mediante diccionarios sin contrato explícito

**Ubicación:** creación del diccionario `solicitud` en `registrar`
y acceso a sus campos en los demás métodos.

**Evidencia:** se utilizan claves de texto como `"estado"`,
`"responsable_id"` y `"estudiante_id"` en distintos puntos del programa.

**Impacto:** la estructura esperada de una solicitud depende de
convenciones que cada método debe conocer.

**Riesgo de mantenimiento:** omitir o escribir incorrectamente una clave
puede provocar errores durante la ejecución. La validación de carga
comprueba las listas principales, pero no todos los campos internos.

**Prioridad:** alta.

**Mejora propuesta:** representar la solicitud mediante una entidad
explícita y definir su conversión a JSON. Cualquier nueva validación
de archivos malformados se registrará como mejora funcional separada
del refactoring.

## D08 — Reglas de transición concentradas en el gestor

**Ubicación:** método `cambiar_estado`.

**Evidencia:** el método interpreta el estado actual, decide los destinos
permitidos y comprueba el responsable mediante condicionales anidados.

```python
if estado_actual == "Pendiente":
    if nuevo_estado not in ("En atención", "Cancelada"):
        raise ValueError("La transición de estado no está permitida.")
elif estado_actual == "En atención":
    if nuevo_estado not in ("Resuelta", "Cancelada"):
        raise ValueError("La transición de estado no está permitida.")
else:
    raise ValueError("La solicitud ya está finalizada.")
```

**Impacto:** las reglas del ciclo de vida de una solicitud se encuentran
en la misma clase que coordina operaciones y almacenamiento.

**Riesgo de mantenimiento:** incorporar o revisar una transición exige
intervenir ese método y comprobar todas sus ramas.

**Prioridad:** media.

**Mejora propuesta:** trasladar el comportamiento de transición a la
entidad Solicitud y expresar las transiciones permitidas de forma
centralizada, manteniendo las reglas actuales.

## Oportunidad adicional — Agrupación de datos de registro

**Ubicación:** firma de `registrar`.

```python
registrar(self, estudiante_id, descripcion, tipo, prioridad)
```

Los cuatro argumentos pertenecen a una misma operación y tres son
textos que podrían intercambiarse por error. La cantidad de parámetros
no constituye por sí sola un defecto, pero agruparlos en
`DatosNuevaSolicitud` permitiría explicitar el contrato de entrada.

Se propone aplicar Introduce Parameter Object y verificar que se
mantengan los mismos campos, validaciones y resultados.

## Priorización y alcance de las mejoras

Primero se centralizará la persistencia y se establecerán límites entre
las responsabilidades. Luego se incorporará la representación explícita
de la solicitud, se reorganizarán las reglas de transición y se
simplificará la interfaz.

D01 describe el problema general de responsabilidades; D02 y D03
identifican aspectos concretos de duplicación y dependencia. Aunque
están relacionados, deberán verificarse por separado: centralizar el
guardado no elimina automáticamente su acoplamiento con el negocio.

Cada refactoring se relacionará con los hallazgos que atiende y con
pruebas del comportamiento previo. No se considerará mejorado un
aspecto únicamente por agregar clases o reducir líneas de código.