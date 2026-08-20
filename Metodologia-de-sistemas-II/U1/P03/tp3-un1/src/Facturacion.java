import java.util.List;

public class Facturacion {
    public double calcularTotalFacturacion(List<Double> estudios, PerfilPaciente perfil) {
        double totalFacturado = sumarPrecioEstudios(estudios, perfil);

        if(perfil.tieneObraSocial() == true) {
            totalFacturado = totalFacturado * 0.9;
        }

        if(perfil.getCantidadConsultas() > 3) {
            totalFacturado = totalFacturado - 100;
        }

        return totalFacturado;
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