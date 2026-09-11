package com.gestion.pedidos.service;

import com.gestion.pedidos.dto.categoria.CategoriaCreate;
import com.gestion.pedidos.dto.categoria.CategoriaEdit;
import com.gestion.pedidos.dto.categoria.CategoriaDto;

import java.util.List;

public interface CategoriaService {

    CategoriaDto crearCategoria(CategoriaCreate dto);

    CategoriaDto obtenerCategoriaPorId(Long id);

    List<CategoriaDto> listarCategorias();

    CategoriaDto actualizarCategoria(Long id, CategoriaEdit dto);

    void eliminarCategoria(Long id);
}