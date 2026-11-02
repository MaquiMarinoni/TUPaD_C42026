if __package__:
    from .dominio import (
        DatosNuevaSolicitud,
        ESTADOS,
        PRIORIDADES,
        TIPOS,
        Solicitud,
    )
    from .repositorio import RepositorioJSON
else:
    from dominio import (
        DatosNuevaSolicitud,
        ESTADOS,
        PRIORIDADES,
        TIPOS,
        Solicitud,
    )
    from repositorio import RepositorioJSON


class SistemaAcademico:
    def __init__(self, archivo, repositorio=None):
        self.repositorio = (
            repositorio
            if repositorio is not None
            else RepositorioJSON(archivo)
        )

        self.datos = {
            "estudiantes": [
                {"id": "E001", "nombre": "Ana Pérez", "legajo": "1001"},
                {"id": "E002", "nombre": "Luis Gómez", "legajo": "1002"},
            ],
            "responsables": [
                {
                    "id": "R001",
                    "nombre": "Laura Díaz",
                    "area": "Secretaría Académica",
                },
                {
                    "id": "R002",
                    "nombre": "Diego Ruiz",
                    "area": "Departamento de Alumnos",
                },
            ],
            "solicitudes": [],
        }

        contenido = self.repositorio.cargar()

        if contenido is not None:
            self.datos = contenido

    def _guardar_datos(self, nuevos_datos):
        self.repositorio.guardar(nuevos_datos)
        self.datos = nuevos_datos

    def _buscar_solicitud(self, solicitud_id):
        datos = next(
            (
                solicitud
                for solicitud in self.datos["solicitudes"]
                if solicitud["id"] == solicitud_id
            ),
            None,
        )

        if datos is None:
            raise ValueError("La solicitud no existe.")

        return Solicitud.desde_diccionario(datos)

    def _actualizar_solicitud(self, solicitud):
        actualizada = solicitud.a_diccionario()
        nuevas_solicitudes = [
            actualizada if registro["id"] == solicitud.id else registro
            for registro in self.datos["solicitudes"]
        ]

        nuevos_datos = {
            **self.datos,
            "solicitudes": nuevas_solicitudes,
        }
        self._guardar_datos(nuevos_datos)

    def registrar(self, estudiante_id, descripcion, tipo, prioridad):
        # Conserva la entrada original para las pruebas de regresión.
        datos = DatosNuevaSolicitud(
            estudiante_id=estudiante_id,
            descripcion=descripcion,
            tipo=tipo,
            prioridad=prioridad,
        )
        return self.registrar_datos(datos)

    def registrar_datos(self, datos):
        estudiante = next(
            (
                estudiante
                for estudiante in self.datos["estudiantes"]
                if estudiante["id"] == datos.estudiante_id
            ),
            None,
        )

        if estudiante is None:
            raise ValueError("El estudiante no existe.")

        descripcion = datos.descripcion.strip()

        if not 10 <= len(descripcion) <= 300:
            raise ValueError(
                "La descripción debe tener entre 10 y 300 caracteres."
            )

        if datos.tipo not in TIPOS:
            raise ValueError("El tipo de solicitud no es válido.")

        if datos.prioridad not in PRIORIDADES:
            raise ValueError("La prioridad no es válida.")

        nuevo_id = max(
            (
                solicitud["id"]
                for solicitud in self.datos["solicitudes"]
            ),
            default=0,
        ) + 1

        solicitud = Solicitud(
            id=nuevo_id,
            estudiante_id=datos.estudiante_id,
            descripcion=descripcion,
            tipo=datos.tipo,
            prioridad=datos.prioridad,
        )

        nuevos_datos = {
            **self.datos,
            "solicitudes": (
                self.datos["solicitudes"] + [solicitud.a_diccionario()]
            ),
        }

        self._guardar_datos(nuevos_datos)
        return nuevo_id

    def asignar(self, solicitud_id, responsable_id):
        solicitud = self._buscar_solicitud(solicitud_id)

        responsable = next(
            (
                responsable
                for responsable in self.datos["responsables"]
                if responsable["id"] == responsable_id
            ),
            None,
        )

        if responsable is None:
            raise ValueError("El responsable no existe.")

        actualizada = solicitud.asignar_responsable(responsable_id)
        self._actualizar_solicitud(actualizada)

    def cambiar_estado(self, solicitud_id, nuevo_estado):
        solicitud = self._buscar_solicitud(solicitud_id)
        actualizada = solicitud.cambiar_estado(nuevo_estado)
        self._actualizar_solicitud(actualizada)

    def consultar(self, solicitud_id=None, estado="", tipo="", prioridad=""):
        resultados = []

        for solicitud in self.datos["solicitudes"]:
            if solicitud_id is not None and solicitud["id"] != solicitud_id:
                continue
            if estado and solicitud["estado"] != estado:
                continue
            if tipo and solicitud["tipo"] != tipo:
                continue
            if prioridad and solicitud["prioridad"] != prioridad:
                continue

            resultados.append(solicitud.copy())

        return resultados

    def reporte(self):
        por_estado = dict.fromkeys(ESTADOS, 0)
        por_prioridad = dict.fromkeys(PRIORIDADES, 0)

        for solicitud in self.datos["solicitudes"]:
            por_estado[solicitud["estado"]] += 1
            por_prioridad[solicitud["prioridad"]] += 1

        return {
            "total": len(self.datos["solicitudes"]),
            "por_estado": por_estado,
            "por_prioridad": por_prioridad,
        }
