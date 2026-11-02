# Registro de refactorings

## R01 — Extract Method para centralizar el guardado

### Problema identificado

El hallazgo D02 del diagnóstico inicial señala que los métodos
registrar, asignar y cambiar_estado repetían el procedimiento
de escritura del archivo JSON.

### Cambio realizado

Se extrajo ese procedimiento al método _guardar_datos(nuevos_datos).
Las tres operaciones ahora llaman al mismo método.

El guardado conserva el orden original:
1. Crear la carpeta de datos si es necesario.
2. Escribir el contenido en un archivo temporal.
3. Reemplazar el archivo de destino.
4. Actualizar los datos en memoria después del guardado exitoso.

### Justificación

La extracción elimina la duplicación y permite modificar el
procedimiento de persistencia en un único lugar, aplicando DRY.

Este cambio todavía no separa la persistencia de SistemaAcademico
ni elimina su dependencia directa del sistema de archivos.

### Verificación

Comando ejecutado:

python -m unittest discover -s tests -v

Resultado: 14 pruebas ejecutadas, todas aprobadas.

La prueba test_14_conservar_datos_si_falla_el_guardado verifica
que un fallo al reemplazar el archivo conserve los datos anteriores
en memoria y en el archivo original.

Los resultados respaldan la conservación del comportamiento
en los escenarios evaluados; no garantizan ausencia de otros defectos.

### Trazabilidad

El cambio y este registro se conservarán en el commit:
TPI MSII: extraer metodo de guardado sin cambiar comportamiento

R02 — Extract Class para separar la persistencia
Se trasladaron la lectura y escritura de JSON a RepositorioJSON.
SistemaAcademico delega el guardado y confirma sus datos en memoria
únicamente después de que el repositorio termina correctamente.

Atiende los hallazgos D01 y D03 y completa la centralización de D02.
R03 — Introduce Parameter Object
Se incorporó DatosNuevaSolicitud para agrupar estudiante, descripción,
tipo y prioridad. La consola utiliza registrar_datos(datos).

Se conserva registrar(estudiante_id, descripcion, tipo, prioridad)
como adaptador de compatibilidad para las pruebas originales. La lógica
del registro tiene una única implementación en registrar_datos.
R04 — Move Method hacia la entidad Solicitud
La validación y aplicación de transiciones se trasladó a
Solicitud.cambiar_estado. La asignación se expresa mediante
Solicitud.asignar_responsable.

Las operaciones devuelven nuevas entidades; no modifican la anterior.
El servicio guarda el nuevo estado antes de confirmarlo en memoria.

Atiende D07 y D08. La conversión entre entidad y diccionario conserva
el formato JSON generado por la versión inicial.
R05 — Extract Method para búsquedas y actualizaciones
Se centralizó la búsqueda por identificador en _buscar_solicitud.
La sustitución de un registro se agrupó en _actualizar_solicitud.

Atiende D05 y evita repetir el procedimiento de actualización.
R06 — Separación de consola y servicio
El menú se trasladó a Consola. Cada opción delega en un método de
interacción y el servicio ya no contiene input ni print.

El punto de entrada main.py construye el repositorio, el servicio
y la consola. Atiende D01 y D04.
R07 — Centralización de valores del dominio
Los estados, prioridades, tipos y transiciones se definieron en
dominio.py. Las validaciones y el reporte utilizan esas definiciones.

Los textos informativos del menú se conservan para mantener la
interacción original. Sigue existiendo esa repetición de presentación,
que podrá eliminarse en una mejora posterior. Atiende parcialmente D06.
SOLID y alcance de la separación
SRP: consola, coordinación, dominio y persistencia poseen
responsabilidades diferenciadas.

OCP y DIP: el servicio admite repositorios sustituibles a través de
cargar y guardar. El punto de entrada proporciona la implementación JSON.
Se conserva una construcción JSON predeterminada por compatibilidad;
no se presenta como independencia absoluta de esa clase concreta.

ISP: el contrato utilizado por el servicio requiere solamente cargar
y guardar. Se expresa por comportamiento compatible, sin una jerarquía
abstracta adicional.

Sustituibilidad: las pruebas adicionales comparan el contrato y un
recorrido del servicio con JSON y memoria. Esto respalda los escenarios
evaluados y no demuestra equivalencia para cualquier implementación.
Verificación
Las 14 pruebas iniciales se mantienen sin modificaciones.
Se agregan 6 pruebas sobre el objeto de parámetros, el dominio,
la cancelación y la sustitución del repositorio.

La salida de ejecución, el intérprete y la fecha se conservan en
pruebas_estado_refactorizado.txt. El resultado solo se considera
aprobado cuando el proceso finaliza sin errores.
