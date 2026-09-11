package com.gestion.pedidos.service;

import com.gestion.pedidos.dto.pedido.PedidoCreate;
import com.gestion.pedidos.dto.pedido.PedidoDto;
import com.gestion.pedidos.dto.pedido.PedidoEdit;
import com.gestion.pedidos.entity.*;
import com.gestion.pedidos.repository.PedidoRepository;
import com.gestion.pedidos.repository.ProductoRepository;
import com.gestion.pedidos.repository.UsuarioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;


import java.util.List;

@Service
@RequiredArgsConstructor
public class PedidoServiceImp implements PedidoService{

    private final PedidoRepository pedidoRepository;
    private final UsuarioRepository usuarioRepository;
    private final ProductoRepository productoRepository;

    @Transactional
    public PedidoDto crearPedido(PedidoCreate dto) {

        Usuario usuario = usuarioRepository.findById(dto.usuarioId())
                .orElseThrow(() -> new RuntimeException(
                        "Usuario no encontrado con id: " + dto.usuarioId()
                ));

        Pedido pedido = dto.toEntity();


        for (var detalleDto : dto.detalles()) {

            Producto producto = productoRepository.findById(detalleDto.productoId())
                    .orElseThrow(() -> new RuntimeException(
                            "Producto no encontrado con id: " + detalleDto.productoId()
                    ));

            validarStock(producto, detalleDto.cantidad());

            pedido.addDetallePedido(detalleDto.cantidad(), producto);

            descontarStock(producto, detalleDto.cantidad());
        }

        pedido.calcularTotal();

        Pedido guardado = pedidoRepository.save(pedido);
        usuario.addPedido(guardado);
        usuarioRepository.save(usuario);
        return PedidoDto.fromEntity(guardado);
    }

    private void validarStock(Producto producto, int cantidad) {
        if (producto.getStock() < cantidad) {
            throw new RuntimeException(
                    "Stock insuficiente para el producto: " + producto.getNombre()
            );
        }
    }

    private void descontarStock(Producto producto, int cantidad) {
        producto.setStock(producto.getStock() - cantidad);
    }

    @Transactional(readOnly = true)
    public PedidoDto obtenerPedidoPorId(Long id) {
        Pedido pedido = pedidoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Pedido no encontrado con id: " + id));
        return PedidoDto.fromEntity(pedido);
    }

    @Transactional(readOnly = true)
    public List<PedidoDto> listarPedidos() {
        return pedidoRepository.findAll().stream()
                .map(PedidoDto::fromEntity)
                .toList();
    }
    @Override
    @Transactional
    public PedidoDto editarPedido(Long id, PedidoEdit dto) {
        Pedido pedido = pedidoRepository.findById(id)
            .orElseThrow(() -> new RuntimeException(
                    "Pedido no encontrado con id: " + id
            ));

        pedido.setEstado(dto.estado());
        pedido.setFormaPago(dto.formaPago());

        Pedido actualizado = pedidoRepository.save(pedido);

        return PedidoDto.fromEntity(actualizado);
    }

    @Override
    public void eliminarPedido(Long id) {
        Pedido pedido = pedidoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Pedido no encontrada con id: " + id));

        pedido.setEliminado(Boolean.TRUE);
        pedidoRepository.save(pedido);
    }


}
