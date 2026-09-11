package com.gestion.pedidos.dto.pedido;

import com.gestion.pedidos.dto.detallepedido.DetallePedidoCreate;
import com.gestion.pedidos.entity.Pedido;
import com.gestion.pedidos.enums.FormaPago;

import java.util.List;

public record PedidoCreate(
        Long usuarioId,
        FormaPago formaPago,
        List<DetallePedidoCreate> detalles
) {
    public Pedido toEntity() {
        return Pedido.builder()
                .formaPago(formaPago)
                .build();
    }
}



