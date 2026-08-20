public class TelegramNotificacion implements Notificacion {
    @Override
    public void enviar(String mensaje) {
        System.out.println("Enviando mensaje por Telegram: " + mensaje);
    }
}