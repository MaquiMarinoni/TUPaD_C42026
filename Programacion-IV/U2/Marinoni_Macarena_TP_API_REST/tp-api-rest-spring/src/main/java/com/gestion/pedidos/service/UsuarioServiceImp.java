package com.gestion.pedidos.service;

import com.gestion.pedidos.dto.usuario.UsuarioCreate;
import com.gestion.pedidos.dto.usuario.UsuarioEdit;
import com.gestion.pedidos.dto.usuario.UsuarioDto;
import com.gestion.pedidos.entity.Usuario;
import com.gestion.pedidos.repository.UsuarioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class UsuarioServiceImp implements UsuarioService{

    private final UsuarioRepository usuarioRepository;

    @Transactional
    public UsuarioDto crearUsuario(UsuarioCreate dto) {
        Usuario usuario = dto.toEntity();
       usuario = usuarioRepository.save(usuario);
        return UsuarioDto.fromEntity(usuario);
    }

    @Transactional(readOnly = true)
    public UsuarioDto obtenerUsuarioPorId(Long id) {
        Usuario usuario = usuarioRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Usuario no encontrado con id: " + id));
        return UsuarioDto.fromEntity(usuario);
    }

    @Transactional(readOnly = true)
    public UsuarioDto obtenerUsuarioPorMail(String mail) {
        Usuario usuario = usuarioRepository.findByMail(mail)
                .orElseThrow(() -> new RuntimeException(
                    "Usuario no encontrado con mail: " + mail
            ));
        return UsuarioDto.fromEntity(usuario);
    }


    @Transactional(readOnly = true)
    public List<UsuarioDto> listarUsuarios() {
        return usuarioRepository.findAll().stream()
                .map(UsuarioDto::fromEntity)
                .toList();
    }

    @Transactional
    public UsuarioDto actualizarUsuario(Long id, UsuarioEdit dto) {
        Usuario usuario = usuarioRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Usuario no encontrado con id: " + id));
        
        dto.applyTo(usuario);
        usuarioRepository.save(usuario);

        return UsuarioDto.fromEntity(usuario);
    }

    @Transactional
    public void eliminarUsuario(Long id) {
        Usuario usuario = usuarioRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Usuario no encontrada con id: " + id));

        usuario.setEliminado(Boolean.TRUE);
        usuarioRepository.save(usuario);
    }
}
