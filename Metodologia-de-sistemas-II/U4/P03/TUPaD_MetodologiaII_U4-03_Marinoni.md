<div align="center">

## Unidad 04 - Practica 23
# Entrega Continua y Resiliencia del Software

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
- [Parte 1: Integración Continua (CI)](#parte-1-integración-continua-ci)
- [Parte 2: Versionado Semántico (SemVer)](#parte-2-versionado-semántico-semver)
- [Parte 3: Entrega y despliegue continuo (CD)](#parte-3-entrega-y-despliegue-continuo-cd)
- [Parte 4: Resiliencia y mitigación de riesgos](#parte-4-resiliencia-y-mitigación-de-riesgos)


<div style="page-break-after: always;"></div>

## Introducción

El presente informe marca el paso final en la profesionalización del ciclo de vida del software: la automatización de la integración y el despliegue. Tras haber establecido flujos de trabajo colaborativos, el objetivo ahora es diseñar pipelines que actúen como "estaciones de inspección" automáticas, validando cada incremento mediante pruebas y análisis estático antes de su fusión.


### Parte 1: Integración Continua (CI)

#### 1. Filosofía de Trabajo "Fail-Fast" en un Pipeline de CI

En el contexto de la IC, un *Pipeline* es una secuencia automatizada de trabajos o pasos que validan cada incremento de código. La importancia de la filosofía "Fail-Fast" (Fallo Rápido) radica en detener de inmediato toda esta secuencia de ejecución si se detecta un error en una etapa temprana, bloqueando la integración sin intentar avanzar a las siguientes validaciones.

Esta práctica beneficia al desarrollo de dos formas:
*   Ahorro de recursos técnicos y financieros: Las etapas avanzadas de un pipeline consumen una gran cantidad de tiempo de cómputo y memoria. Si el código falla en el paso inicial por un simple error de estilo o sintaxis, el *Fail-Fast* detiene el proceso de inmediato, evitando recursos en ejecutar pruebas complejas sobre un código roto.
*   Agilidad del equipo: En metodologías ágiles donde los desarrolladores integran cambios varias veces al día, un pipeline lento destruye la velocidad operativa. El *Fail-Fast* garantiza que el autor del código reciba una alerta roja de forma casi instantánea, permitiéndole corregir el error localmente.

#### 2. Anatomía del pipeline (Stages)

*   Lint & Static Analysis:
    *   *Validación:* Inspecciona el código fuentesin ejecutarlo. El *Linter* analiza el árbol de sintaxis abstracta para detectar violaciones de estilo y malas prácticas (ej. variables sin uso). Las herramientas de análisis estático (como SonarQube) calculan métricas estructurales complejas, como la complejidad ciclomática o la duplicación de bloques lógicos.
    *   *Riesgo que mitiga:* Previene la acumulación de Deuda Técnica. Mitiga el riesgo de introducir código difícil de mantener o frágil en la rama principal.

*   Unit Tests:
    *   *Validación:* Ejecuta la lógica de los componentes de forma dinámica en aislamiento total (utilizando dobles de prueba como *Mocks* y *Stubs* para no depender de bases de datos o red). Se validan las aseveraciones lógicas y se inyectan datos inválidos para asegurar que el sistema maneje correctamente los casos de borde (valores nulos, desbordamientos).
    *   *Riesgo que mitiga:* Mitiga el riesgo de introducir regresiones funcionales. Evita que un cambio rompa la lógica de negocio existente y previene que excepciones no controladas provoquen la caída del sistema en producción.

*   Security Scan:
    *   *Validación:* Las herramientas de seguridad contrastan los archivos del proyecto (como `package.json` o `requirements.txt`) contra las bases de datos globales de vulnerabilidades (registros CVE). 
    *   *Riesgo que mitiga:* Neutraliza brechas de ciberseguridad. Mitiga el riesgo crítico de desplegar a producción software que dependa de paquetes de terceros obsoletos o comprometidos, protegiendo al sistema de ataques.

#### 3. Pipeline as Code

Pipeline as Code significa que las instrucciones, etapas y reglas de validación que debe ejecutar el servidor de IC no se configuran manualmente a través de interfaces gráficas, sino que se declaran explícitamente en un archivo de texto estructurado (generalmente en formato YAML). Este archivo actúa como el "cerebro" del pipeline.
Almacenar este archivo en la raíz del repositorio de código aporta los siguientes beneficios:
*   Permite que el pipeline evolucione de manera conjunta con el código de la aplicación. Si una nueva rama del proyecto incorpora una base de datos nueva o requiere un paso extra de testing, el desarrollador actualiza el YAML en ese mismo commit, asegurando que el entorno de pruebas coincida exactamente con las necesidades de esa versión del código.
*   Al tratar la configuración del servidor como si fuera código fuente tradicional, cualquier modificación en las reglas del pipeline queda registrada en el historial de Git (quién lo cambió, cuándo y por qué). 
*   Si una actualización en el pipeline rompe el proceso de validación, el equipo puede aplicar un `git revert` o un `git checkout` para restaurar instantáneamente la configuración funcional anterior.



### Parte 2: Versionado Semántico (SemVer)

#### 4. El Lenguaje del Cambio

Situacion: Se debe asignar un nuevo número de versión a un sistema que actualmente está en la v2.4.1. 

*   Escenario A: Pasar a `v2.4.2`
*Justificación:* Corregir un error de cálculo matemático sin alterar la forma en que los usuarios interactúan con el sistema es un cambio completamente retrocompatible. Por regla, se incrementa exclusivamente el número de PARCHE (Patch), indicando una corrección menor de errores.

*   Escenario B: Pasar a `v2.5.0`
*Justificación:* La incorporación de la nueva funcionalidad "Exportar a PDF" agrega valor pero se mantiene totalmente retrocompatible con las funciones actuales. En este caso se debe incrementar el número MENOR (Minor). Por convención de la especificación SemVer, cada vez que se incrementa el número Menor, el componente Parche se reinicia a cero.

*   Escenario C: Pasar a `v3.0.0`
*Justificación:* Eliminar una función existente y alterar el mecanismo de autenticación introduce *Breaking Changes* (cambios destructivos). Esto obligará a otros sistemas dependientes a modificar su propio código para no romperse. Para alertar sobre este alto nivel de riesgo, se debe incrementar el número MAYOR (Major), reiniciando matemáticamente los componentes Menor y Parche a cero.


#### 5. Tags y Disparadores

Un **Tag** es una referencia estática e inmutable que apunta a un commit específico en el historial, utilizado como etiqueta para marcar hitos exactos o lanzamientos de versión. Su vínculo con la automatización del despliegue a producción (CD) se da a través de los **Events (Triggers o Disparadores)** configurados en el archivo YAML del pipeline. 

En flujos de trabajo profesionales, desplegar a producción frente a cada evento de `push` a la rama principal puede ser riesgoso. Para controlarlo, el equipo configura el orquestador (ej. GitHub Actions) para que permanezca inactivo hasta detectar un evento específico de "creación de Tag". Cuando el responsable del lanzamiento ejecuta el comando de subida de la etiqueta, el sistema intercepta este evento y lo utiliza como disparador automático. Esto asegura que el servidor tome únicamente ese estado inmutable del código y lo envíe de forma segura al entorno productivo.



### Parte 3: Entrega y despliegue continuo (CD)

#### 6. Entrega (Delivery) vs. Despliegue (Deployment)

Aunque ambos conceptos buscan automatizar el ciclo de vida del software más allá de la fase de CI, existe una diferencia entre ellos que radica exclusivamente en la intervención humana:
*   Entrega Continua: El pipeline automatiza la construcción, el testing y la preparación del artefacto hasta un entorno previo a producción (Staging). Sin embargo, el paso final hacia el entorno productivo real requiere explícitamente una aprobación manual. El código siempre está listo para ser desplegado, pero el desarrollador decide cuándo hacerlo.
*   Despliegue Continuo: No hay barreras humanas. Si el incremento de código supera todas las pruebas automatizadas del pipeline, se despliega automáticamente y de forma directa en los servidores de producción frente a los usuarios finales.

En el sector bancario o en sistemas de software médico se opta por la Entrega Continua. En este tipo de negocios críticos, aunque el código pase las pruebas técnicas automáticas, suelen existir requisitos de cumplimiento normativo o auditorías legales que exigen firmas formales de los responsables de seguridad antes de autorizar que un nuevo cálculo de intereses financieros o un protocolo de salud impacte en la base de usuarios reales.


#### 7. Gestión de entornos 

1.  Entorno de Desarrollo (Dev): Es el primer entorno de prueba compartido. Aquí se despliega automáticamente el código tras superar la fase de CI. Permite a los desarrolladores verificar que las distintas piezas de código que acaban de fusionar funcionen correctamente juntas en un servidor real. Suele ser un entorno más inestable y de cambios rápidos.
2.  Entorno de Staging (Pre-producción): Es el puente crítico entre el desarrollo y el cliente.
3.  Entorno de Producción (Prod): Es el entorno final donde el software es utilizado por los usuarios reales y procesa datos críticos del negocio.

El entorno de *Staging* tiene una regla de oro: debe ser una réplica exacta y simétrica de Producción (mismos recursos de hardware, misma configuración de red, y en lo posible, bases de datos anonimizadas de tamaño similar). 
Su función específica antes del paso final es servir como el último simulacro de seguridad. Al ser idéntico a Producción, garantiza que si el código funciona perfectamente allí, funcionará exactamente igual para los usuarios finales.


#### 8. El principio de inmutabilidad

Un artefacto inmutable es un paquete de software ya construido, compilado y sellado que, una vez generado en la fase de IC, no puede ser alterado, parcheado ni modificado bajo ninguna circunstancia.

Es crítico que el código no se vuelva a compilar cuando se promueve a través de los distintos entornos (Dev, Staging y Prod). Si se recompilara en cada estación, se introducirían variables externas. 
Al trasladar un artefacto inmutable, el equipo tiene la garantía de que el paquete exacto (bit a bit) que superó las rigurosas pruebas de seguridad y estrés en *Staging* es idénticamente el mismo que se va a ejecutar frente a los usuarios reales en *Producción*.


### Parte 4: Resiliencia y mitigación de riesgos

#### 9. El mecanismo de Rollback

Ante una falla crítica en el entorno de producción (por ejemplo, la caída de un servicio tras una actualización), el equipo de ingeniería debe priorizar la restauración inmediata del servicio por sobre el diagnóstico del error.

¿En qué consiste a nivel de infraestructura?
    Un Rollback consiste en ordenar al orquestador de despliegue o balanceador de carga que apague o destruya los servidores/contenedores que ejecutan la versión defectuosa, y vuelva a desplegar el artefacto inmutable de la versión anterior que se consideraba estable.
    
La ventaja de los Tags de SemVer:
    Haber trabajado con un control de versiones basado en Tags de SemVer es lo que hace que este proceso sea casi instantáneo. Como cada Tag está vinculado de manera estricta a un artefacto ya compilado y almacenado en un registro, el equipo no necesita volver a pasar por la fase de CI ni recompilar el código.

#### 10. Estrategias progresivas: Blue-Green vs. Canary Deployment

*   Blue-Green Deployment (Cambio de switch total): Se mantienen dos entornos de producción arquitectónicamente idénticos (eno ejecuta la versión estable actual y el otro ejecuta la nueva versión). Una vez que la segunda versión está lista, el balanceador de carga redirige el 100% del tráfico de los usuarios del primero al segundo en un solo instante. No hay mezcla de usuarios; todos ven la versión antigua o todos ven la versión nueva.

*  Canary Deployment (Despliegue gradual): El balanceador de carga desvía solo un pequeño porcentaje del tráfico real (por ejemplo, el 5%) hacia los servidores que tienen la nueva versión, mientras el 95% restante sigue utilizando la versión estable de manera transparente. Si los monitores de sistema no reportan anomalías en ese 5%, el tráfico hacia la nueva versión se incrementa progresivamente (10%, 50%, 100%) hasta reemplazar totalmente a la anterior.

De acuerdo a lo analizado, la estrategia Canary Deployment es la única que permite probar el código con un grupo reducido de usuarios reales antes del lanzamiento total.