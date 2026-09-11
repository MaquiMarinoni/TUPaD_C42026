package com.gestion.pedidos.service;

import com.gestion.pedidos.dto.pedido.PedidoCreate;
import com.gestion.pedidos.dto.pedido.PedidoDto;
import com.gestion.pedidos.dto.pedido.PedidoEdit;
import java.util.List;

public interface PedidoService {

    PedidoDto crearPedido(PedidoCreate dto);

    PedidoDto obtenerPedidoPorId(Long id);

    List<PedidoDto> listarPedidos();
    PedidoDto editarPedido(Long id, PedidoEdit dto);

    void eliminarPedido(Long id);
}