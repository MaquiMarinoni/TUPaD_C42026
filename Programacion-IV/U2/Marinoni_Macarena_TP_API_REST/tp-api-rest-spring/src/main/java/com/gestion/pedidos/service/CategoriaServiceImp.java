package com.gestion.pedidos.service;

import com.gestion.pedidos.dto.categoria.CategoriaCreate;
import com.gestion.pedidos.dto.categoria.CategoriaEdit;
import com.gestion.pedidos.dto.categoria.CategoriaDto;
import com.gestion.pedidos.entity.Categoria;
import com.gestion.pedidos.repository.CategoriaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class CategoriaServiceImp implements CategoriaService{

    private final CategoriaRepository categoriaRepository;

    @Transactional
    public CategoriaDto crearCategoria(CategoriaCreate dto) {
        Categoria categoria = dto.toEntity();
        categoria = categoriaRepository.save(categoria);
        return CategoriaDto.fromEntity(categoria);
    }

    @Transactional(readOnly = true)
    public CategoriaDto obtenerCategoriaPorId(Long id) {
        Categoria categoria = categoriaRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Categoría no encontrada con id: " + id));
        return CategoriaDto.fromEntity(categoria);
    }

    @Transactional(readOnly = true)
    public List<CategoriaDto> listarCategorias() {
        return categoriaRepository.findAll().stream()
                .map(CategoriaDto::fromEntity)
                .toList();
    }

    @Transactional
    public CategoriaDto actualizarCategoria(Long id, CategoriaEdit dto) {
        Categoria categoria = categoriaRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Categoría no encontrada con id: " + id));

        dto.applyTo(categoria);
        categoriaRepository.save(categoria);
        return CategoriaDto.fromEntity(categoria);
    }

    @Transactional
    public void eliminarCategoria(Long id) {
        Categoria categoria = categoriaRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Categoría no encontrada con id: " + id));

        categoria.setEliminado(Boolean.TRUE);
        categoriaRepository.save(categoria);
    }
}
