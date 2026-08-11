package com.example.demo.config;

import com.example.demo.service.DataService;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component // Estereotipo de propósito general para que Spring gestione esta clase
public class DataInitializer implements CommandLineRunner {

    private final DataService dataService;

    // INYECCIÓN DE DEPENDENCIAS POR CONSTRUCTOR
    // Spring inyecta automáticamente el DataService aquí al arrancar
    public DataInitializer(DataService dataService) {
        this.dataService = dataService;
    }

    @Override
    public void run(String... args) throws Exception {
        System.out.println("Iniciando la carga de datos...");
        dataService.imprimirMensaje();
    }
}