package com.gestion.pedidos.dto.categoria;

import com.gestion.pedidos.entity.Categoria;

public record CategoriaCreate(
        String nombre,
        String descripcion
) {
    public Categoria toEntity() {
        return Categoria.builder()
                .nombre(nombre)
                .descripcion(descripcion)
                .build();
    }
}
