<div align="center">

## Unidad 04 - Practica 1
# Git avanzado

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
- [Git avanzado](#git-avanzado)
  - [ÍNDICE](#índice)
  - [Introducción](#introducción)
    - [Parte 1: La "Física" de Git](#parte-1-la-física-de-git)
      - [1. El modelo de objetos](#1-el-modelo-de-objetos)
      - [2. Direccionamiento por contenido](#2-direccionamiento-por-contenido)
      - [3. El grafo dirigido acíclico (DAG)](#3-el-grafo-dirigido-acíclico-dag)
    - [Parte 2: Áreas de trabajo y flujo atómico](#parte-2-áreas-de-trabajo-y-flujo-atómico)
      - [4. Las tres areas y la secuencia de ejecución](#4-las-tres-areas-y-la-secuencia-de-ejecución)
      - [5. El rol de HEAD y el estado Detached](#5-el-rol-de-head-y-el-estado-detached)
    - [Parte 3: Gestión y cirugía del historial](#parte-3-gestión-y-cirugía-del-historial)
      - [6. Limpieza de historial](#6-limpieza-de-historial)
      - [7. Manipulación quirúrgica: Cherry-pick vs. Merge](#7-manipulación-quirúrgica-cherry-pick-vs-merge)
    - [Parte 4: Casos prácticos de resiliencia](#parte-4-casos-prácticos-de-resiliencia)
      - [8. Escenario de desastre](#8-escenario-de-desastre)
      - [9. Reset vs. Revert](#9-reset-vs-revert)
    - [Parte 5: Diagnóstico y auditoría](#parte-5-diagnóstico-y-auditoría)
      - [10. Comandos de Bajo Nivel (Plumbing)](#10-comandos-de-bajo-nivel-plumbing)

<div style="page-break-after: always;"></div>

## Introducción

El presente informe desarrolla los conceptos avanzados de la arquitectura de Git, superando la visión tradicional de un simple sistema de control de versiones para analizarlo como una base de datos. 

<div style="page-break-after: always;"></div>

### Parte 1: La "Física" de Git

#### 1. El modelo de objetos

La arquitectura interna de Git no almacena simplemente las diferencias entre archivos, sino que opera como una base de datos de objetos criptográficos. Para formar una instantánea (snapshot) del proyecto en un momento dado, Git utiliza tres tipos de objetos fundamentales que se almacenan físicamente en el directorio oculto `.git/objects`:

*   **Blobs (Binary Large Objects):** Son la unidad de almacenamiento más básica. Su única función es guardar el contenido puro de los archivos, sin registrar sus metadatos (como el nombre del archivo o sus permisos).
*   **Trees (Árboles):** Representan la estructura de directorios y otorgan contexto. Un objeto *Tree* asocia los nombres de los archivos y sus permisos de acceso con los hashes de los *Blobs* correspondientes, o con otros *Trees* si existen subdirectorios, reconstruyendo así la jerarquía completa del sistema de archivos.
*   **Commits (Unidades de Historial):** Consolidan un punto específico en la línea de tiempo. Cada objeto Commit vincula un Tree raíz (que representa el estado total del proyecto en ese momento exacto) con los metadatos de autoría (quién hizo el cambio, cuándo y el mensaje) y con el hash del commit o los commits antecesores.

**Relación estructural (Snapshot):**
Para conformar la instantánea, estos objetos se relacionan de forma estrictamente jerárquica: el Commit apunta a un Tree raíz; este Tree mapea la estructura de carpetas apuntando a otros Trees o directamente a los Blobs que contienen la información. Juntos, congelan el estado exacto de todo el repositorio conformando una unidad inmutable.

#### 2. Direccionamiento por contenido

En la arquitectura de Git, el identificador de un archivo deja de ser su nombre o ruta para convertirse en una "huella digital" (Hash SHA-256) calculada estrictamente a partir de sus datos. Por este motivo, se afirma que la dirección de un archivo en la base de datos es su contenido mismo: es la propia información interna del archivo la que, al pasar por el algoritmo criptográfico, genera el identificador único que Git utiliza para almacenarlo y recuperarlo.

La importancia del Hash (SHA-256) radica en dos pilares fundamentales para el control de versiones:
*   **Integridad del historial:** garantiza que los datos sean inmutables. Cualquier intento de alteración en el contenido, por mínimo que sea, cambiaría totalmente su hash y, por lo tanto, su dirección lógica. Esto hace que el historial sea auditable y virtualmente imposible de falsificar sin romper la cadena completa.
*   **Deduplicación de datos:** Si el contenido de un archivo no varía entre distintas versiones o confirmaciones, el hash es idéntico. Esta característica permite que Git reutilice el mismo objeto físico (Blob) en el disco para múltiples momentos, optimizando el espacio de almacenamiento.

#### 3. El grafo dirigido acíclico (DAG)

En Git, el historial de versiones no es una simple lista lineal, sino que se estructura matemáticamente como un grafo dirigido acíclico (DAG). En este grafo, cada nodo (commit) apunta de forma unidireccional a su antecesor, incluyendo el hash SHA-256 del commit previo dentro de sus propios metadatos.

Si se realizara una alteración mínima en un archivo de un commit del pasado, se desencadenaría un efecto estructural:
1. Al cambiar el contenido del archivo, su hash (Blob) cambia radicalmente.
2. Esto modifica el contenido del directorio (Tree) que lo contiene, cambiando también su hash.
3. En consecuencia, el hash del propio Commit cambia por completo al apuntar a un nuevo Tree.

Al modificarse el identificador (hash) de este commit pasado, el commit sucesor queda desconectado. Para que el historial siga teniendo sentido, Git se vería obligado a actualizar el enlace en el commit sucesor, lo que cambiaría su contenido y, por ende, generaría un nuevo hash, invalidando y reescribiendo toda la cadena de commits sucesores. 

Este diseño actúa como una estricta cadena de custodia criptográfica: garantiza que es imposible falsificar, alterar o corromper una versión antigua sin que todo el historial posterior lo evidencie y deba ser regenerado.


### Parte 2: Áreas de trabajo y flujo atómico

#### 4. Las tres areas y la secuencia de ejecución

El ciclo de vida de una modificación en Git atraviesa distintas áreas lógicas antes de consolidarse. Al ejecutar la secuencia de comandos `git add` seguida de `git commit`, ocurre el siguiente proceso:

**A. Ejecución de `git add` (Interacción con el Staging Area):**
Cuando se ejecuta `git add` sobre un archivo del *Working Directory*, Git lee su contenido, calcula su Hash SHA-256 y lo guarda físicamente como un objeto *Blob* dentro de la base de datos (`.git/objects`). Luego, actualiza el *Staging Area*, registrando que el nombre de ese archivo ahora apunta al nuevo hash calculado. 
El *Staging Area* actúa como un archivo técnico de borrador; es la zona de preparación donde se definen y aislan qué cambios específicos están "listos para la foto".

**B. Ejecución de `git commit` (Consolidación en el Repository):**
Al invocar `git commit`, Git toma el estado exacto que dejamos preparado en el *Staging Area* y crea un objeto *Tree* que mapea esa estructura. Luego, genera un objeto *Commit* que apunta a ese nuevo *Tree*, adjunta los metadatos (autor, fecha, mensaje) y lo enlaza con el commit predecesor. 
Finalmente, la información pasa a residir de manera permanente en el *Repository* (.git), integrándose a la base de datos inmutable, y la referencia de la rama actual avanza para apuntar al hash de este flamante commit.

#### 5. El rol de HEAD y el estado Detached

HEAD es un puntero que indica en qué parte exacta del grafo de commits (DAG) está posicionado el directorio de trabajo actual. HEAD no apunta directamente a un commit, sino a la referencia de la rama activa (por ejemplo, `main`), la cual a su vez apunta al commit más reciente. De esta forma, al realizar un nuevo commit, la rama avanza y HEAD se mueve automáticamente con ella.

**El estado Detached HEAD:**
Se produce cuando se ordena a Git que mueva el puntero HEAD para que deje de rastrear una rama y apunte directamente al hash criptográfico de un commit específico en el pasado (por ejemplo, mediante `git checkout <hash>`). 

**Utilidad para la resiliencia técnica:**
Trabajar con un HEAD despegado es una técnica esencial para la resiliencia del software. Permite viajar en el tiempo para compilar, auditar o ejecutar el sistema exactamente como existía en ese punto del pasado, todo ello en un entorno aislado y seguro, sin alterar ni destruir el historial de la rama actual. Si se detecta código útil en ese punto antiguo, Git permite crear una rama nueva directamente desde ese estado detached, guardando la integridad del repositorio principal.


### Parte 3: Gestión y cirugía del historial

#### 6. Limpieza de historial

Para unificar 5 commits locales con mensajes temporales ("fix 1", "test", etc.) en un solo commit profesional, se recomienda usar el Rebase Interactivo apuntando a los últimos 5 commits:
`git rebase -i HEAD~5`

Al ejecutar este comando, Git abre un editor interactivo con la lista de esos commits. Para unirlos, se debe aplicar el comando Squash a los últimos 4 commits, lo que le indica a Git que los combine entro del primer commit más antiguo de esa lista. Finalmente, el editor permitirá redactar un único mensaje consolidado que explique la funcionalidad completa.

**Diferencia técnica entre `amend` y `rebase interactivo`:**
*   **`git commit --amend` (Corrección Inmediata):** Su alcance está limitado a modificar el último commit realizado. No edita el commit, sino que crea uno nuevo reemplazando al anterior en la punta de la rama. Es la herramienta adecuada para arreglar un error de tipeo en el último mensaje o adjuntar un archivo olvidado en el Staging Area.
*   **`git rebase -i` (Cirugía Estética):** Es una herramienta que permite transformar una serie histórica de múltiples commits. A diferencia de `amend`, el rebase interactivo permite eliminar o reescribir los mensajes de cualquier cantidad de commits del pasado antes de enviarlos al repositorio remoto.


#### 7. Manipulación quirúrgica: Cherry-pick vs. Merge

Se recomienda utilizar `git cherry-pick` en lugar de un `merge` convencional cuando se necesita extraer e integrar un cambio muy específico (un commit o un conjunto reducido de commits) desde otra rama, sin arrastrar todo el historial de desarrollo. 

Mientras que un `merge` fusiona dos líneas de tiempo completas, el `cherry-pick` funciona como una herramienta de precisión quirúrgica para la manipulación de cambios, evaluando si el Tree de origen es compatible para traer un commit suelto sin romper las dependencias.

**Ejemplo de aplicación (Escenario de Hotfix):**
Situacion: que un desarrollador está trabajando en una rama `feature/nueva-interfaz` que tardará semanas en terminarse. Durante ese trabajo, descubre y soluciona un error crítico (un bug) que actualmente está afectando a los usuarios en la rama de producción (`main`). 
Si el desarrollador hiciera un `merge` de su rama `feature` hacia `main` para aplicar la solución, arrastraría toda la interfaz a medio terminar, rompiendo el sistema en producción. La alternativa segura es crear una rama temporal `hotfix` (o posicionarse en `main`) y ejecutar `git cherry-pick <hash-del-arreglo>`. Esto aplica únicamente el parche crítico (hotfix) en producción, sin comprometer el proyecto y permitiendo que la rama `feature` original continúe su desarrollo.


### Parte 4: Casos prácticos de resiliencia

#### 8. Escenario de desastre

Situacion: Un desarrollador ejecutó por error git reset --hard HEAD~1 y borró una tarde entera
de trabajo. El commit no aparece en el git log.

A- ¿Está realmente perdido el trabajo?
No, el trabajo no está definitivamente perdido. Al ejecutar un `git reset --hard HEAD~1`, el desarrollador solo ordenó que el puntero de la rama actual y el directorio de trabajo retrocedieran un paso, haciendo que el último commit "desaparezca" de la vista de la rama. Sin embargo, los objetos físicos de ese trabajo borrado (Commits, Trees y Blobs) quedan como "huérfanos" pero permanecen intactos en la base de datos oculta (`.git/objects`) hasta que Git ejecuta rutinariamente su recolector de basura (*Garbage Collector*).

B- Procedimiento paso a paso utilizando `git reflog`:
1. Diagnóstico: Se debe ejecutar el comando `git reflog` en la terminal.
2. Localización del Hash: En la lista resultante, se debe buscar la línea anterior a la ejecución del reset. Allí aparecerá registrado el movimiento y el hash SHA-256 corto del commit "perdido" (por ejemplo, identificándolo bajo una etiqueta como `HEAD@{1}: commit: [mensaje del trabajo perdido]`).
3. Restauración: Una vez identificado el hash (ej. `a1b2c3d`), existen dos vías:
   * Opción segura: Crear una rama nueva exactamente en ese punto de la historia ejecutando `git branch rescate a1b2c3d`.
   * Opción directa: Forzar a la rama actual a viajar de nuevo hacia el futuro apuntando a ese commit con `git reset --hard a1b2c3d`.

#### 9. Reset vs. Revert

Situacion: El equipo ha detectado un error en un commit que ya fue enviado al repositorio
remoto (push).

¿Por qué es una mala práctica usar `git reset` en este caso?
`reset` altera el Grafo Dirigido Acíclico (DAG) retrocediendo el puntero de la rama y borrando los commits de la línea de tiempo oficial. Si otros desarrolladores ya descargaron (pull) ese código y basaron su trabajo en él, al reescribir el pasado se destruye la sincronización del equipo, generando inconsistencias estructurales al momento de intentar integrar nuevos cambios.

La alternativa correcta y profesional es utilizar el comando `git revert <hash>`. 
A diferencia de `reset`, `revert` respeta la inmutabilidad de la base de datos de Git. Funciona analizando los cambios introducidos en el commit defectuoso y generando un nuevo objeto Commit que contiene exactamente las modificaciones inversas (el código opuesto) al commit original. De esta forma, el error se deshace funcionalmente, pero el historial avanza de forma segura, dejando un registro de que hubo un error y fue corregido de manera controlada. Este nuevo commit puede ser enviado al remoto (push) sin romper el entorno de ningún otro desarrollador.

### Parte 5: Diagnóstico y auditoría

#### 10. Comandos de Bajo Nivel (Plumbing)

Para realizar auditorías o diagnósticos profundos sin alterar el estado del directorio de trabajo, se utilizan los siguientes comandos:

*   Para verificar el tipo de objeto tras un hash:
    Se debe utilizar el comando `git cat-file -t <hash>` (la bandera `-t` hace referencia a *type*). Al ejecutarlo, Git analizará la base de datos y devolverá explícitamente el tipo de la estructura criptográfica correspondiente a ese identificador, es decir, si se trata de un `blob`, un `tree`, un `commit` o un `tag`.

*   Para visualizar el contenido puro de un tree o un blob:
    Se debe utilizar el comando `git cat-file -p <hash>` (la bandera `-p` hace referencia a *pretty-print* o formato legible). Este comando extrae y decodifica la información de la base de datos: si el hash pertenece a un objeto *Tree*, mostrará por consola la estructura jerárquica y la lista de archivos que contiene; si pertenece a un objeto *Blob*, imprimirá en pantalla el código puro o texto exacto del archivo, permitiendo recuperar contenido incluso si el archivo original fue borrado del directorio de trabajo y no se recuerda su nombre.