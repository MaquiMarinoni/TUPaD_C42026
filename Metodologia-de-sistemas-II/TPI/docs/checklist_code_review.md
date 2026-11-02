# Revisión técnica del sistema refactorizado

## Contexto

Versión de código revisada: bd6edac, etiqueta estadorefactorizado.
Evidencia automatizada: c12c376, etiqueta etapa-pruebas.

Revisora: Macarena Marinoni.
Modalidad: autorrevisión guiada con asistencia de ChatGPT.
Fecha: completar con la fecha efectiva de revisión.

Esta revisión no se presenta como una revisión independiente realizada
por otra integrante. La participación de Marianela Valletto se registrará
cuando efectivamente revise o contribuya al trabajo.

## Checklist aplicado

- [x] La interacción por consola se encuentra en Consola.
- [x] El servicio no utiliza input, print ni json.dump.
- [x] El servicio confirma los datos en memoria después del guardado.
- [x] Las reglas de transición están en Solicitud.
- [x] La persistencia JSON utiliza un archivo temporal.
- [x] La consola utiliza DatosNuevaSolicitud para registrar.
- [x] Las 14 pruebas originales se conservan sin modificaciones.
- [x] Las 20 pruebas automatizadas finalizaron correctamente.
- [x] El recorrido manual final permitió consultar, registrar,
      asignar, cambiar estado, filtrar y generar el reporte.
- [x] Los diagramas se visualizaron y se conservaron como imágenes.

## Observaciones y decisiones

### CR01 — Duplicación de persistencia

Hallazgo relacionado: D02.

La versión inicial repetía el procedimiento de guardado en tres
operaciones. La versión refactorizada concentra la escritura en
RepositorioJSON.guardar y la confirmación en memoria en
SistemaAcademico._guardar_datos.

Criterio de aceptación: no repetir la escritura del JSON en las
operaciones y conservar los datos anteriores ante un fallo de guardado.

Evidencia: código de ambos métodos y pruebas de fallo de persistencia.

Estado: corregido y verificado en los escenarios evaluados.

### CR02 — Responsabilidades y reglas del dominio

Hallazgos relacionados: D01, D04 y D08.

La consola se separó del servicio y las reglas de transición se
trasladaron a Solicitud. El menú delega sus opciones en métodos
de interacción específicos.

Criterio de aceptación: el servicio no debe leer entradas de consola
ni presentar resultados, y las reglas de transición deben poder
probarse sin archivos.

Evidencia: consola.py, servicio.py, dominio.py y pruebas de la entidad.

Estado: corregido y verificado en los escenarios evaluados.

### CR03 — Dependencia predeterminada del repositorio JSON

Hallazgo relacionado: D03.

El servicio permite recibir un repositorio, pero conserva la construcción
de RepositorioJSON cuando no se proporciona uno. La dependencia concreta
se redujo, aunque no se eliminó completamente.

Decisión: conservar esta alternativa por compatibilidad. El punto de
entrada proporciona explícitamente el repositorio y las pruebas verifican
la sustitución por memoria.

Criterio de aceptación: las operaciones deben funcionar con ambos
repositorios en los escenarios definidos.

Estado: aceptado con limitación documentada.

### CR04 — Valores del dominio en los mensajes del menú

Hallazgo relacionado: D06.

Las validaciones y el reporte utilizan constantes centralizadas.
Los mensajes informativos de la consola todavía repiten los nombres
de tipos, estados y prioridades.

Decisión: se mantiene como mejora pendiente. Los textos actuales
coinciden con los valores admitidos.

Propuesta futura: generar los mensajes a partir de las constantes
para evitar desactualizaciones.

Estado: mejora parcial; pendiente no bloqueante para el alcance actual.

### CR05 — Validación del archivo de datos

Hallazgo relacionado: D07.

La carga comprueba el objeto principal y las tres listas, pero no valida
todos los campos de cada registro. Un archivo alterado externamente
podría provocar errores que no están contemplados por esas validaciones.

Decisión: documentar el límite y utilizar archivos generados por el
programa. La validación completa se considera una mejora funcional
posterior y no un resultado ya implementado.

Criterio de aceptación del alcance actual: recuperar correctamente
los archivos producidos por ambas versiones y conservar el archivo
original ante un JSON sintácticamente corrupto.

Estado: limitación documentada; no se afirma tolerancia a cualquier
archivo modificado externamente.

## Resultado de la revisión

Se acepta la versión refactorizada para el alcance local y los
escenarios comprobados. Las pruebas automatizadas y el recorrido
manual respaldan el comportamiento evaluado.

La aceptación técnica no equivale a la entrega completa del TPI:
todavía deben cerrarse el informe, los anexos, la participación
de las integrantes, la publicación del repositorio y el video.