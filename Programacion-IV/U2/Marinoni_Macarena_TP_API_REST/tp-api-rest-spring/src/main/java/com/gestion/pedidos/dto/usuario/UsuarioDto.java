package com.gestion.pedidos.dto.usuario;

import com.gestion.pedidos.entity.Usuario;

public record UsuarioDto(
        Long id,
        String nombre,
        String apellido,
        String email,
        String celular
) {
    public static UsuarioDto fromEntity(Usuario usuario) {
        return new UsuarioDto(
                usuario.getId(),
                usuario.getNombre(),
                usuario.getApellido(),
                usuario.getMail(),
                usuario.getCelular()
        );
    }
}
