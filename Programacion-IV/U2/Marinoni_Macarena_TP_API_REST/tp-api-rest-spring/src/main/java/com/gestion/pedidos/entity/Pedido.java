package com.gestion.pedidos.entity;

import com.gestion.pedidos.enums.EstadoPedido;
import com.gestion.pedidos.enums.FormaPago;
import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Entity
@Table(name = "pedido")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@SuperBuilder
@EqualsAndHashCode(callSuper = false, onlyExplicitlyIncluded = true)
public class Pedido extends Base implements Calculable{


    @Column(nullable = false)
    @Builder.Default
    private LocalDate fecha = LocalDate.now() ;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    @Builder.Default
    private EstadoPedido estado = EstadoPedido.PENDIENTE;

    private Double total;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private FormaPago formaPago;

    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "pedido_id")
    @Builder.Default
    private Set<DetallePedido> detalles = new HashSet<>();


    public void addDetallePedido(int cantidad, Producto producto) {
        detalles.add(new DetallePedido(cantidad,cantidad* producto.getPrecio(), producto));
        calcularTotal();
    }

    public void calcularTotal() {
        this.total = detalles.stream()
                .mapToDouble(DetallePedido::getSubtotal)
                .sum();
    }

    public DetallePedido findDetallePedidoByProducto(Producto producto) {
        Long productoId = producto.getId();
        return detalles.stream()
                .filter(detalle ->
                        detalle.getProducto() != null &&
                                detalle.getProducto().getId().equals(productoId)
                )
                .findFirst()
                .orElse(null);
    }

    public void deleteDetallePedidoByProducto(Producto producto) {
        DetallePedido detalle = findDetallePedidoByProducto(producto);
        if (detalle != null) {
            detalles.remove(detalle);
            calcularTotal();
        }
    }

}
