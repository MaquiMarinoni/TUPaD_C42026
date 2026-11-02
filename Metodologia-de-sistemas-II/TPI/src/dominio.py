from dataclasses import asdict, dataclass, replace


TIPOS = ("Certificado", "Inscripción", "Consulta")
PRIORIDADES = ("Baja", "Media", "Alta")
ESTADOS = ("Pendiente", "En atención", "Resuelta", "Cancelada")
ESTADOS_FINALES = ("Resuelta", "Cancelada")

TRANSICIONES = {
    "Pendiente": ("En atención", "Cancelada"),
    "En atención": ("Resuelta", "Cancelada"),
}


@dataclass(frozen=True)
class DatosNuevaSolicitud:
    estudiante_id: str
    descripcion: str
    tipo: str
    prioridad: str


@dataclass(frozen=True)
class Solicitud:
    id: int
    estudiante_id: str
    descripcion: str
    tipo: str
    prioridad: str
    estado: str = "Pendiente"
    responsable_id: str | None = None

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(**datos)

    def a_diccionario(self):
        return asdict(self)

    def asignar_responsable(self, responsable_id):
        if self.estado in ESTADOS_FINALES:
            raise ValueError("No se puede reasignar una solicitud finalizada.")

        return replace(self, responsable_id=responsable_id)

    def cambiar_estado(self, nuevo_estado):
        if self.estado not in TRANSICIONES:
            raise ValueError("La solicitud ya está finalizada.")

        if nuevo_estado not in TRANSICIONES[self.estado]:
            raise ValueError("La transición de estado no está permitida.")

        if nuevo_estado == "En atención" and self.responsable_id is None:
            raise ValueError("Primero se debe asignar un responsable.")

        # Se devuelve una nueva entidad sin modificar la anterior.
        return replace(self, estado=nuevo_estado)
