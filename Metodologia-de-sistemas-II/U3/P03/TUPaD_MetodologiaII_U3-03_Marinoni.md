<div align="center">

## Unidad 03 - Practica 3
# Automatización de calidad y blindaje

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

## iNDICE
  - [Introducción](#introducción)
  - [Desarrollo](#desarrollo)
    - [1. Configuración de un Pre-commit Hook](#1-configuración-de-un-pre-commit-hook)
    - [2. Auditoría estática](#2-auditoría-estática)
    - [3. Informe decalidad en verde](#3-informe-decalidad-en-verde)

<div style="page-break-after: always;"></div>

## Introducción
El presente informe detalla la implementación de estrategias de automatización de calidad para el ciclo de vida del software. Delegar la auditoría del código en herramientas automáticas permite eliminar la subjetividad humana y asegurar que ningún incremento viole las reglas técnicas del equipo. A continuación, se describen los mecanismos de blindaje local (pre-commit hooks), el diagnóstico mediante análisis estático y la consolidación del Informe de calidad en verde, artefacto que certifica que el software está listo para su integración.

## Desarrollo

### 1. Configuración de un Pre-commit Hook

Para asegurar que ningún desarrollador pueda proponer código que viole la *Definition of Done* (DoD), es imperativa la implementación de Pre-commit Hooks en la arquitectura del repositorio local. Este script automatizado se dispara de manera nativa inmediatamente después de invocar el comando `git commit`, ejecutando una cadena de custodia secuencial y obligatoria:

1. **Formatter:** Garantiza la estética unificada del código.
2. **Linter:** Audita la sintaxis, detecta malas prácticas y variables en desuso.
3. **Pruebas Unitarias:** Ejecuta la suite de tests locales de forma dinámica.

**Comportamiento ante un fallo y protección de la rama principal:**
Si durante esta secuencia el formateador detecta fallos insalvables, el linter encuentra una variable no declarada, o un solo test unitario arroja un resultado fallido (en rojo), el script interrumpe la operación de Git de forma abrupta. Como resultado, el proceso aborta el *commit* y devuelve un código de error en la consola. 

Este mecanismo protege la rama principal porque retiene el código defectuoso exclusivamente en el espacio de trabajo local del programador, obligándolo a sanear la deuda técnica antes de poder registrar el cambio y enviarlo al repositorio remoto.

### 2. Auditoría estática

El análisis estático avanzado funciona como una auditoría de calidad profunda sobre los planos lógicos del sistema, examinando su salud estructural en frío (sin necesidad de ejecutar el software). Ante un escenario donde un módulo presenta indicadores de baja calidad en herramientas de grado industrial (como SonarQube), identificamos los siguientes puntos críticos y sus respectivas estrategias de mitigación:

**A. Identificación de puntos críticos mediante métricas:**
1. **Complejidad ciclomática elevada:** La herramienta detectó funciones con un alto índice de bloques condicionales anidados. Esto expone un exceso de caminos lógicos independientes, lo que incrementa la probabilidad de fallos lógicos y eleva el costo de mantenimiento.
2. **Duplicación de código:** Se detectaron bloques lógicos idénticos o redundantes dispersos en diferentes archivos del repositorio. Esto vulnera directamente el principio de no repetición (DRY - Don't Repeat Yourself) y dificulta la modularización del sistema.
3. **Seguridad de dependencias (vulnerabilidades):** El escaneo de los archivos de manifiesto del proyecto (ej. `requirements.txt`) alertó sobre el uso de bibliotecas de terceros que figuran en las bases de datos globales de vulnerabilidades conocidas (registros CVE).

**B. Estrategia de refactorización y saneamiento:**
Para reducir la complejidad técnica y garantizar la seguridad antes de proponer la integración del código, se aplicará la siguiente estrategia:
*   **Refactorización y Reducción de Complejidad:** Se aplicarán técnicas de refactoring seguro avaladas por la filosofía Clean Code. Específicamente, se utilizará la técnica *Extract Method* para extraer los fragmentos de código duplicado hacia métodos nuevos con nombres descriptivos. Asimismo, para mitigar la complejidad ciclomática, se simplificarán las estructuras condicionales delegando responsabilidades a clases más pequeñas y cohesivas.
*   **Aseguramiento de Dependencias:** Al detectarse un paquete inseguro, el sistema debe bloquear el flujo de trabajo. La estrategia consiste en analizar el reporte técnico emitido por el escaner, aislar la biblioteca comprometida y forzar la actualización hacia la versión estable y parchada que subsana la brecha de seguridad (resolución del CVE).

<div style="page-break-after: always;"></div>

### 3. Informe decalidad en verde

El Informe decalidad en verde representa el artefacto consolidado que recopila las evidencias analíticas generadas localmente para certificar que el incremento de software cumple de forma estricta con la *Definition of Done* (DoD) y se encuentra apto para su integración. 

A continuación, se consolidan las cuatro evidencias obligatorias de laboratorio exigidas para aprobar el *Pull Request* (PR):

1. **Evidencia de gobernanza de entrada:** 
   * **Trazabilidad:** [Enlace al Pull Request #42 vinculado al Issue #15 - "Implementar cálculo de descuentos"]
   * **Descripción:** Se certifica que el cambio propuesto en la rama responde directamente a un requerimiento formal estructurado, asegurando la trazabilidad histórica en el repositorio y anulando la ambigüedad.

2. **Evidencia sintáctica y estética:** 
   * **Logs del Pre-commit Hook:** Ejecución de `Formatter` y `Linter` finalizada con código de salida `0` (Success).
   * **Descripción:** Se aportan los logs que prueban la ejecución exitosa del script local. Se certifica la uniformidad visual del código y la ausencia total de variables en desuso, errores lógicos tempranos o excepciones de sintaxis.

3. **Evidencia dinámica:**
   * **Reporte de Cobertura (Code Coverage):** 85% de *Branch Coverage* alcanzado (Suite ejecutada 100% en verde).
   * **Descripción:** Se certifica matemáticamente el cumplimiento del umbral mínimo de pruebas. Las aseveraciones confirman que todos los caminos condicionales de la lógica de negocio fueron recorridos exitosamente, sin introducir regresiones.

4. **Evidencia Estructural:**
   * **Diagnóstico de análisis estático (SonarQube):** 0 Vulnerabilidades (CVE), 0 Code Smells críticos, complejidad ciclomática controlada.
   * **Descripción:** Se certifica mediante escaneo en frío que el plano lógico del sistema posee un índice de deuda técnica aceptable y que las dependencias de terceros se encuentran libres de vulnerabilidades críticas conocidas.

**Veredicto Final:** El presente desarrollo supera la totalidad de los controles de calidad exigidos, blindando la rama principal. **APROBADO PARA INTEGRACIÓN**.

[def]: #automatización-de-calidad-y-blindaje