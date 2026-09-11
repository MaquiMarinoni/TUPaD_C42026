package com.gestion.pedidos.controller;

import com.gestion.pedidos.dto.usuario.UsuarioCreate;
import com.gestion.pedidos.dto.usuario.UsuarioDto;
import com.gestion.pedidos.dto.usuario.UsuarioEdit;
import com.gestion.pedidos.service.UsuarioService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/usuarios")
@RequiredArgsConstructor
public class UsuarioController {

    private final UsuarioService usuarioService;

    @PostMapping
    public ResponseEntity<UsuarioDto> crearUsuario(
            @RequestBody UsuarioCreate dto) {

        UsuarioDto usuario = usuarioService.crearUsuario(dto);

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(usuario);
    }

    @GetMapping
    public ResponseEntity<List<UsuarioDto>> listarUsuarios() {
        return ResponseEntity.ok(
                usuarioService.listarUsuarios()
        );
    }

    @GetMapping("/{id}")
    public ResponseEntity<UsuarioDto> obtenerUsuarioPorId(
            @PathVariable Long id) {

        return ResponseEntity.ok(
                usuarioService.obtenerUsuarioPorId(id)
        );
    }

    @GetMapping("/mail")
    public ResponseEntity<UsuarioDto> obtenerUsuarioPorMail(
            @RequestParam String mail) {

        return ResponseEntity.ok(
                usuarioService.obtenerUsuarioPorMail(mail)
        );
    }

    @PutMapping("/{id}")
    public ResponseEntity<UsuarioDto> actualizarUsuario(
            @PathVariable Long id,
            @RequestBody UsuarioEdit dto) {

        return ResponseEntity.ok(
                usuarioService.actualizarUsuario(id, dto)
        );
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminarUsuario(
            @PathVariable Long id) {

        usuarioService.eliminarUsuario(id);

        return ResponseEntity.noContent().build();
    }
}
