public class WhatsappNotificacion implements Notificacion {
    @Override
    public void enviar(String mensaje) {
        System.out.println("Enviando WhatsApp: " + mensaje);
    }
}