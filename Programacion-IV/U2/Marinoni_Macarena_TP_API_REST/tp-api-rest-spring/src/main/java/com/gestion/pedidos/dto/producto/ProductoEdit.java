package com.gestion.pedidos.dto.producto;

import com.gestion.pedidos.entity.Producto;


public record ProductoEdit(
        String nombre,
        String descripcion,
        Double precio,
        Integer stock,
        String imagen
) {

    public void applyTo(Producto producto) {
        if (this.nombre != null) {
            producto.setNombre(this.nombre);
        }
        if (this.descripcion != null) {
            producto.setDescripcion(this.descripcion);
        }
        if (this.precio != null) {
            producto.setPrecio(this.precio);
        }
        if (this.stock != null) {
            producto.setStock(this.stock);
        }
        if (this.imagen != null) {
            producto.setImagen(this.imagen);
        }

    }
}