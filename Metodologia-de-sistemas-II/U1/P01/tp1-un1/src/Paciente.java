public class Paciente {
    private String nombre;
    private int edad;
    private String obraSocial;

    public Paciente(String nombre, int edad, String obraSocial) {
        this.nombre = nombre;
        this.edad = edad;
        this.obraSocial = obraSocial;
    }

    public String getNombre() {
        return nombre;
    }

    public int getEdad() {
        return edad;
    }

    public String getObraSocial() {
        return obraSocial;
    }
}