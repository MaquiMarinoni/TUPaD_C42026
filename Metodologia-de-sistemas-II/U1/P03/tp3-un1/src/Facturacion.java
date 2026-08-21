import java.util.List;

public class Facturacion {
    public double calcularTotalFacturacion(List<Double> estudios, PerfilPaciente perfil) {
        // 1. Calculamos el subtotal de los estudios
        double totalFacturado = sumarPrecioEstudios(estudios, perfil);

        // 2. Delegamos la responsabilidad de los descuentos al perfil
        return perfil.aplicarDescuentosFinales(totalFacturado);
    }

    private static double sumarPrecioEstudios(List<Double> estudios, PerfilPaciente perfil) {
        double totalFacturado = 0;

        for(Double precioEstudio : estudios) {
            if(perfil.aplicaPromocion() == true) {
                totalFacturado += precioEstudio * 0.5;
            } else {
                totalFacturado += precioEstudio;
            }
        }
        return totalFacturado;
    }
}