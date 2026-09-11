package com.gestion.pedidos.dto.pedido;

import com.gestion.pedidos.enums.EstadoPedido;
import com.gestion.pedidos.enums.FormaPago;

public record PedidoEdit(
        EstadoPedido estado,
        FormaPago formaPago
) {
}