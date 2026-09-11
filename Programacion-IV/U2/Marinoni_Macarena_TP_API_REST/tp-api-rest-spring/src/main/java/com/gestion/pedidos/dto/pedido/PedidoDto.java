package com.gestion.pedidos.dto.pedido;

import com.gestion.pedidos.dto.detallepedido.DetallePedidoDto;
import com.gestion.pedidos.entity.Pedido;
import com.gestion.pedidos.enums.EstadoPedido;

import java.time.LocalDate;
import java.util.List;

public record PedidoDto(
        Long id,
        LocalDate fecha,
        EstadoPedido estado,
        Double total,
        List<DetallePedidoDto> detalles
) {
    public static PedidoDto fromEntity(Pedido pedido) {
        return new PedidoDto(
                pedido.getId(),
                pedido.getFecha(),
                pedido.getEstado(),
                pedido.getTotal(),
                pedido.getDetalles().stream()
                        .map(DetallePedidoDto::fromEntity)
                        .toList()
        );
    }
}
