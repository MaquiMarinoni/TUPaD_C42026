<div align="center">

## Unidad 05 - Práctica 2
# Demostraciones de Software

<br><br><br>

**Comisión 15**  
**Marinoni, Macarena** <marinonimacarena@gmail.com>  
Tecnicatura Universitaria en Programación - Universidad Tecnológica Nacional  
Metodología de Sistemas II  
Profesor: Videla, Flavia  
Tutor: Lobos, Diego  
16/10/2026  

</div>

<div style="page-break-after: always;"></div>

## ÍNDICE

- [Demostraciones de Software](#demostraciones-de-software)
  - [ÍNDICE](#índice)
  - [Introducción](#introducción)
    - [Parte 1: Preparación (Discovery)](#parte-1-preparación-discovery)
      - [Ejercicio 1: Cuestionario Pre-Demo](#ejercicio-1-cuestionario-pre-demo)
    - [Parte 2: Demo ejecutiva (Dueño del estudio)](#parte-2-demo-ejecutiva-dueño-del-estudio)
      - [Ejercicio 2: Tecnica "Outcome-First"](#ejercicio-2-tecnica-outcome-first)
    - [Parte 3: Demo técnica (Diseñadores)](#parte-3-demo-técnica-diseñadores)
      - [Ejercicio 3: Guion de navegación paso a paso](#ejercicio-3-guion-de-navegación-paso-a-paso)
    - [Parte 4: Manejo de preguntas y objeciones](#parte-4-manejo-de-preguntas-y-objeciones)
      - [Ejercicio 4: El poder del NO](#ejercicio-4-el-poder-del-no)
      - [Ejercicio 5: Pregunta de respuesta (Contra-pregunta)](#ejercicio-5-pregunta-de-respuesta-contra-pregunta)
    - [Parte 5: Resolución de caso real](#parte-5-resolución-de-caso-real)
      - [Ejercicio 6: Problema específico](#ejercicio-6-problema-específico)

<div style="page-break-after: always;"></div>

## Introducción

El presente trabajo práctico aborda el diseño y la ejecución estratégica de demostraciones de software profesionales aplicadas al producto **TaskHub** (sistema web de gestión de tareas con tableros Kanban, asignación de responsables, control de vencimientos y analítica en tiempo real) frente al cliente **"Estudio Pixel"**, una agencia de diseño gráfico e identidad visual integrada por 12 profesionales.



### Parte 1: Preparación (Discovery)

Antes de exponer cualquier interfaz gráfica de **TaskHub**, es necesario formular preguntas abiertas y estratégicas que revelen las fricciones operativas, los cuellos de botella y los motivadores de decisión de "Estudio Pixel".

#### Ejercicio 1: Cuestionario Pre-Demo

A continuación, se detallan las tres preguntas de diagnóstico diseñadas para relevar el contexto de la agencia antes de iniciar la sesión demostrativa:

1. `¿Cómo se organizan actualmente?`
     > *"Sabemos que hoy coordinan a las 12 personas del estudio combinando grupos de WhatsApp y planillas de Google Sheets. ¿Cómo es el flujo exacto desde que un cliente les pide un diseño o corrección por WhatsApp hasta que eso se vuelca en la planilla, se asigna a un diseñador y se aprueba la entrega final?"*

2. `¿Cuál es su MAYOR problema en la gestión de tareas?`:
     > *"En este esquema actual de trabajo con 12 diseñadores en simultáneo, ¿cuál es el cuello de botella que más problemas les genera en la semana: no saber en qué está trabajando cada diseñador en tiempo real, los errores de fechas de entrega pactadas, o el tiempo perdido con actualizaciones de estado?"*

3. `¿Qué los haría cambiar de sistema HOY?`:
     > *"Cambiar la forma en que un equipo de 12 creativos trabaja todos los días requiere un esfuerzo de adopción. ¿Qué resultado concreto tendría que demostrarles TaskHub en los primeros 15 días —por ejemplo, ahorrarle al Director 5 horas semanales de seguimiento o eliminar el 100% de las entregas fuera de fecha— para que decidan dejar atrás las planillas hoy mismo?"*


### Parte 2: Demo ejecutiva (Dueño del estudio)

#### Ejercicio 2: Tecnica "Outcome-First" 

* Guion de Apertura:
  > *"Imaginen que es viernes a las 5:00 PM. Su cliente más importante escribe para preguntar: '¿Cómo viene el rediseño de mi marca para el lanzamiento del lunes?'. Hoy, responder eso en Estudio Pixel les demanda revisar 3 grupos de WhatsApp, una planilla de Google Sheets desactualizada y llamar a 3 de sus 12 diseñadores para ver quién tiene la última versión.*
  > *Con TaskHub, en cambio, ustedes abren esta única pantalla y en 5 segundos tienen la respuesta exacta sin interrumpir a nadie: ven que el proyecto está al 85% de avance, que los bocetos ya están aprobados y que el cierre de piezas está en curso bajo responsabilidad de Sofía, con entrega programada para hoy a las 18:00 hs. Cero llamadas de urgencia antes de cerrar la semana."*

* Descripción de la pantalla proyectada:
  * Se proyecta el Dashboard ejecutivo y vista resumen de Proyectos (sin pasar por el login ni menús).
  * Indicadores clave (KPIs superiores): 
    * Tarjeta 1: *Proyectos activos de Estudio Pixel (X en curso)*.
    * Tarjeta 2: *Entregas Semanales: XX% a tiempo (X tareas críticas vencidas)*.
    * Tarjeta 3: *Carga de trabajo del Equipo (12/12 diseñadores asignados de forma equilibrada)*.
  * Bloque central destacado:
    * Barra de progreso visual al XX% (Color Verde).
    * Resumen de estados del tablero: Completado (X tareas), En Progreso (X tarea), Por Hacer (X tareas bloqueadas).
  * Gráfico lateral: Distribución de capacidad de los 12 miembros de la agencia, evidenciando de un vistazo quién tiene disponibilidad y quién está al límite operativo.


### Parte 3: Demo técnica (Diseñadores)

#### Ejercicio 3: Guion de navegación paso a paso

* Funcionalidad a demostrar: Crear una tarea y asignarla a un compañero

**[ESTOY EN: Dashboard principal / Tablero del oroyecto "Cafetería Luna"]**
* **DIGO:** *"Supongamos que el cliente 'Cafetería Luna' acaba de pedir el diseño de los vasos térmicos para su lanzamiento. En lugar de mandar un mensaje al grupo de WhatsApp que se pierde en minutos o abrir una planilla, miren cómo lo dejamos asignado y con recordatorio en menos de 20 segundos. Voy a crear la tarea directamente aquí."*
* **HAGO:** Clic en el botón primario "+ Nueva Tarea" (ubicado en la esquina superior derecha del tablero).

**[APARECE: Formulario desplegable de creación de tarea]**
* **DIGO:** *"Primero le damos un nombre claro a la pieza, y pegamos las especificaciones del cliente para que nadie tenga que preguntar dos veces qué medidas lleva."*
* **HAGO:** Escribo en el campo Título: `"Diseño de Packaging - Vasos Térmicos 12oz (Cafetería Luna)"` y en Descripción: `"Aplicar nueva paleta aprobada. Entregar original y mockup 3D"`.

**[ESTOY EN: Sección de asignación y estado dentro del mismo formulario]**
* **DIGO:** *"Ahora, en vez de preguntar por chat quién está libre, abro el selector de responsables. TaskHub me muestra a los 12 integrantes de Estudio Pixel y cuántas tareas activas tiene cada uno. Veo que Tomás tiene disponibilidad para diseño de packaging."*
* **HAGO:** Clic en el desplegable "Asignar a"*, selecciono a "Tomás R. (Diseñador Senior)" y verifico que el estado inicial quede en la columna "Por hacer".

**[ESTOY EN: Selector de fecha límite y recordatorios automáticos]**
* **DIGO:** *"Para que nadie corra a último momento, fijamos la fecha de entrega para este jueves a las 16:00 hs y activamos el recordatorio automático de 24 horas antes."*
* **HAGO:** Selecciono en el calendario "Jueves - 16:00 hs", marco el check "Recordatorio automático (24 hs antes)" y hago clic en el botón "Crear y Asignar Tarea"

**[APARECE: Tablero Kanban actualizado con la nueva tarjeta en la columna "Por hacer" y notificación toast de confirmación]**
* **DIGO:** *"Y asi de simple, la tarjeta ya está creada y visible en la columna 'Por hacer' de Cafetería Luna con la foto de Tomás y la fecha límite en verde. En este mismo instante, Tomás recibió notificación directa con toda la info centralizada, y cuando empiece a diseñar, solo tendrá que arrastrar la tarjeta a 'En progreso'. Cero mensajes perdidos en WhatsApp."*
* **HAGO:** Señalo con el cursor la tarjeta recién creada en la columna "Por hacer" mostrando la foto del diseñador y la etiqueta de vencimiento, y hago una pausa breve para que el equipo asimile la simplicidad del flujo.


### Parte 4: Manejo de preguntas y objeciones

#### Ejercicio 4: El poder del NO

* Situación: Un diseñador del equipo interrumpe y pregunta: "¿Se pueden subir archivos de Photoshop (.PSD) directamente?" (El producto NO soporta almacenamiento directo de archivos `.PSD`).
* Respuesta honesta:
  > *"No, TaskHub no permite subir archivos pesados `.PSD` o `.AI` de forma directa, y es una decisión de diseño intencional para que el tablero les cargue siempre en menos de un segundo y no se vuelva lento como les pasa hoy cuando buscan adjuntos pesados. Lo que sí hacen las agencias de diseño en TaskHub es pegar directamente en la tarjeta el enlace a la carpeta de Google Drive, Dropbox o el prototipo de Figma donde guardan el editable, y adjuntar acá únicamente el `.PNG` o `.JPG` liviano de previsualización. Así mantienen toda la velocidad del tablero y acceden al editable original con un solo clic. ¿Hoy ustedes guardan los `.PSD` en Google Drive o en un servidor local del estudio?"*

#### Ejercicio 5: Pregunta de respuesta (Contra-pregunta)

* Situación: Un integrante del estudio pregunta: "¿Puedo ver las tareas de mi compañero?"
* **Contra-pregunta:**
  > *"Antes de contarte cómo se configura la visibilidad, me gustaría entender tu uso diario: ¿necesitás ver las tareas de tu compañero para saber cuándo te pasa una pieza que tenés que continuar vos, o te preocupa más bien que otros puedan editar tus entregas por error?"*

Si se responde rapido "Sí, todos ven todo", puede generar recelo en quien busca privacidad; si se responde "No, está restringido", se puede generar frustacion a quien buscaba trabajo colaborativo. La contra-pregunta activa el protocolo de escucha, obliga al usuario a revelar su verdadero interes y permite mostrar la configuración de permisos de TaskHub que resuelve su inquietud.


### Parte 5: Resolución de caso real

#### Ejercicio 6: Problema específico

* Situación: Durante la demo, el director creativo interrumpe y objeta "Mis diseñadores entregan todo el último día porque no planifican. ¿Esto me ayuda con ESO o es solo una lista linda?"

* Respuesta
  > *"Entiendo su frustración; cuando los 12 diseñadores entregan sobre la hora en WhatsApp, termina haciendo de cuello de botella corrigiendo todo un viernes a la noche. Consulto, ¿esas demoras ocurren porque olvidan la fecha final o porque no dividen entregas grandes en avances previos?"*
  > *Para evitar eso, TaskHub utiliza fechas límite con recordatorios automáticos escalonados. Si miramos acá en pantalla la tarjeta de 'Cafetería Luna' vemos que se configura un alerta 48 horas antes para revisar el boceto y el tablero resalta en amarillo quién aún no pasó su tarea a 'En progreso' "*
