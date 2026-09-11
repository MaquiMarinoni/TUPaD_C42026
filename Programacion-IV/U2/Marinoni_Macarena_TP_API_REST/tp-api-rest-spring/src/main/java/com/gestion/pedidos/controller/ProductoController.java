package com.gestion.pedidos.controller;

import com.gestion.pedidos.dto.producto.ProductoCreate;
import com.gestion.pedidos.dto.producto.ProductoDto;
import com.gestion.pedidos.dto.producto.ProductoEdit;
import com.gestion.pedidos.service.ProductoService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import jakarta.validation.Valid;


import java.util.List;

@RestController
@RequestMapping("/api/productos")
@RequiredArgsConstructor
public class ProductoController {

    private final ProductoService productoService;

    @PostMapping
    public ResponseEntity<ProductoDto> crearProducto(
           @Valid @RequestBody ProductoCreate dto) {

        ProductoDto producto = productoService.crearProducto(dto);

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(producto);
    }

    @GetMapping
    public ResponseEntity<List<ProductoDto>> listarProductos() {
        return ResponseEntity.ok(
                productoService.listarProductos()
        );
    }

    @GetMapping("/{id}")
    public ResponseEntity<ProductoDto> obtenerProductoPorId(
            @PathVariable Long id) {

        return ResponseEntity.ok(
                productoService.obtenerProductoPorId(id)
        );
    }

    @PutMapping("/{id}")
    public ResponseEntity<ProductoDto> actualizarProducto(
            @PathVariable Long id,
            @RequestBody ProductoEdit dto) {

        return ResponseEntity.ok(
                productoService.actualizarProducto(id, dto)
        );
    }

    @PatchMapping("/{id}")
    public ResponseEntity<ProductoDto> actualizarProductoParcial(
            @PathVariable Long id,
            @RequestBody ProductoEdit dto) {

        return ResponseEntity.ok(
                productoService.actualizarProducto(id, dto)
        );
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminarProducto(
            @PathVariable Long id) {

        productoService.eliminarProducto(id);

        return ResponseEntity.noContent().build();
    }
}