package com.example.demo.dto.detallePedido;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DetallePedidoCreate {
    private int cantidad;
    private Double subtotal;
}