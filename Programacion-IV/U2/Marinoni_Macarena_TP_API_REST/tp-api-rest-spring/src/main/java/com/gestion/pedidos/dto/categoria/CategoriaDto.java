package com.gestion.pedidos.dto.categoria;

import com.gestion.pedidos.entity.Categoria;

public record CategoriaDto(
        Long id,
        String nombre,
        String descripcion
) {
    public static CategoriaDto fromEntity(Categoria categoria) {
        return new CategoriaDto(
                categoria.getId(),
                categoria.getNombre(),
                categoria.getDescripcion()
        );
    }
}
