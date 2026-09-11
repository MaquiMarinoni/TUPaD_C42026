package com.gestion.pedidos.service;

import com.gestion.pedidos.dto.usuario.UsuarioCreate;
import com.gestion.pedidos.dto.usuario.UsuarioEdit;
import com.gestion.pedidos.dto.usuario.UsuarioDto;

import java.util.List;

public interface UsuarioService {

    UsuarioDto crearUsuario(UsuarioCreate dto);

    UsuarioDto obtenerUsuarioPorId(Long id);
    
    UsuarioDto obtenerUsuarioPorMail(String mail);

    List<UsuarioDto> listarUsuarios();

    UsuarioDto actualizarUsuario(Long id, UsuarioEdit dto);

    void eliminarUsuario(Long id);
}