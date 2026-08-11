package com.example.demo.service;

import com.example.demo.dto.categoria.CategoriaDto;
import com.example.demo.dto.detallePedido.DetallePedidoDto;
import com.example.demo.dto.pedido.Estado;
import com.example.demo.dto.pedido.FormaPago;
import com.example.demo.dto.pedido.PedidoDto;
import com.example.demo.dto.producto.ProductoDto;
import com.example.demo.dto.usuario.Rol;
import com.example.demo.dto.usuario.UsuarioDto;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Service // Mantenemos el estereotipo de lógica de negocio
public class DataService {

    public void inicializarDatosDelTP() {
        // a) Instanciar 2 Usuarios
        UsuarioDto user1 = new UsuarioDto(1L, "Macarena", "Marinoni", "maca@mail.com", "123456", "pass123", Rol.ADMIN);
        UsuarioDto user2 = new UsuarioDto(2L, "Anto", "Gomez", "anto@mail.com", "654321", "pass456", Rol.USUARIO);

        // c) Instanciar 3 Categorías
        CategoriaDto cat1 = new CategoriaDto(1L, "Librería y Estudio", "Libros y cursos");
        CategoriaDto cat2 = new CategoriaDto(2L, "Mascotas", "Cuidado animal");
        CategoriaDto cat3 = new CategoriaDto(3L, "Tecnología", "Hardware y software");

        // d) Instanciar 10 Productos
        ProductoDto prod1 = new ProductoDto(1L, "Libro Pet Sematary", 15000.0, "Novela de Stephen King", 10, "img1.jpg", true);
        ProductoDto prod2 = new ProductoDto(2L, "Alimento Premium Felino", 25000.0, "Bolsa de 3kg", 15, "img2.jpg", true);
        ProductoDto prod3 = new ProductoDto(3L, "Set Mate y Bombilla de Acero", 18000.0, "Acero inoxidable", 20, "img3.jpg", true);
        ProductoDto prod4 = new ProductoDto(4L, "Monitor 27 pulgadas", 300000.0, "Monitor ideal para programar", 5, "img4.jpg", true);
        ProductoDto prod5 = new ProductoDto(5L, "Licencia MongoDB Atlas", 50000.0, "Suscripción anual", 100, "img5.jpg", true);
        ProductoDto prod6 = new ProductoDto(6L, "Curso Diseño UX/UI", 45000.0, "Formación completa", 50, "img6.jpg", true);
        ProductoDto prod7 = new ProductoDto(7L, "Camiseta Argentina", 80000.0, "Talle M", 30, "img7.jpg", true);
        ProductoDto prod8 = new ProductoDto(8L, "Entrada Recital", 35000.0, "Campo general", 200, "img8.jpg", true);
        ProductoDto prod9 = new ProductoDto(9L, "Pasaje Búzios", 450000.0, "Ida y vuelta", 10, "img9.jpg", true);
        ProductoDto prod10 = new ProductoDto(10L, "Juguete para gatos", 5000.0, "Ratón de tela", 40, "img10.jpg", true);

        // b) Instanciar 3 Pedidos (con al menos 2 detalles cada uno)
        PedidoDto pedido1 = new PedidoDto(1L, LocalDate.now(), Estado.CONFIRMADO, 40000.0, FormaPago.TARJETA);
        DetallePedidoDto det1_1 = new DetallePedidoDto(1, 15000.0); // 1 Libro
        DetallePedidoDto det1_2 = new DetallePedidoDto(1, 25000.0); // 1 Alimento

        PedidoDto pedido2 = new PedidoDto(2L, LocalDate.now(), Estado.PENDIENTE, 345000.0, FormaPago.TRANSFERENCIA);
        DetallePedidoDto det2_1 = new DetallePedidoDto(1, 300000.0); // 1 Monitor
        DetallePedidoDto det2_2 = new DetallePedidoDto(1, 45000.0);  // 1 Curso

        PedidoDto pedido3 = new PedidoDto(3L, LocalDate.now(), Estado.TERMINADO, 23000.0, FormaPago.EFECTIVO);
        DetallePedidoDto det3_1 = new DetallePedidoDto(1, 18000.0); // 1 Mate
        DetallePedidoDto det3_2 = new DetallePedidoDto(1, 5000.0);  // 1 Juguete

        System.out.println("¡Datos instanciados correctamente en el sistema!");
        System.out.println("Total usuarios: 2 | Total categorías: 3 | Total productos: 10 | Total pedidos: 3");
    }
}