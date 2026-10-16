<div align="center">

## Unidad 05 - Práctica 1
# Elicitación de Requerimientos

<br><br><br>

**Comisión 15**  
**Marinoni, Macarena** <marinonimacarena@gmail.com>  
Tecnicatura Universitaria en Programación - Universidad Tecnológica Nacional  
Metodología de Sistemas II  
Profesor: Videla, Flavia  
Tutor: Lobos, Diego  
15/10/2026  

</div>

<div style="page-break-after: always;"></div>

## ÍNDICE

- [Elicitación de Requerimientos](#elicitación-de-requerimientos)
  - [ÍNDICE](#índice)
  - [Introducción](#introducción)
    - [Parte 1: Identificación de stakeholders](#parte-1-identificación-de-stakeholders)
    - [Parte 2: Entrevista Estructurada](#parte-2-entrevista-estructurada)
      - [1. Situación Actual](#1-situación-actual)
      - [2. Funcionalidad Requerida](#2-funcionalidad-requerida)
      - [3. Notificaciones del Sistema](#3-notificaciones-del-sistema)
    - [Parte 3: Análisis competitivo](#parte-3-análisis-competitivo)
    - [Parte 4: Análisis de Documentación](#parte-4-análisis-de-documentación)
    - [Parte 5: Perfiles de Usuario (User Personas)](#parte-5-perfiles-de-usuario-user-personas)
      - [Perfil 1: Cliente Digital](#perfil-1-cliente-digital)
      - [Perfil 2: Cliente Tradicional](#perfil-2-cliente-tradicional)
    - [Parte 6: Verificación de Requisitos](#parte-6-verificación-de-requisitos)
      - [Actor: Cliente](#actor-cliente)
      - [Actor: Administrador de Tienda (Dueño del Negocio)](#actor-administrador-de-tienda-dueño-del-negocio)
    - [Parte 7: Casos de uso](#parte-7-casos-de-uso)

<div style="page-break-after: always;"></div>

## Introducción

El presente informe aborda la fase fundamental del ciclo de vida del software: la elicitación y especificación de requerimientos para el desarrollo de la plataforma de comercio electrónico del emprendimiento mendocino "Sabores de Cuyo".

Mediante la aplicación de técnicas de elicitación se busca transformar la visión del negocio en una base de especificaciones formales, verificables y trazables, mitigando la deuda técnica y garantizando la viabilidad del producto final.

### Parte 1: Identificación de stakeholders

A continuación, se detalla la matriz de stakeholders para "Sabores de Cuyo":

| **Categoría** | **Stakeholder** | **Rol en el Sistema** | **Interés / Necesidad Principal** |
| :--- | :--- | :--- | :--- |
| **Usuarios Directos** | Clientes finales (consumidores) | Comprador online | Explorar el catálogo regional, verificar stock disponible en tiempo real, efectuar compras de forma segura y realizar el seguimiento logístico de sus envíos a nivel nacional. |
| **Usuarios Directos** | Dueño del negocio ("Sabores de Cuyo") | Administrador general y gestor comercial | Centralizar pedidos, automatizar el flujo de cobros, mantener actualizadas listas de precios/stock y minimizar el retrabajo de atención manual por canales informales. |
| **Usuarios Indirectos** | Personal de empaque y logística interna | Operador de despacho y embalaje | Acceder en tiempo real al detalle de pedidos confirmados para preparar empaques especiales y emitir etiquetas de despacho estandarizadas. |
| **Product Champions** | Community manager / Encargado de marketing | Administrador de promociones y fidelización | Gestionar cupones promocionales, publicar productos destacados por temporada y automatizar el canal de novedades a suscriptores. |
| **Proveedores / Integradores** | Operador Logístico (ej. Andreani / Correo Argentino) | Servicio externo de distribución | Consumir datos normalizados de destino, peso y volumetría de bultos para tarificación dinámica de fletes y emisión bidireccional del código de seguimiento (tracking). |
| **Proveedores / Integradores** | Pasarela de Pagos | Procesador transaccional financiero | Proveer una infraestructura de cobro segura, procesar validaciones y notificar el cambio de estado de transacciones (aprobada/rechazada). |
| **Consejeros / Reguladores** | Contador externo / Organismo fiscal (AFIP/ARCA) | Auditor contable y fiscal | Garantizar la emisión automatizada y trazable de facturación electrónica conforme a normativas impositivas vigentes y la conciliación contable de ingresos. |


### Parte 2: Entrevista Estructurada

**Contexto:** Registro realizado por el Analista de Sistemas al Dueño del emprendimiento "Sabores de Cuyo".

#### 1. Situación Actual

* **Pregunta 1: ¿Cómo vende sus productos actualmente y qué problemas enfrenta?**
  * Respuesta del entrevistado:
    > *"Actualmente comercializamos mediante venta directa en nuestro local físico en Mendoza y a través de conversaciones por WhatsApp e Instagram. El principal problema es el cuello de botella operativo: la atención es completamente manual. Perdemos aproximadamente un 30% de consultas porque no logramos responder a tiempo en horarios pico. Además, se generan errores recurrentes de stock (vendemos productos que ya no quedan) y los pagos por transferencia exige revisar comprobantes uno a uno, lo que retrasa el envio del paquete."*

* **Pregunta 2: ¿Cuántos pedidos recibe por mes? ¿Por qué canales?**
  * Respuesta del entrevistado:
    > *"Estamos procesando un promedio de entre 120 y 150 pedidos mensuales. El 70% ingresa por WhatsApp, un 20% mediante mensajes directos de Instagram y el 10% restante corresponde a clientes que llaman por teléfono o nos contactan por correo. Todo el registro se lleva en planillas de excel compartidas, lo que se vuelve dificil para escalar."*


#### 2. Funcionalidad Requerida

* **Pregunta 3: ¿Cuáles son las funcionalidades principales que necesita?**

  * [x] Catálogo de productos con fotos de alta resolución y ficha técnica. *
  * [x] Carrito de compras con actualización dinámica de subtotales y costos de envío.
  * [x] Gestión de pagos online integrada.
  * [x] Seguimiento de envíos (Tracking en tiempo real).
  * [x] Control automatizado de stock.
  * [x] Sistema de promociones y cupones de descuento.
  * Otras: 
    > *Módulo de impresión de etiquetas de despacho con rotulado especial para mercadería frágil (botellas de vidrio y conservas).*

* **Pregunta 4: ¿Qué métodos de pago y zonas de envío desea cubrir?**
  * Respuesta del entrevistado:
    > *"Necesitamos integración directa con Mercado Pago para pagos con tarjetas de crédito en cuotas, tarjetas de débito y dinero en cuenta, además de habilitar la opción de transferencia bancaria con verificación de acreditación. Respecto a la logística, el objetivo del lanzamiento es abarcar todo el territorio argentino mediante acuerdos de integración con empresas de paquetería nacional (como Andreani o Correo Argentino)."*


#### 3. Notificaciones del Sistema

* **Pregunta 5: ¿Qué eventos debe notificarle el sistema?**
  * Respuesta del entrevistado:
    > 1. *Notificación inmediata ante un nuevo pedido, enviando resumen de compra y la hoja de preparación a la zona de embalaje.*
    > 2. *Alerta de stock crítico/bajo (cuando un producto alcance un umbral mínimo configurable, ej. 5 unidades).*
    > 3. *Notificaciones al comprador vía correo electrónico y SMS/WhatsApp ante cada cambio de estado de su orden (pago aprobado, pedido en preparación, paquete despachado con número de tracking).*


### Parte 3: Análisis competitivo

*   Tienda 1: *Tienda Santa Julia / Zuccardi* (Mendoza - Vinos, Aceites de Oliva y Conservas).
*   Tienda 2: *Almacén 1249 / Tienda Regional Gourmet* (Productos regionales, dulces artesanales, frutos secos y fiambres).

| Aspecto Evaluado | Tienda 1 | Tienda 2 |
| :--- | :--- | :--- |
| **Funcionalidades destacadas** | • Fichas técnicas completas descargables (maridaje, notas de cata y origen geográfico).<br>• Selector de compra por caja cerrada (descuento por 6 unidades).<br>• Calculador de costo de flete por código postal en la misma página de producto.<br>• Verificación de mayoría de edad (+18 años) al ingresar al portal. | • Búsqueda por facetas y filtros combinados (aptitud celíaca, orgánicos, sin azúcar agregada).<br>• Paquetes prediseñados ("Kits de Regalo" / "Cajas Degustación").<br>• Botón flotante de WhatsApp para soporte en vivo y resolución de dudas sobre productos frágiles. |
| **Proceso de compra (simple / complejo)** | Simple y directo:<br>Permite comprar en modo "invitado" sin requerir registro previo obligatorio. El flujo es de 3 pasos: Carrito → Datos de entrega/facturación → Pago. | Moderadamente complejo:<br>Exige la creación de una cuenta de usuario con confirmación de correo antes de habilitar el botón de pago. |
| **Problemas identificados** | • No muestra el nivel de stock en tiempo real (solo indica disponibilidad general).<br>• No comunica la política de embalaje de seguridad frente a posibles roturas de botellas de vidrio durante el flete. | • El costo de envío se calcula recién en el último paso del proceso de pago, generando posible insatisfacción por cobros inesperados.<br>• Falta de claridad en los plazos de entrega diferenciados para el interior del país. |
| **Ideas a implementar en Sabores de Cuyo** | 1. Módulo "Armá tu caja mixta": Permitir al cliente combinar botellas de vino, frascos de dulces y frutos secos alcanzando el tope de bonificación de envío gratis.<br>2. Sello visible de "Garantía de Embalaje Seguro": Comunicar al comprador que las botellas viajan en cajas térmicas reforzadas contra impactos.<br>3. Cotizador dinámico de envíos por CP: Informar el costo exacto y la fecha estimada de entrega antes de ingresar a la pasarela de pago. |


### Parte 4: Análisis de Documentación

| ID | Requisito Identificado y Especificación | Documento Fuente | Tipo (F / NF) | Prioridad |
| :--- | :--- | :--- | :--- | :--- |
| **REQ-01** | Bonificación automática de costo de flete: El sistema debe calcular el subtotal del carrito y, si el importe neto es igual o superior a $25.000, establecer el costo de envío en $0, mostrando un banner de confirmación en la vista de checkout. | Doc 1 | Funcional | Alta |
| **REQ-02** | Diferenciación geográfica de plazos de entrega: El motor logístico debe calcular y mostrar el plazo estimado de recepción según el código postal: 3 a 5 días hábiles para CABA/GBA y 5 a 7 días hábiles para el resto del país. | Doc 1 | Funcional | Media |
| **REQ-03** | Gestión de cupón promocional de bienvenida: El sistema debe validar el código alfanumérico "BIENVENIDA" en el checkout, aplicando un 10% de descuento sobre el subtotal únicamente si el usuario ejecuta su primera orden de compra registrada. | Doc 1 | Funcional | Media |
| **REQ-04** | Gestión de devoluciones por fallas de calidad: El módulo de postventa debe permitir la apertura de reclamos por rotura o producto defectuoso dentro de una ventana temporal máxima de 7 días corridos posteriores a la entrega certificada. | Doc 1 | Funcional | Baja |
| **REQ-05** | Galería fotográfica y especificaciones técnicas: Cada ficha de producto debe exhibir un carrusel de fotografías de alta resolución junto con detalles de peso, volumen, graduación alcohólica (en vinos) e información de alérgenos/vencimiento. | Doc 2 | Funcional | Alta |
| **REQ-06** | Disponibilidad y stock en tiempo real: La interfaz de catálogo debe mostrar el inventario remanente exacto de cada ítem e inhabilitar el botón de agregado al carrito si el stock físico del SKU es igual a cero. | Doc 2 | Funcional | Alta |
| **REQ-07** | Módulo de suscripción a novedades y promociones: El sistema debe permitir la suscripción voluntaria del cliente mediante correo electrónico para recibir notificaciones sobre nuevos lanzamientos, lotes de temporada y descuentos especiales. | Doc 2 | Funcional | Baja |
| **REQ-08** | Generación de hojas de preparación y segregación de frágiles: Tras la confirmación del pago, el sistema debe emitir automáticamente el listado de empaque, alertando de forma visible si la orden contiene vinos para exigir empaque reforzado anti-impacto. | Doc 3 | Funcional | Alta |
| **REQ-09** | Integración de rotulado y seguimiento logístico (Tracking): El sistema debe generar la etiqueta normalizada de despacho con código de barras e interoperar vía API con el operador logístico para asignar un número de tracking único por envío. | Doc 3 | Funcional | Alta |
| **REQ-10** | Seguridad en transacciones y protección de datos: El procesamiento de pagos mediante pasarelas externas debe operar no almacenando datos sensibles de tarjetas en la base de datos local. | Doc 2 | No Funcional | Alta |


### Parte 5: Perfiles de Usuario (User Personas)

A continuación, se especifican los dos perfiles principales identificados para "Sabores de Cuyo":

#### Perfil 1: Cliente Digital 

* **Nombre y Datos Demográficos:** María Fernández, 35 años, CABA.
* **Ocupación / Contexto:** Diseñadora gráfica / Profesional independiente. Realiza compras online de forma semanal y valora la inmediatez.
* **Nivel Técnico:** Alto. Usuaria intensiva de billeteras virtuales, e-commerce y servicios bajo demanda.
* **Dispositivo Preferido:** Smartphone (Mobile: 70% / Desktop: 30%). Navega en momentos de descanso o durante traslados urbanos.
* **Objetivos Principales:**
  1. Localizar y comprar rápidamente productos gourmet específicos (vinos de autor y aceites de oliva premium) filtrando por varietal, precio o maridaje.
  2. Completar el proceso de compra (checkout) en menos de 3 clics mediante métodos de pago ágiles (Mercado Pago, Apple Pay/Google Pay o tarjetas guardadas), sin pasos burocráticos de registro previo.
* **Frustraciones:**
  * Procesos de compra extensos, formularios repetitivos o la obligación de crear una cuenta para poder abonar.
  * Falta de información de stock en tiempo real (descubrir que un ítem está agotado recién al intentar pagar).
  * Plataformas lentas, no responsivas o con costos de envío sorpresa que no se calculan de entrada.
* **Impacto en el Sistema:** Requiere un diseño *Mobile-First*, cotización inmediata de flete mediante ingreso de Código Postal en el carrito y soporte de flujo de compra en modo "invitado" (*guest checkout*).


#### Perfil 2: Cliente Tradicional

* **Nombre y Datos Demográficos:** Roberto Sánchez, 58 años, Córdoba Capital.
* **Ocupación / Contexto:** Contador público jubilado. Disfruta de la gastronomía regional y busca productos auténticos que no se consiguen en cadenas de supermercados locales.
* **Nivel Técnico:** Básico. Utiliza internet principalmente para consultas bancarias, noticias y correo electrónico; prefiere la simplicidad y la previsibilidad operativa.
* **Dispositivo Preferido:** Computadora de escritorio (Desktop / Notebook) con pantalla amplia y teclado físico.
* **Temores:**
  * Desconfianza frente a estafas digitales, clonación de tarjetas de crédito o cobros duplicados en plataformas desconocidas.
  * Miedo a equivocarse durante el proceso de pago o no saber cómo rectificar un producto cargado por error en el carrito.
  * Temor a que los productos de vidrio (botellas de vino y frascos de conservas) lleguen rotos por un mal manejo del transporte y no existan canales humanos para reclamar.
* **Necesidades Especiales:**
  * Interfaz visual con tipografía legible, contrastes accesibles y botones de acción claros (CTA) con etiquetas descriptivas (ej. "Ir a Pagar de Forma Segura").
  * Explicación explícita y transparente de las garantías de embalaje reforzado y políticas claras de devolución en caso de roturas.
  * Canales de asistencia humana visibles (número de teléfono o botón de contacto directo por WhatsApp) para resolver dudas antes de confirmar la transacción.
* **Impacto en el Sistema:** Requiere confirmaciones visuales paso a paso (miga de pan o *stepper* de compra), sellos de seguridad SSL visibles, emisión instantánea de comprobante de compra por email con número de tracking y botón flotante de soporte humano.


### Parte 6: Verificación de Requisitos

#### Actor: Cliente

1. **Tareas que quiere que realice el sistema:**
   * Navegar, buscar y filtrar productos del catálogo por categoría, rango de precios y sellos regionales (ej. vinos, aceites, dulces artesanales, conservas).
   * Gestionar los ítems del carrito de compras (agregar, modificar cantidades, eliminar productos y visualizar subtotales actualizados en tiempo real).
   * Calcular de forma anticipada el costo y plazo de entrega ingresando el código postal (CP) de destino.
   * Aplicar cupones de descuento (validación del código promocional "BIENVENIDA").
   * Procesar el pago electrónico seguro a través de la pasarela integrada (tarjetas de crédito en cuotas, débito o dinero en cuenta).
   * Gestionar la solicitud de cambios o devoluciones por rotura/producto defectuoso dentro del plazo de garantía (7 días).

2. **Información que consulta:**
   * Ficha técnica detallada de cada producto: fotos en alta resolución, descripción, maridaje, notas de cata, peso y dimensiones.
   * Disponibilidad de stock real en góndola/almacén antes de efectuar la compra.
   * Desglose claro de costos: subtotal, impuestos aplicables, descuento por cupón y tarifa final de envío.
   * Estado del envío y código de seguimiento logístico (número de tracking emitido por el correo).
   * Historial de pedidos realizados y comprobantes de facturación emitidos.

3. **Eventos que necesita que le informe el sistema:**
   * Confirmación inmediata de recepción de la orden y acreditación exitosa del pago.
   * Alerta o rechazo de pago si la pasarela no autorizó la operación, ofreciendo reintentar con otro medio.
   * Notificación de despacho logístico con enlace directo para el seguimiento del paquete (tracking en tiempo real).
   * Confirmación de entrega efectiva del producto en el domicilio seleccionado.
   * Avisos por email sobre novedades de productos de temporada, reposición de ítems agotados y promociones exclusivas (si se encuentra suscripto).

#### Actor: Administrador de Tienda (Dueño del Negocio)

1. **Tareas que quiere que realice el sistema:**
   * Administrar el catálogo de productos (crear, editar precios, cargar imágenes, modificar fichas técnicas y deshabilitar publicaciones).
   * Monitorear y actualizar el inventario físico (stock centralizado y descuento automático tras compra confirmada).
   * Gestionar cupones y reglas comerciales de promoción (ej. bonificación de flete en compras $\ge$ $25.000).
   * Emitir la hoja de empaque y preparación (*picking list*) para el operario de depósito, segregando ítems frágiles (botellas de vino y frascos de vidrio).
   * Generar e imprimir etiquetas normalizadas de despacho logístico vinculadas con la API de paquetería.
   * Emitir y registrar comprobantes de facturación fiscal electrónica homologados ante AFIP/ARCA.

2. **Información que consulta:**
   * Tablero de control (dashboard) con métricas de ventas diarias, semanales y mensuales.
   * Registro consolidado de pedidos clasificados por estado (pendiente de pago, pago aprobado, en preparación, despachado, entregado).
   * Reportes de niveles críticos de inventario (artículos por debajo del stock de seguridad).
   * Reporte de transacciones financieras y liquidaciones pendientes de la pasarela de pagos.
   * Tasa de conversión y efectividad en el uso de cupones de descuento.

3. **Eventos que necesita que le informe el sistema:**
   * Alerta inmediata ante el ingreso y acreditación de un nuevo pedido para iniciar el proceso de embalaje.
   * Alerta preventiva de stock crítico/bajo cuando un SKU alcance el umbral mínimo configurado (ej. 5 unidades) para gestionar la reposición con productores de la región.
   * Alerta por discrepancias o fallas en la sincronización con la API de logística o pasarela de pagos.
   * Notificación de apertura de reclamos por roturas o solicitudes de devolución ingresadas por clientes.


### Parte 7: Casos de uso

| ID | Caso de Uso | Actor Primario | Descripción Breve |
| :--- | :--- | :--- | :--- |
| **CU-01** | Buscar y filtrar productos del catálogo | Cliente | Localizar productos regionales mediante motor de búsqueda por texto predictivo y filtros combinados (categoría, rango de precios, maridaje y aptitud alimentaria). |
| **CU-02** | Administrar carrito y cotizar envío | Cliente | Agregar o modificar unidades de artículos, calcular el costo y plazo de entrega según el código postal ingresado y aplicar reglas automáticas de bonificación de flete ($ \ge \$25.000 $). |
| **CU-03** | Aplicar cupón de descuento | Cliente | Ingresar el código promocional "BIENVENIDA" en el flujo de compra para obtener un 10% de descuento sobre el subtotal, previa validación de que sea la primera compra del usuario. |
| **CU-04** | Procesar pago electrónico | Cliente / Pasarela de Pago | Confirmar los datos de facturación y efectuar el pago seguro (tarjeta de crédito, débito o transferencia) a través del checkout integrado de Mercado Pago. |
| **CU-05** | Consultar seguimiento de envío (Tracking) | Cliente / Operador Logístico | Visualizar el estado logístico del pedido en tiempo real mediante la sincronización del código de tracking provisto por la empresa de distribución. |
| **CU-06** | Gestionar catálogo de productos y stock | Administrador de Tienda | Crear, modificar o deshabilitar publicaciones de artículos, actualizar precios de venta, cargar fichas técnicas e imágenes, y fijar umbrales mínimos de stock crítico. |
| **CU-07** | Procesar despacho e imprimir rotulado logístico | Administrador de Tienda / Operador Logístico | Emitir la orden de preparación segregando mercadería frágil (vinos/conservas) y generar la etiqueta estandarizada de despacho con código de barras para el correo. |

