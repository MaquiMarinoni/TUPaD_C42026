package com.gestion.pedidos.dto.detallepedido;

import com.gestion.pedidos.dto.producto.ProductoDto;
import com.gestion.pedidos.entity.DetallePedido;

public record DetallePedidoDto(
        Long id,
        Integer cantidad,
        Double subtotal,
        ProductoDto producto
) {
    public static DetallePedidoDto fromEntity(DetallePedido detalle) {
        return new DetallePedidoDto(
                detalle.getId(),
                detalle.getCantidad(),
                detalle.getSubtotal(),
                ProductoDto.fromEntity(detalle.getProducto())
        );
    }
}
