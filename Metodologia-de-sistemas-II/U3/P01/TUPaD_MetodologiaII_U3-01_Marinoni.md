<div align="center">

## Unidad 03 - Practica 1
# Gobernanza y Definición de Terminado (DoD)

<br><br><br>

**Comisión 15**  
**Marinoni, Macarena** &lt;marinonimacarena@gmail.com&gt;  
Tecnicatura Universitaria en Programación - Universidad Tecnológica Nacional  
Metodología de Sistemas II  
Profesor: Videla, Flavia  
Tutor: Lobos, Diego  
29/09/2026  

</div>

<div style="page-break-after: always;"></div>

## Indice
- [Gobernanza y Definición de Terminado (DoD)](#gobernanza-y-definición-de-terminado-dod)
  - [Indice](#indice)
  - [Introducción](#introducción)
  - [Desarrollo](#desarrollo)
    - [1. Definition of Done (DoD) - Criterios de Aceptación Técnica (TAC)](#1-definition-of-done-dod---criterios-de-aceptación-técnica-tac)
    - [2. Configuración de Trazabilidad (Issue Template)](#2-configuración-de-trazabilidad-issue-template)
    - [3. Matriz de Categorización (Labels)](#3-matriz-de-categorización-labels)

<div style="page-break-after: always;"></div>

## Introducción
El presente informe establece los lineamientos de gobernanza y control de calidad para el repositorio del equipo de desarrollo, con el objetivo de garantizar un desarrollo profesional y sostenible. La ausencia de estándares claros al momento de integrar código fomenta la acumulación de "deuda técnica", la cual representa el costo futuro que se pagará por tomar atajos en el presente. Para evitar que el costo del cambio crezca exponencialmente a lo largo del ciclo de vida del software, es imperativo resguardar su "calidad interna", asegurando que el sistema sea fácil de entender, modificar y extender. En este marco, se definen a continuación los Criterios de Aceptación Técnica (TAC), una plantilla de incidencias estructurada para erradicar la ambigüedad y una matriz de categorización de tareas.

## Desarrollo

### 1. Definition of Done (DoD) - Criterios de Aceptación Técnica (TAC)
Para asegurar la calidad interna del producto y evitar la acumulación de deuda técnica, todo incremento de software debe cumplir obligatoriamente con los siguientes Criterios de Aceptación Técnica (TAC) antes de ser integrado al proyecto:

* **Integridad de compilación:** El código debe compilar de manera exitosa y pasar todos los tests en el entorno de integración.
* **Validación de pruebas automatizadas:** El incremento debe incluir pruebas (tests unitarios o de integración) que pasen correctamente, garantizando que no se introducen bugs ni se rompen funcionalidades existentes.
* **Umbrales mínimos de cobertura de código:** El código nuevo o modificado debe alcanzar un umbral mínimo de cobertura para su validación técnica.
* **Revisión por pares obligatoria (Code Review):** El Pull Request (PR) debe presentar atomicidad, es decir, resolver una sola cosa para evitar que sea difícil de revisar. Además, debe contar con la revisión y el "Approve" formal enfocado en la lógica, legibilidad y diseño.
* **Gobernanza de estilo (Linting):** El código entregado debe cumplir con la guía de estilo del equipo, respetando los estándares de formateo e indentación.
* **Sustento de la documentación técnica:** En caso de incorporar lógicas complejas o nuevos puntos de acceso, estos deben encontrarse debidamente documentados (por ejemplo, en el README o mediante Swagger).

<div style="page-break-after: always;"></div>

### 2. Configuración de Trazabilidad (Issue Template)
Para garantizar la mantenibilidad del software, entendiéndola como la capacidad del sistema para ser corregido y modificado con el menor esfuerzo posible, es fundamental evitar la desinformación y la ambigüedad en los reportes. Todo reporte de error (bug) o solicitud de nueva funcionalidad (feature) deberá regirse obligatoriamente por la siguiente plantilla en formato Markdown:

**Título:** 
*[Un resumen claro, conciso y técnico del problema o funcionalidad]*

**Descripción técnica del problema:**
*[Explicación detallada del fallo detectado o de la necesidad técnica a resolver. Debe proveer el contexto necesario para que cualquier desarrollador pueda entenderlo sin requerir explicaciones adicionales]*

**Pasos exactos para reproducir el fallo:**
*[Secuencia enumerada para llegar al error]*
1. *Ir a...*
2. *Hacer clic en...*
3. *Ingresar el dato...*

**Comportamiento esperado frente al observado:**
* **Comportamiento Esperado:** *[Qué debería ocurrir según la lógica de negocio si el sistema funcionara correctamente]*
* **Comportamiento Observado:** *[Qué es lo que está ocurriendo actualmente (el fallo)]*

**Evidencias adjuntas:**
*[Espacio para incluir capturas de pantalla, fragmentos de logs de error, o enlaces a la traza del error]*

<div style="page-break-after: always;"></div>

### 3. Matriz de Categorización (Labels)
Para gestionar de forma eficiente el repositorio y auditar de manera rigurosa el cumplimiento de la DoD antes de integrar cualquier código, se implementará el siguiente sistema de etiquetas (Labels). Esta categorización permite mitigar riesgos arquitectónicos y visualizar los "Code Smells" o deuda técnica antes de que su costo de modificación crezca de forma exponencial.

*   **`bug`**: Identifica fallos en el sistema. Estos pueden afectar la calidad externa (lo que percibe el usuario final, como fallos de fiabilidad) o evidenciar problemas de calidad interna que requieren resolución prioritaria. 
*   **`feature`**: Representa el desarrollo de una nueva funcionalidad. Todo incremento de código etiquetado como feature debe cumplir innegociablemente con todos los Criterios de Aceptación Técnica (TAC) y respetar las reglas de bajo acoplamiento para evitar fragilidad en el sistema.
*   **`technical-debt`**: Etiqueta crítica destinada a visibilizar "atajos" tomados durante el desarrollo, tales como código duplicado, falta de refactorización o de cobertura de pruebas. Hace visible el problema para planificar su resolución ("pago de intereses") antes de que el código sufra putrefacción o se vuelva rígido.
*   **`documentation`**: Asignada a tareas que actualizan la arquitectura, manuales o APIs. Su uso garantiza la auditoría del criterio "sustento de la documentación técnica", exigido en la DoD, asegurando que el software pueda entenderse sin depender del conocimiento aislado de un desarrollador.