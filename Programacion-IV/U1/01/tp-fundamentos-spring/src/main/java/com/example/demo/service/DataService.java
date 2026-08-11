package com.example.demo.service;

import org.springframework.stereotype.Service;

@Service // Estereotipo que indica que esta clase maneja lógica de negocio
public class DataService {

    // Aquí adentro guardaremos nuestras listas de Usuarios, Productos, etc.
    public void imprimirMensaje() {
        System.out.println("El DataService ha sido inyectado correctamente");
    }
}