<div align="center">

## Unidad 04 - Practica 2
# Flujos de trabajo colaborativo

<br><br><br>

**Comisión 15**  
**Marinoni, Macarena** &lt;marinonimacarena@gmail.com&gt;  
Tecnicatura Universitaria en Programación - Universidad Tecnológica Nacional  
Metodología de Sistemas II  
Profesor: Videla, Flavia  
Tutor: Lobos, Diego  
12/10/2026  

</div>

<div style="page-break-after: always;"></div>

## ÍNDICE
  - [Introducción](#introducción)
  - [Parte 1: Estrategias de Branching (Modelos de ramificación)](#parte-1-estrategias-de-branching-modelos-de-ramificación)
  - [Parte 2: Procesos de integración colaborativa](#parte-2-procesos-de-integración-colaborativa)
  - [Parte 3: Estandarización y documentación del proyecto](#parte-3-estandarización-y-documentación-del-proyecto)
  - [Parte 4: Validación de estándares locales](#parte-4-validación-de-estándares-locales)

<div style="page-break-after: always;"></div>

## Introducción

A medida que los equipos de desarrollo escalan, surge el desafío de coordinar el flujo de código para que la velocidad de entrega no comprometa la estabilidad del producto. El presente informe aborda la transición desde el dominio técnico individual hacia la ingeniería de software colaborativa.

### Parte 1: Estrategias de Branching (Modelos de ramificación)

#### 1. Análisis de Modelos: GitFlow vs. Trunk-based Development

| **Factor**                         | **GitFlow**                                                                                                                                              | **Trunk-based Development**                                                                                                                            |
| :--------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Estructura de comunicación         | Jerárquica y estructurada: Los desarrolladores trabajan aislados. La integración a ramas principales requiere un proceso formal de revisión.             | Sincronizada y orgánica: Requiere alineación total. Los desarrolladores integran código a la rama principal de forma ágil y coordinada en tiempo real. |
| Deuda de Integración               | Alta: El aislamiento prolongado de una funcionalidad (*feature*) genera una gran divergencia técnica respecto al código base que evoluciona en paralelo. | Mínima: Al integrar fragmentos pequeños de código múltiples veces al día, se evita la acumulación de divergencias y deuda técnica.                     |
| Complejidad de Fusión (Merge Hell) | Alta: Fusionar una rama tras semanas de aislamiento produce conflictos masivos, entrelazados y sumamente costosos de resolver.                           | Baja: Los conflictos son minúsculos y de fácil resolución inmediata, aunque exige una estricta disciplina de pruebas automatizadas.                    |

#### 2. Caso de Estudio: elección de strategia

Situacion: Una empresa de software médico está desarrollando un sistema crítico que requiere auditorías estrictas y solo lanza actualizaciones cada tres meses. El equipo es grande y jerárquico.

El modelo de ramificación recomendado es GitFlow debido a
*   Alineación con el ciclo de lanzamientos: GitFlow está diseñado específicamente para proyectos con ciclos de entrega programados y espaciados (como las actualizaciones trestrales). Su estructura permite estabilizar el código en una rama dedicada (`release`) para realizar auditorías y pruebas manuales, sin detener el trabajo de los desarrolladores en nuevas funcionalidades que residen en la ram`develo.
*   Control de Calidad y Auditoría: En sistemas críticos de salud, la velocidad de entrega (*time-to-market*) pasa a un segundo plano frente a la fiabilidad y la seguridad. GitFlow proporciona una fuerte "red de seguridad manual. La separación estricta de ramas obliga a que cada incremento pase por un proceso de revisión formal, facilitando la trazabilidad exacta de quién aprobó qué código, un requisito indispensable para las auditorías médicas.
*   Gestión de la Estructura del Equipo: Al tratarse de un equipo grande y jerárquico, la estructura rígida y burocrática de GitFlow se adapta de manera natural a la organizacion. Los desarrolladores base trabajan aislados en ramas de características (*feature branches*) y elevan su código a los líderes técnicos mediante Pull Requests. Esta jerarquización previene el caos de integración y asegura que ningún código inestable escale a producción por accidente.


#### 3. Feature Flags (Interruptores de código)

En equipos que operan bajo modelos de integración diaria a la rama principal (como *Trunk-based Development*), surge el desafío de cómo integrar una funcionalidad que requiere varios días de trabajo continuo sin exponer una experiencia a medias o con errores a los usuarios en producción.
Las Feature Flags resuelven este problema permitiendo que el programador suba el código nuevo pero "apagado". Gracias a esto, el código llega físicamente al servidor de producción y se integra al sistema, pero el usuario final no interactúa con él hasta que el equipo decide cambiar el estado de la bandera a "activo". Esta práctica separa el despliegue del lanzamiento.



### Parte 2: Procesos de integración colaborativa

#### 4. El Pull Request (PR) como herramienta de comunicación

Para que un compañero pueda comprender el alcance, el objetivo y el impacto del cambio sin tener que descifrar inicialmente el código línea por línea, la descripción del PR debe incluir los siguientes elementos indispensables:
*   Contexto y trazabilidad: Debe incluir un enlace directo al requerimiento funcional, historia de usuario o *Issue* que originó el trabajo. Esto responde al *por qué* del cambio y asegura la gobernanza del repositorio.
*   Resumen técnico: Una descripción concisa de *qué* se modificó a nivel estructural y *cómo* se abordó la solución.
*   Instrucciones de verificación: Pasos claros y deterministas para que el revisor pueda levantar el entorno local, reproducir el escenario y probar la funcionalidad manualmente.
*   Evidencias visuales y de calidad: Si el cambio impacta en la interfaz (GUI), es importante incluir capturas de pantalla o videos cortos. Asimismo, debe adjuntar la confirmación o logs de que el código superó las pruebas unitarias y el análisis estático local.

#### 5. La cultura de la code review

El propósito fundamental de una Code Review no es encontrar errores o culpables, sino asegurar colaborativamente que el software sea mantenible, seguro y adherido a los estándares organizacionales.
Esta práctica se fundamenta en dos pilares críticos:
*   Transferencia de Conocimiento (Mentoría): Las revisiones por pares representan el espacio educativo más valioso del flujo de trabajo. Es el momento institucionalizado donde los desarrolladores Junior aprenden mejores prácticas, patrones de diseño y lógica de negocio a partir de la retroalimentación constructiva de los perfiles Senior. Esto previene el aislamiento del conocimiento.
*   Cumplimiento de Principios de Diseño (DRY y SOLID): Mientras que la Integración Continua (CI) certifica que el código compila, el revisor humano audita la calidad del diseño arquitectónico. Durante la revisión se verifica:
    *   DRY: Se inspecciona activamente que el nuevo código no introduzca bloques lógicos redundantes o duplicados, forzando la reutilización y modularidad.
    *   Principios SOLID: Se evalúa, por ejemplo, que las nuevas clases respeten el Principio de Responsabilidad Única (SRP) haciendo solo una cosa, y que el código esté abierto a la extensión pero cerrado a la modificación (OCP). Este filtro humano es la única barrera efectiva contra la acumulación de deuda técnica estructural a largo plazo.

#### 6. Estrategias de merge y el historial

Al finalizar un Pull Request, el equipo debe decidir cómo integrar el trabajo en la rama principal. Esta decisión la legibilidad del repositorio, existiendo tres enfoques principales:
*   Create a Merge Commit (Historial verídico): Esta estrategia respeta la historia tal cual ocurrió. Mantiene intactos todos y cada uno de los commits originales realizados en la rama de funcionalidad, y los une a la rama principal mediante la creación de un nuevo "commit de merge". 
    *   *Impacto en el grafo:* Genera un historial no lineal (con forma de "vías de tren" que se separan y se vuelven a unir). Muestra la verdad absoluta, pero puede volverse visualmente ruidoso y complejo de auditar en equipos grandes.
*   Squash and Merge (Historial limpio): Consiste en condensar todos los micro-commits de la rama de trabajo en un único y bien documentado commit al momento de integrarlo a la rama principal. 
    *   *Impacto en el grafo:* Crea un historial principal inmaculado y modular. Se pierde el detalle cronológico de los pequeños pasos del desarrollador, pero el grafo queda totalmente limpio, donde cada commit en la rama principal equivale a una funcionalidad completa terminada.
*   Rebase and Merge (Historial lineal): Antes de fusionar, toma los commits de la rama de funcionalidad y los "re-aplica" en la punta actual de la rama principal, como si el desarrollador los hubiera escrito directamente allí. 
    *   *Impacto en el grafo:* Evita la creación del commit de merge, generando un historial estrictamente lineal (una línea recta continua). Esto facilita enormemente la lectura secuencial y el uso de herramientas de búsqueda de errores (como `git bisect`), aunque reescribe matemáticamente los hashes originales de la rama.



### Parte 3: Estandarización y documentación del proyecto

#### 7. Guías de contribución (CONTRIBUTING.md)

Como líder de un proyecto de software, es imperativo establecer un "contrato social y técnico" para el equipo, el cual se materializa en la raíz del repositorio a través del archivo `CONTRIBUTING.md`. 
Para que un nuevo desarrollador pueda integrarse de manera autónoma y empezar a codificar siguiendo estrictamente las reglas del equipo, este documento debe proveer la siguiente información:
*   Configuración del Entorno: Instrucciones claras y paso a paso sobre cómo levantar el proyecto localmente, qué dependencias instalar y cómo configurar el entorno de pruebas.
*   Nomenclatura de Ramas (Branching): Las reglas exactas sobre cómo deben crearse y nombrarse las ramas de trabajo (por ejemplo, estandarizando el uso de prefijos como `feature/`, `bugfix/` o `hotfix/`).
*   Reglas de Estilo y Calidad (Linting): Las convenciones de escritura de código que exige el proyecto, especificando qué herramientas de análisis estático se utilizan para validar la sintaxis antes de subir los cambios.
*   Estructura de Commits y Pull Requests: Los estándares de comunicación con el repositorio, exigiendo, por ejemplo, el uso de *Conventional Commits* para los mensajes del historial y detallando los pasos obligatorios para abrir un Pull Request profesional.

#### 8. Architecture Decision Records (ADRs)

Un Architecture Decision Record (ADR) es un documento corto y formal cuya utilidad principal es registrar una decisión técnica importante, detallando explícitamente el contexto en el que se tomó y las consecuencias de dicha elección. 

En el ciclo de vida de proyectos largos, es habitual olvidar los motivos que impulsaron una elección de arquitectura (por ejemplo, por qué se eligió usar una base de datos NoSQL en lugar de una Relacional, o por qué se adoptó cierta librería). Cuando un desarrollador se suma al proyecto un año después, el ADR le resulta vital porque:
*   Aporta contexto histórico: Le permite entender de forma autónoma el trasfondo y el por qué de una decisión técnica, comprendiendo las limitaciones que tenía el equipo en ese momento.
*   Evita regresiones y debates cíclicos: Previene que el nuevo integrante, por falta de contexto, intente revertir un cambio estructural que funciona o que obligue al equipo a reabrir discusiones técnicas sobre temas que ya fueron resueltos en el pasado.

#### 9. Plantillas de trabajo (Templates)

El uso de plantillas para Issues y Pull Requests, implementadas generalmente como archivos Markdown en la configuración del repositorio, aporta beneficios como:
*   Estandarización y anulación de ambigüedades: Las plantillas de *Issues* fuerzan al reportero a completar secciones predefinidas obligatorias (título estructurado, descripción, pasos deterministas para reproducir el fallo, comportamiento esperado frente al observado y evidencias adjuntas). Esto estandariza el ingreso de solicitudes y elimina descripciones vagas que retrasan el diagnóstico.
*   Garantía de completitud en la integración: Las plantillas de *Pull Request* aseguran que el autor del código siempre documente el contexto indispensable antes de pedir una revisión: qué problema resuelve exactamente, cómo se probó la solución de forma local, y si el cambio afecta a la base de datos o a las variables de entorno. 
*   Optimización del tiempo del equipo: Al obligar al desarrollador a estructurar la información antes de hacer clic en "enviar", se genera una fricción positiva que evita que los revisores o líderes técnicos pierdan tiempo valioso haciendo preguntas básicas de contexto para entender el cambio.



### Parte 4: Validación de estándares locales

#### 10. Git Hooks y la "Primera Línea de Defensa"

Un Hook de Git (gestionado a menudo por herramientas como Husky en JavaScript) es un script automatizado que se dispara de manera nativa como reacción ante eventos específicos del control de versiones (por ejemplo, al intentar hacer un `git commit` o un `git push`). 
El `pre-commit hook` actúa como un guardián. Cuando el desarrollador intenta guardar sus cambios, el script pausa la acción de Git y ejecuta de forma obligatoria las herramientas de análisis de calidad (como el *Linter* y el *Formatter*). Si el linter detecta variables sin usar, mala indentación o violaciones a las guías de estilo del equipo, el hook aborta el commit inmediatamente, devolviendo un error en la consola y obligando al desarrollador a corregir el código.

La validación local se considera la "primera línea de defensa" en un flujo de trabajo profesional por tres motivos fundamentales:
1. Evitar la contaminación del repositorio compartido: Garantiza que al servidor remoto solo llegue código que, como mínimo, es correcto y estéticamente uniforme, protegiendo la rama principal de errores humanos básicos.
2. Filosofía "Fail-Fast" y ahorro de recursos: Si el código no cumple los estándares estéticos, es ineficiente enviarlo a la nube para que unsuntoso pipeline de Integración Continua (CI) lo rechace minutos después. El error se detecta y corrige en segundos en la terminal local.
3. Optimización de las Code Reviews: Al delegar la revisión del estilo y la sintaxis a una herramienta automática local, los revisores humanos no pierden tiempo buscando detalles faltantes, enfocando energía en auditar la arquitectura, la lógica de negocio y los principios SOLID.