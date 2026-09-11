package com.gestion.pedidos;

import com.gestion.pedidos.dto.categoria.CategoriaCreate;
import com.gestion.pedidos.dto.detallepedido.DetallePedidoCreate;
import com.gestion.pedidos.dto.pedido.PedidoCreate;
import com.gestion.pedidos.dto.producto.ProductoCreate;
import com.gestion.pedidos.dto.usuario.UsuarioCreate;
import com.gestion.pedidos.enums.FormaPago;
import com.gestion.pedidos.service.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
// import org.springframework.stereotype.Component;

import java.util.List;

/*
 * DataLoader utilizado en el TP anterior para cargar datos automáticamente.
 *
 * En este TP se desactiva porque la consigna solicita crear y persistir
 * los usuarios, categorías, productos y pedidos utilizando Postman.
 *
 * Para volver a activarlo en el futuro:
 * 1. Descomentar el import de Component.
 * 2. Descomentar la anotación @Component.
 */

// @Component
@RequiredArgsConstructor
@Slf4j
public class DataLoader implements CommandLineRunner {

    private final CategoriaService categoriaService;
    private final ProductoService productoService;
    private final UsuarioService usuarioService;
    private final PedidoService pedidoService;

    @Override
    public void run(String... args) throws Exception {

        log.info("========== INICIANDO CARGA DE DATOS DE PRUEBA ==========");

        // 1. Crear 3 categorías
        log.info("Creando categorías...");

        var categoria1 = categoriaService.crearCategoria(
                new CategoriaCreate(
                        "Tecnología",
                        "Equipos y accesorios tecnológicos"
                )
        );

        var categoria2 = categoriaService.crearCategoria(
                new CategoriaCreate(
                        "Librería",
                        "Artículos escolares y de oficina"
                )
        );

        var categoria3 = categoriaService.crearCategoria(
                new CategoriaCreate(
                        "Hogar",
                        "Productos y accesorios para el hogar"
                )
        );

        log.info("✓ Categorías creadas: {}, {}, {}",
                categoria1.nombre(),
                categoria2.nombre(),
                categoria3.nombre());

        // 2. Crear 10 productos
        log.info("Creando productos...");

        var producto1 = productoService.crearProducto(
                new ProductoCreate(
                        "Auriculares Bluetooth",
                        "Auriculares inalámbricos",
                        45.50,
                        30,
                        categoria1.id()
                )
        );

        var producto2 = productoService.crearProducto(
                new ProductoCreate(
                        "Teclado Inalámbrico",
                        "Teclado compacto multidispositivo",
                        38.90,
                        25,
                        categoria1.id()
                )
        );

        var producto3 = productoService.crearProducto(
                new ProductoCreate(
                        "Mouse Inalámbrico",
                        "Mouse óptico inalámbrico",
                        22.75,
                        40,
                        categoria1.id()
                )
        );

        var producto4 = productoService.crearProducto(
                new ProductoCreate(
                        "Cuaderno Universitario",
                        "Cuaderno de 100 hojas",
                        6.50,
                        80,
                        categoria2.id()
                )
        );

        var producto5 = productoService.crearProducto(
                new ProductoCreate(
                        "Agenda",
                        "Agenda semanal tapa dura",
                        12.90,
                        35,
                        categoria2.id()
                )
        );

        var producto6 = productoService.crearProducto(
                new ProductoCreate(
                        "Set de Marcadores",
                        "Set de 12 marcadores de colores",
                        9.75,
                        50,
                        categoria2.id()
                )
        );

        var producto7 = productoService.crearProducto(
                new ProductoCreate(
                        "Lámpara de Escritorio",
                        "Lámpara LED regulable",
                        28.50,
                        20,
                        categoria3.id()
                )
        );

        var producto8 = productoService.crearProducto(
                new ProductoCreate(
                        "Organizador",
                        "Organizador plástico multiuso",
                        15.25,
                        45,
                        categoria3.id()
                )
        );

        var producto9 = productoService.crearProducto(
                new ProductoCreate(
                        "Botella Térmica",
                        "Botella térmica de acero inoxidable",
                        19.90,
                        30,
                        categoria3.id()
                )
        );

        var producto10 = productoService.crearProducto(
                new ProductoCreate(
                        "Taza",
                        "Taza de cerámica",
                        8.50,
                        60,
                        categoria3.id()
                )
        );

        log.info("✓ 10 productos creados exitosamente");

        // 3. Crear 2 usuarios
        log.info("Creando usuarios...");

        var usuario1 = usuarioService.crearUsuario(
                new UsuarioCreate(
                        "Lucía",
                        "Fernández",
                        "lucia.fernandez@email.com",
                        "342-555-1234",
                        "lucia123"
                )
        );

        var usuario2 = usuarioService.crearUsuario(
                new UsuarioCreate(
                        "Martín",
                        "Gómez",
                        "martin.gomez@email.com",
                        "342-555-5678",
                        "martin456"
                )
        );

        log.info("✓ Usuarios creados: {} {}, {} {}",
                usuario1.nombre(),
                usuario1.apellido(),
                usuario2.nombre(),
                usuario2.apellido());

        // 4. Crear 3 pedidos con al menos 2 detalles cada uno
        log.info("Creando pedidos...");

        var pedido1 = pedidoService.crearPedido(
                new PedidoCreate(
                        usuario1.id(),
                        FormaPago.EFECTIVO,
                        List.of(
                                new DetallePedidoCreate(1, producto1.id()),
                                new DetallePedidoCreate(2, producto4.id()),
                                new DetallePedidoCreate(1, producto6.id())
                        )
                )
        );

        log.info("✓ Pedido 1 creado - ID: {}, Total: ${}, Detalles: {}",
                pedido1.id(),
                pedido1.total(),
                pedido1.detalles().size());

        var pedido2 = pedidoService.crearPedido(
                new PedidoCreate(
                        usuario1.id(),
                        FormaPago.TARJETA,
                        List.of(
                                new DetallePedidoCreate(1, producto2.id()),
                                new DetallePedidoCreate(2, producto5.id())
                        )
                )
        );

        log.info("✓ Pedido 2 creado - ID: {}, Total: ${}, Detalles: {}",
                pedido2.id(),
                pedido2.total(),
                pedido2.detalles().size());

        var pedido3 = pedidoService.crearPedido(
                new PedidoCreate(
                        usuario2.id(),
                        FormaPago.TRANSFERENCIA,
                        List.of(
                                new DetallePedidoCreate(1, producto7.id()),
                                new DetallePedidoCreate(2, producto8.id()),
                                new DetallePedidoCreate(1, producto9.id())
                        )
                )
        );

        log.info("✓ Pedido 3 creado - ID: {}, Total: ${}, Detalles: {}",
                pedido3.id(),
                pedido3.total(),
                pedido3.detalles().size());

        log.info("========== CARGA DE DATOS COMPLETADA ==========");
        log.info("Resumen:");
        log.info("  - Categorías: 3");
        log.info("  - Productos: 10");
        log.info("  - Usuarios: 2");
        log.info("  - Pedidos: 3");
        log.info("================================================");
    }
}