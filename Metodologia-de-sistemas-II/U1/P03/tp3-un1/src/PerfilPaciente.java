public class PerfilPaciente {
    private boolean aplicaPromocion;
    private boolean tieneObraSocial;
    private int cantidadConsultas;

    public PerfilPaciente(boolean aplicaPromocion, boolean tieneObraSocial, int cantidadConsultas) {
        this.aplicaPromocion = aplicaPromocion;
        this.tieneObraSocial = tieneObraSocial;
        this.cantidadConsultas = cantidadConsultas;
    }

    public boolean aplicaPromocion() { return aplicaPromocion; }
    public boolean tieneObraSocial() { return tieneObraSocial; }
    public int getCantidadConsultas() { return cantidadConsultas; }

    public double aplicarDescuentosFinales(double subtotal) {
        double total = subtotal;
        if(this.tieneObraSocial == true) {
            total = total * 0.9;
        }
        if(this.cantidadConsultas > 3) {
            total = total - 100;
        }
        return total;
    }
}