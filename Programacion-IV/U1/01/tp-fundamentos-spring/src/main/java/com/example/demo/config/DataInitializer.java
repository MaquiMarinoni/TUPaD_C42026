package com.example.demo.config;

import com.example.demo.service.DataService;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer implements CommandLineRunner {

    private final DataService dataService;

    public DataInitializer(DataService dataService) {
        this.dataService = dataService;
    }

    @Override
    public void run(String... args) throws Exception {
        System.out.println("--- INICIANDO SISTEMA DE GESTIÓN DE PEDIDOS ---");
        dataService.inicializarDatosDelTP();
        System.out.println("--- CARGA FINALIZADA ---");
    }
}