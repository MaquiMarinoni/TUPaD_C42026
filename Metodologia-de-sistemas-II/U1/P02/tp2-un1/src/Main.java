public class Main {
    public static void main(String[] args) {

        // 1. Crea los distintos canales
        Notificacion email = new EmailNotificacion();
        Notificacion whatsapp = new WhatsappNotificacion();
        Notificacion telegram = new TelegramNotificacion();

        System.out.println("--- Prueba 1: Notificando por Email ---");
        // Inyecta la dependencia de Email al gestor
        GestorTurnos gestor1 = new GestorTurnos(email);
        gestor1.confirmarTurno("Carlos Rodríguez");

        System.out.println("\n--- Prueba 2: Cambiando a WhatsApp ---");
        // Inyecta la dependencia de WhatsApp a un nuevo gestor
        GestorTurnos gestor2 = new GestorTurnos(whatsapp);
        gestor2.confirmarTurno("Ana Gómez");

        System.out.println("\n--- Prueba 3: Usando el nuevo canal de Telegram ---");
        // inyecta Telegram (prueba de extensibilidad)
        GestorTurnos gestor3 = new GestorTurnos(telegram);
        gestor3.confirmarTurno("Luis Martínez");
    }
}