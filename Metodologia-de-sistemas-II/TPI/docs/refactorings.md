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