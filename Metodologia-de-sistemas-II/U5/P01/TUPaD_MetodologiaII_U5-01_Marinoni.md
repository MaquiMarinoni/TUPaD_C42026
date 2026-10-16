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

- [Introducción](#introducción)
- [Parte 1: Identificación de stakeholders](#parte-1-identificación-de-stakeholders)
- [Parte 2: Entrevista estructurada](#parte-2-entrevista-estructurada)
- [Parte 3: Análisis competitivo](#parte-3-análisis-competitivo)
- [Parte 4: Análisis de documentación](#parte-4-análisis-de-documentación)
- [Parte 5: Perfiles de usuario](#parte-5-perfiles-de-usuario)
- [Parte 6: Verificación de requisitos](#parte-6-verificación-de-requisitos)
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


