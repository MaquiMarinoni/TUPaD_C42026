import java.util.ArrayList;
import java.util.List;

public class TurnoManager {
    private List<String> turnos = new ArrayList<>();

    public void procesar(Paciente paciente, boolean urgente) {

        // Cláusulas Guarda: Filtramos los casos inválidos y salimos temprano
        if (paciente.getNombre() == null || paciente.getNombre().equals("")) {
            return;
        }
        if (paciente.getEdad() <= 0) {
            return;
        }

        // A partir de acá, el código fluye plano (camino feliz)
        if (paciente.getObraSocial().equals("OSDE") || paciente.getObraSocial().equals("SWISS")) {
            System.out.println("Paciente premium");
        } else if (paciente.getObraSocial().equals("PUBLICA")) {
            System.out.println("Paciente publico");
        }

        String turno = formatearTurno(paciente, urgente);

        turnos.add(turno);
        System.out.println("Turno agregado");
    }

    // NUEVO METODO: Su única responsabilidad es dar formato al texto del turno
    private String formatearTurno(Paciente paciente, boolean urgente) {
        String turno = paciente.getNombre() + "-" + paciente.getEdad() + "-" + paciente.getObraSocial();
        if (urgente) {
            turno += "-URGENTE";
        }
        return turno;
    }

    public void mostrar() {
        for (int i = 0; i < turnos.size(); i++) {
            System.out.println(turnos.get(i));
        }
    }
}