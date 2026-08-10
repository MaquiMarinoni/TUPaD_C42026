package com.example.demo.dto.pedido;

import java.time.LocalDate;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PedidoDto {
    private Long id;
    private LocalDate fecha;
    private Estado estado;
    private Double total;
    private FormaPago formaPago;
}