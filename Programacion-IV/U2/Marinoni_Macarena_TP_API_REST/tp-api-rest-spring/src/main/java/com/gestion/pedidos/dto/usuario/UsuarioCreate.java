package com.gestion.pedidos.dto.usuario;

import com.gestion.pedidos.entity.Usuario;

public record UsuarioCreate(
        String nombre,
        String apellido,
        String email,
        String celular,
        String contrasena
) {
    public Usuario toEntity() {
        return Usuario.builder()
                .nombre(nombre)
                .apellido(apellido)
                .mail(email)
                .celular(celular)
                .contraseña(contrasena)
                .build();
    }
}
