<div align="center">

## Unidad 05 - Práctica 3
# IA como Copiloto

<br><br><br>

**Comisión 15**  
**Marinoni, Macarena** <marinonimacarena@gmail.com>  
Tecnicatura Universitaria en Programación - Universidad Tecnológica Nacional  
Metodología de Sistemas II  
Profesor: Videla, Flavia  
Tutor: Lobos, Diego  
17/10/2026  

</div>

<div style="page-break-after: always;"></div>

## ÍNDICE

- [IA como Copiloto](#ia-como-copiloto)
  - [ÍNDICE](#índice)
  - [Introducción](#introducción)
    - [Parte 1: Prompts Efectivos para Requerimientos](#parte-1-prompts-efectivos-para-requerimientos)
      - [Ejercicio 1: Estructura de Prompt (Básico → Mejorado)](#ejercicio-1-estructura-de-prompt-básico--mejorado)
      - [Ejercicio 2: Técnica "Chain of Thought"](#ejercicio-2-técnica-chain-of-thought)
    - [Parte 2: Validación crítica de resultados](#parte-2-validación-crítica-de-resultados)
      - [Ejercicio 3: Detectar problemas en respuestas de IA](#ejercicio-3-detectar-problemas-en-respuestas-de-ia)
    - [Parte 3: Trazabilidad de Decisiones](#parte-3-trazabilidad-de-decisiones)
      - [Ejercicio 4: Documentar el uso de IA (Bitácora)](#ejercicio-4-documentar-el-uso-de-ia-bitácora)
    - [Parte 4: Límites de la IA](#parte-4-límites-de-la-ia)
      - [Ejercicio 5: Confidencialidad y propiedad intelectual](#ejercicio-5-confidencialidad-y-propiedad-intelectual)
    - [Parte 5: Uso ético y responsable](#parte-5-uso-ético-y-responsable)
      - [Ejercicio 6: Citación de asistencia de IA](#ejercicio-6-citación-de-asistencia-de-ia)
      - [Ejercicio 7: Caso ético real](#ejercicio-7-caso-ético-real)
    - [Autoevaluación](#autoevaluación)

<div style="page-break-after: always;"></div>

## Introducción

La incorporación de la Inteligencia Artificial Generativa y los Modelos Grandes de Lenguaje (LLMs) en el ciclo de vida del software ha redefinido la productividad en la Ingeniería de Requerimientos. Sin embargo, su efectividad real depende de un cambio de paradigma: concebir a la IA como un copiloto analítico y nunca como un sustituto del juicio crítico del ingeniero.


### Parte 1: Prompts Efectivos para Requerimientos

#### Ejercicio 1: Estructura de Prompt (Básico → Mejorado)


* Descripción informal del cliente: 
  > *"Necesitamos un sistema para gestionar las reservas del gimnasio. Que los usuarios puedan reservar clases, cancelar si no pueden ir y que el instructor vea quiénes confirmaron. También queremos que envíe recordatorios."*

* **Tarea A: Prompt BÁSICO**
  > *"Tengo un cliente que quiere un sistema para gestionar las reservas de un gimnasio donde los usuarios reserven clases, cancelen, el instructor vea los confirmados y mande recordatorios. Escribi la lista de requerimientos para este sistema."*

* **Tarea B: Prompt MEJORADO**
  > [CONTEXTO]: *Actuá como un Analista Funcional e Ingeniero de Requerimientos Senior. Estamos diseñando una aplicación web y mobile para gestionar las reservas de turnos de un gimnasio. Los actores principales son: Socio (alumno), instructor de clase y administrador del gimnasio.*  
  > [TAREA]: *A partir de la siguiente necesidad del cliente ('Permitir a los socios reservar clases, cancelar su asistencia, listar confirmados para el instructor y enviar recordatorios automáticos'), desglosá y redactá la especificación formal de requerimientos del sistema. Debés contemplar reglas de negocio implícitas del dominio (control de cupo máximo por salón, lista de espera y tiempo límite previo para cancelar sin penalización).*
  > [FORMATO]: *Entregá la respuesta estructurada en una tabla Markdown con las siguientes columnas: `ID` (RF-XX o RNF-XX), `Categoría` (Funcional / No Funcional), `Actor Asociado`, `Descripción del Requerimiento`, `Prioridad (MoSCoW: Must, Should, Could)` y `Criterio de Aceptación / Verificabilidad`.*
  > [CRITERIOS]: *Generá al menos 6 Requerimientos Funcionales y 3 No Funcionales. Redactá cada ítem aplicando sintaxis SMART: evitá adjetivos ambiguos ('rápido', 'fácil', 'amigable') y definí métricas cuantificables, umbrales de tiempo exactos y condiciones de borde verificables por QA."*


#### Ejercicio 2: Técnica "Chain of Thought"

La técnica *Chain of Thought* (CoT) pide a la IA que "piense paso a paso" antes de dar la respuesta final.

* Situación: Un requerimiento dice: *"El sistema debe ser rápido"*.
* Prompt con Chain of Thought:
  > *"Actuá como un Arquitecto de Software y Especialista en Ingeniería de Requerimientos. Necesito transformar el siguiente requerimiento ambiguo expresado por un cliente en especificaciones no funcionales de rendimiento verificables para nuestro sistema de reservas: 'El sistema debe ser rápido'.*
  > *Antes de dar la respuesta final, razoná paso a paso ejecutando la siguiente cadena de pensamiento:*
  > *Paso 1 (Diagnóstico de Ambigüedad): Analizá y explicá por qué la palabra 'rápido' es subjetiva, no testeable y qué riesgos de deuda técnica o conflicto contractual genera entre el equipo de desarrollo y el cliente.*
  > *Paso 2 (Desglose de Escenarios Críticos): Identificá las 3 operaciones críticas del sistema donde la velocidad impacta directamente al usuario (ej. carga del calendario de clases, transacción de confirmación de reserva y disparo de notificaciones).*  
  > *Paso 3 (Definición de Variables y Métricas): Determiná qué indicadores técnicos permiten medir cada escenario de forma objetiva (tiempo de respuesta en segundos/milisegundos en el percentil 95, cantidad de usuarios concurrentes en hora pico y tipo de conexión móvil 4G/Wi-Fi).*  
  > *Paso 4 (Reformulación Verificable): Recién después de completar el análisis previo, redactá 3 Requerimientos No Funcionales (RNF) de rendimiento bajo sintaxis SMART que incluyan su respectivo criterio de prueba automatizable."*


### Parte 2: Validación crítica de resultados

#### Ejercicio 3: Detectar problemas en respuestas de IA

A continuación, se presenta la validación crítica de los 4 requerimientos generados por la IA para el caso del "Sistema de Biblioteca Escolar":

| Req. # | Requerimiento Original (IA) | ¿Es verificable? | ¿Es completo? | Propuesta Mejorada |
| :---: | :--- | :--- | :--- | :--- |
| **1** | *"El sistema debe permitir buscar libros"* | **NO** (Es genérico, no especifica bajo qué parámetros o filtros se ejecuta la búsqueda). | **NO** (Faltan los actores y las condiciones de la búsqueda). | *El sistema debe permitir a los alumnos y bibliotecarios buscar material bibliográfico utilizando filtros combinados por "Título", "Autor" o "Editorial", retornando únicamente resultados con stock disponible.* |
| **2** | *"Los usuarios deben poder hacer consultas rápidamente"* | **NO** ("rápidamente" es subjetivo y no puede medirse en un test automatizado). | **NO** (No establece bajo qué condiciones de red o volumen de datos aplica). | *El motor de búsqueda del catálogo debe procesar y retornar los resultados en pantalla en un tiempo máximo de 1.5 segundos, asumiendo una conexión de red estándar.* |
| **3** | *"El sistema debe tener una interfaz amigable"* | **NO** (La "amigabilidad" no es un criterio técnico; depende de la percepción de cada usuario). | **NO** (No define flujos de UX/UI ni esfuerzo). | *La interfaz de usuario debe ser responsiva y permitir que un alumno concrete la reserva de un libro en un máximo de 3 clics partiendo desde la pantalla principal, sin requerir asistencia previa.* |
| **4** | *"Debe almacenar información de forma segura"* | **NO** (La "seguridad" es un concepto abstracto si no se apoya en protocolos o normativas específicas). | **NO** (No aclara si protege datos en tránsito o en reposo). | *El sistema debe encriptar todas las contraseñas en la base de datos utilizando el algoritmo bcrypt, y todo el tráfico de datos (en tránsito) debe ejecutarse obligatoriamente bajo protocolo HTTPS/TLS 1.2+.* |


### Parte 3: Trazabilidad de Decisiones

El uso de Inteligencia Artificial como asistente técnico exige un gobierno estricto de la información y la asunción de responsabilidad profesional (*Accountability*). Las sugerencias de priorización generadas algorítmicamente deben ser registradas y sometidas a auditoría humana, funcionando como una adaptación ligera de los Registros de Decisiones Arquitectónicas (ADR) para evitar la "amnesia de diseño" y documentar la cadena de custodia de la decisión.

#### Ejercicio 4: Documentar el uso de IA (Bitácora)

A continuación se presenta el registro de trazabilidad aplicado a la priorización de un sistema de facturación:

**BITÁCORA DE USO DE IA**

*   Fecha: 17/10/2026
*   Tarea realizada con IA: Priorización inicial del backlog de requerimientos para el MVP del Sistema de Facturación Electrónica B2B.
*   Herramienta utilizada: Claude 3.5 Sonnet (Anthropic) / ChatGPT Plus.
*   Prompt exacto utilizado: 
    > *"Actuá como un Product Owner. Evalúa la siguiente lista de 10 requerimientos para un sistema de facturación y priorizalos utilizando la matriz MoSCoW (Must, Should, Could, Won't). Considerá como contexto crítico de negocio que el principal riesgo del cliente es la evasión de multas fiscales por demoras en la homologación con AFIP. Asigná prioridad alta, media o baja justificando cada decisión técnica."*
*   Resultado obtenido (resumen): La IA clasificó correctamente como *Must Have* (Alta) la integración con la API de AFIP y la generación del PDF con código QR. Sin embargo, clasificó como *Could Have* (Baja) el envío automático de la factura por correo electrónico al cliente final.
*   Validación humana realizada: Se auditó la salida de la IA contrastándola con el marco legal vigente. El analista detectó una discrepancia: si bien el correo electrónico parece funcionalmente secundario, la normativa comercial exige notificar fehacientemente al consumidor, por lo que no puede ser de prioridad baja.
*   Decisión final tomada: Se aprobó el 80% de la priorización sugerida por la IA, pero se aplicó un *override* (anulación manual) sobre el requerimiento de "Envío por email", elevándolo de *Could Have* a *Must Have* antes de ingresarlo al flujo del Sprint.
*   Responsable de la decisión: Marinoni, Macarena (Analista de Sistemas / Ingeniería de Requerimientos).

### Parte 4: Límites de la IA

#### Ejercicio 5: Confidencialidad y propiedad intelectual

A continuación, se evalúa el nivel de riesgo de distintas situaciones con un modelo de IA público:

| Situación | Nivel de Riesgo (Seguro / Riesgoso) |
| :--- | :---: |
| Pegar código fuente completo de un proyecto privado de la empresa | **Riesgoso** |
| Preguntar cómo escribir un algoritmo genérico de ordenamiento | **Seguro** |
| Compartir nombres reales de clientes y sus datos personales | **Riesgoso** |
| Pedir ayuda con conceptos teóricos de ingeniería de software | **Seguro** |

Justificación de los casos riesgosos:
Compartir el código fuente completo de un proyecto privado o ingresar datos personales reales de clientes constituye una vulneración directa a los Acuerdos de Confidencialidad (NDA) y a las normativas de protección de datos personales. 
Los LLMs de acceso público pueden almacenar y procesar estas interacciones para el reentrenamiento continuo de sus modelos. El profesionalismo exige que, al consultar a una IA por un error de código, el desarrollador aísle únicamente el bloque problemático, modifique el nombre de las variables de negocio y reemplace cualquier información sensible por datos ficticios (*Mock Data*).


### Parte 5: Uso ético y responsable

#### Ejercicio 6: Citación de asistencia de IA

Contexto: Se utilizó IA para revisar gramática, generar un borrador de priorización y sugerir reformulaciones de requerimientos ambiguos.

Citación propuesta:
> *"Para la elaboración de las especificaciones de este documento, se utilizó el modelo de lenguaje Claude 3.5 (Anthropic) / ChatGPT Plus exclusivamente como asistente técnico. Su alcance de uso se limitó a la corrección ortográfica, la estructuración inicial de la matriz de priorización y la sugerencia de reformulación para requerimientos ambiguos. Todas las decisiones de negocio, la priorización final, el alcance del sistema y la validación técnica fueron revisadas, modificadas y aprobadas bajo el criterio y responsabilidad profesional del autor."*


#### Ejercicio 7: Caso ético real

**Caso:** Un compañero de equipo copió un informe completo generado por IA sin revisarlo, validarlo ni citarlo, y es incapaz de defenderlo ante preguntas específicas.

*   Problemas éticos identificados
    Existe acto de deshonestidad intelectual y falta de transparencia al adjudicarse el texto de una herramienta de terceros como propio. Al no revisar ni entender el documento, el profesional es negligente y nada ético, faltando al cuidado exigido en la ingeniería de software.
*   Riesgos profesionales de la esta conducta
    A nivel de proyecto, introduce un riesgo alto de propagar "alucinaciones" de la IA directo al equipo de desarrollo, causando que se programen funciones incorrectas, lo que deriva en deuda técnica y sobrecostos. A nivel personal, el analista pierde por completo su credibilidad técnica, reputación y confianza frente a los *stakeholders* y directivos al no poder sostener ni explicar la arquitectura de su propio entregable.
*   ¿Cómo debería haberse usado la IA correctamente?
    Debería haberse utilizado como un Copiloto: para estructurar ideas, plantear *prompts* con contexto y luego auditar línea por línea la salida del modelo (Verificación y Validación). Cualquier requerimiento sugerido por la IA debe ser contrastado con el problema real, reformulado por el analista, documentado en una bitácora de trazabilidad y, finalmente, incluir la cita metodológica correspondiente en el informe entregado.


### Autoevaluación

*   [x] Mis prompts incluyen contexto, tarea específica y formato esperado.
*   [x] Validé críticamente las respuestas de la IA en vez de copiarlas directamente.
*   [x] Documenté qué prompts usé y qué decisiones tomé.
*   [x] Identifiqué correctamente información confidencial que NO debe compartirse.
*   [x] Sé cómo citar correctamente el uso de IA en trabajos profesionales.
*   [x] Entiendo que la IA es un ASISTENTE, no un reemplazo de mi criterio profesional.

