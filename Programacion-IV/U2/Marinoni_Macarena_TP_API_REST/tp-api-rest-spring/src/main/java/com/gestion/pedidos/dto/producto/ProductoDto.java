package com.gestion.pedidos.dto.producto;


import com.gestion.pedidos.entity.Producto;



public record ProductoDto(
        Long id,
        String nombre,
        String descripcion,
        Double precio,
        Integer stock
) {
    public static ProductoDto fromEntity(Producto producto) {
        return new ProductoDto(
                producto.getId(),
                producto.getNombre(),
                producto.getDescripcion(),
                producto.getPrecio(),
                producto.getStock()
        );
    }
}
