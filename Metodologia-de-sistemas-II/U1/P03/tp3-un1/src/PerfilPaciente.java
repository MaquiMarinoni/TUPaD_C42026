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
}