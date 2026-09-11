package com.gestion.pedidos.dto.usuario;

import com.gestion.pedidos.entity.Usuario;

public record UsuarioEdit(
        String nombre,
        String apellido,
        String email,
        String celular
) {
    public void applyTo(Usuario usuario) {
        if (this.nombre != null) {
            usuario.setNombre(this.nombre);
        }
        if (this.apellido != null) {
            usuario.setApellido(this.apellido);
        }
        if (this.email != null) {
            usuario.setMail(this.email);
        }
        if (this.celular != null) {
            usuario.setCelular(this.celular);
        }
    }
}