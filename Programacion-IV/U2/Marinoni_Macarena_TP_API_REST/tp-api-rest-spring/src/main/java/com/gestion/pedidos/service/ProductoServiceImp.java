package com.gestion.pedidos.service;

import com.gestion.pedidos.dto.producto.ProductoCreate;
import com.gestion.pedidos.dto.producto.ProductoEdit;
import com.gestion.pedidos.dto.producto.ProductoDto;
import com.gestion.pedidos.entity.Categoria;
import com.gestion.pedidos.entity.Producto;
import com.gestion.pedidos.repository.CategoriaRepository;
import com.gestion.pedidos.repository.ProductoRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ProductoServiceImp implements ProductoService{

    private final ProductoRepository productoRepository;
    private final CategoriaRepository categoriaRepository;

    @Transactional
    public ProductoDto crearProducto(ProductoCreate dto) {
        Categoria categoria = categoriaRepository.findById(dto.categoriaId())
                .orElseThrow(() -> new RuntimeException("Categoría no encontrada con id: " + dto.categoriaId()));
        
        Producto producto = dto.toEntity();
        
        Producto guardado = productoRepository.save(producto);

        categoria.addProducto(producto);
        categoriaRepository.save(categoria);

        return ProductoDto.fromEntity(guardado);
    }

    @Transactional(readOnly = true)
    public ProductoDto obtenerProductoPorId(Long id) {
        Producto producto = productoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Producto no encontrado con id: " + id));
        return ProductoDto.fromEntity(producto);
    }

    @Transactional(readOnly = true)
    public List<ProductoDto> listarProductos() {
        return productoRepository.findAll().stream()
                .map(ProductoDto::fromEntity)
                .toList();
    }


    @Transactional
    public ProductoDto actualizarProducto(Long id, ProductoEdit dto) {
        Producto producto = productoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Producto no encontrado con id: " + id));
        
       dto.applyTo(producto);
        productoRepository.save(producto);
        return ProductoDto.fromEntity(producto);
    }

    @Transactional
    public void eliminarProducto(Long id) {
        Producto producto = productoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Producto no encontrada con id: " + id));

        producto.setEliminado(Boolean.TRUE);
        productoRepository.save(producto);
    }
}
