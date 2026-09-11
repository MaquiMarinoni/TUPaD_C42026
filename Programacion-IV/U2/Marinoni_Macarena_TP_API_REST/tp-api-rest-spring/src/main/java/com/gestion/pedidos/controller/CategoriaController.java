package com.gestion.pedidos.controller;

import com.gestion.pedidos.dto.categoria.CategoriaCreate;
import com.gestion.pedidos.dto.categoria.CategoriaDto;
import com.gestion.pedidos.dto.categoria.CategoriaEdit;
import com.gestion.pedidos.service.CategoriaService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/categorias")
@RequiredArgsConstructor
public class CategoriaController {

    private final CategoriaService categoriaService;

    @PostMapping
    public ResponseEntity<CategoriaDto> crearCategoria(
            @RequestBody CategoriaCreate dto) {

        CategoriaDto categoria = categoriaService.crearCategoria(dto);

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(categoria);
    }

    @GetMapping
    public ResponseEntity<List<CategoriaDto>> listarCategorias() {
        return ResponseEntity.ok(
                categoriaService.listarCategorias()
        );
    }

    @GetMapping("/{id}")
    public ResponseEntity<CategoriaDto> obtenerCategoriaPorId(
            @PathVariable Long id) {

        return ResponseEntity.ok(
                categoriaService.obtenerCategoriaPorId(id)
        );
    }

    @PutMapping("/{id}")
    public ResponseEntity<CategoriaDto> actualizarCategoria(
            @PathVariable Long id,
            @RequestBody CategoriaEdit dto) {

        return ResponseEntity.ok(
                categoriaService.actualizarCategoria(id, dto)
        );
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminarCategoria(
            @PathVariable Long id) {

        categoriaService.eliminarCategoria(id);

        return ResponseEntity.noContent().build();
    }
}