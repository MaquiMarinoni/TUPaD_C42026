package com.gestion.pedidos.dto.detallepedido;

public record DetallePedidoCreate(
        Integer cantidad,
        Long productoId
) {
}
