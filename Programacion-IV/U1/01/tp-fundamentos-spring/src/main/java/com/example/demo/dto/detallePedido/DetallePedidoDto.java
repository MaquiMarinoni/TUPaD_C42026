package com.example.demo.dto.detallePedido;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DetallePedidoDto {
    private int cantidad;
    private Double subtotal;
}