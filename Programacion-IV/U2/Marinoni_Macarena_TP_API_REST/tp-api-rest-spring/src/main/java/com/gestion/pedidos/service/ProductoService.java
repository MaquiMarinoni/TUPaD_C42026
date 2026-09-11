package com.gestion.pedidos.service;

import com.gestion.pedidos.dto.producto.ProductoCreate;
import com.gestion.pedidos.dto.producto.ProductoEdit;
import com.gestion.pedidos.dto.producto.ProductoDto;

import java.util.List;

public interface ProductoService {

    ProductoDto crearProducto(ProductoCreate dto);

    ProductoDto obtenerProductoPorId(Long id);

    List<ProductoDto> listarProductos();

    ProductoDto actualizarProducto(Long id, ProductoEdit dto);

    void eliminarProducto(Long id);
}