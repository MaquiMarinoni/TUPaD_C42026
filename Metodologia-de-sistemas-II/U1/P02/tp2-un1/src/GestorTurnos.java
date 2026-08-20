public class GestorTurnos {

    // Depende de la abstraccion, no de una implementacion concreta
    private Notificacion mecanismoNotificacion;

    // Inyeccion de dependencia por constructor
    public GestorTurnos(Notificacion mecanismoNotificacion) {
        this.mecanismoNotificacion = mecanismoNotificacion;
    }

    // Metodo que simula la lógica de negocio
    public void confirmarTurno(String paciente) {
        System.out.println("Registrando turno en la base de datos para: " + paciente);

        // se delega el envío al mecanismo inyectado
        mecanismoNotificacion.enviar("Su turno ha sido confirmado exitosamente.");
    }
}