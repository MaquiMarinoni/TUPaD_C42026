# Sistema de Gestión de Solicitudes Académicas

Trabajo Práctico Integrador de Metodología de Sistemas II.
Comisión 15. Integrantes: Macarena Marinoni y Marianela Valletto.

## Descripción

El programa permite registrar solicitudes de estudiantes, clasificarlas
por tipo y prioridad, asignar responsables, cambiar estados, consultar
registros y generar un reporte por estado y prioridad.

El prototipo funciona por consola, utiliza datos ficticios y guarda
la información en JSON. No implementa autenticación ni uso concurrente.

## Requisitos

- Python 3.10 o posterior.
- Git para consultar el historial y sus etiquetas.
- No requiere instalar paquetes externos.

## Ejecución

Abrir una terminal en la carpeta TPI y ejecutar:

```powershell
python src/main.py
```

Los tipos admitidos son Certificado, Inscripción y Consulta.
Las prioridades son Baja, Media y Alta. Deben escribirse tal como
aparecen en el menú.

Los estudiantes precargados son E001 y E002.
Los responsables precargados son R001 y R002.

El archivo de persistencia se encuentra en datos/solicitudes.json.
Si no existe, se utilizan los catálogos iniciales y se crea al guardar
la primera operación válida.

Pruebas
Desde la carpeta TPI:
python -m unittest discover -s tests -v

Las pruebas utilizan archivos temporales o un repositorio en memoria.
No modifican los datos de la demostración.
Organización
- src/main.py: punto de entrada y composición de componentes.
- src/consola.py: menú e interacción con el usuario.
- src/servicio.py: coordinación de operaciones.
- src/dominio.py: entidades, datos de entrada y reglas de transición.
- src/repositorio.py: lectura y escritura en JSON.
- tests: pruebas iniciales y pruebas del diseño refactorizado.
- docs: diagnóstico, refactorings y evidencias.
- datos: información sintética de demostración.
Versiones
- estado-inicial: sistema base y evidencias manuales.
- etapa-diagnostico: diagnóstico y pruebas iniciales.
- etapa-refactoring: reorganización del código.
- estadorefactorizado: versión refactorizada.
- etapa-pruebas: evidencia automatizada de la versión refactorizada.
- etapa-docs: se incorporará al cerrar la documentación.
La etiqueta estado-inicial precede a la incorporación de las pruebas.
Las 14 pruebas iniciales están disponibles desde etapa-diagnostico.
Alcance y límites
Los estados Resuelta y Cancelada son terminales.
Para iniciar la atención debe existir un responsable asignado.

El reemplazo mediante archivo temporal reduce el riesgo de dejar
el archivo de destino parcialmente escrito, pero no constituye un
mecanismo de concurrencia ni una garantía de durabilidad ante fallos
de hardware.

La validación del archivo controla la estructura principal. No se
implementa una validación completa de cada registro editado externamente.
Asistencia de IA
Se utilizó ChatGPT como apoyo para la planificación, documentación,
propuestas de código, refactoring y pruebas. Se utilizó además un script
de transformación para separar componentes y generar documentación.

Las integrantes deben revisar y comprender las decisiones y conservar
los intercambios relevantes como parte de los anexos solicitados.
