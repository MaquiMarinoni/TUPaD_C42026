package com.gestion.pedidos.controller;

import com.gestion.pedidos.dto.pedido.PedidoCreate;
import com.gestion.pedidos.dto.pedido.PedidoDto;
import com.gestion.pedidos.service.PedidoService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/pedidos")
@RequiredArgsConstructor
public class PedidoController {

    private final PedidoService pedidoService;

    @PostMapping
    public ResponseEntity<PedidoDto> crearPedido(
            @RequestBody PedidoCreate dto) {

        PedidoDto pedido = pedidoService.crearPedido(dto);

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(pedido);
    }

    @GetMapping
    public ResponseEntity<List<PedidoDto>> listarPedidos() {
        return ResponseEntity.ok(
                pedidoService.listarPedidos()
        );
    }

    @GetMapping("/{id}")
    public ResponseEntity<PedidoDto> obtenerPedidoPorId(
            @PathVariable Long id) {

        return ResponseEntity.ok(
                pedidoService.obtenerPedidoPorId(id)
        );
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminarPedido(
            @PathVariable Long id) {

        pedidoService.eliminarPedido(id);

        return ResponseEntity.noContent().build();
    }
}