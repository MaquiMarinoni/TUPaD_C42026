import json
from pathlib import Path


ARCHIVO = Path(__file__).resolve().parent.parent / "datos" / "solicitudes.json"


class SistemaAcademico:
    def __init__(self, archivo):
        self.archivo = Path(archivo)
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

        if self.archivo.exists():
            with self.archivo.open("r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)

            if not isinstance(contenido, dict):
                raise ValueError("El archivo debe contener un objeto JSON.")

            for clave in ("estudiantes", "responsables", "solicitudes"):
                if clave not in contenido or not isinstance(contenido[clave], list):
                    raise ValueError(f"El archivo no contiene una lista '{clave}'.")

            self.datos = contenido

    def registrar(self, estudiante_id, descripcion, tipo, prioridad):
        estudiante = next(
            (
                e
                for e in self.datos["estudiantes"]
                if e["id"] == estudiante_id
            ),
            None,
        )

        if estudiante is None:
            raise ValueError("El estudiante no existe.")

        descripcion = descripcion.strip()

        if not 10 <= len(descripcion) <= 300:
            raise ValueError("La descripción debe tener entre 10 y 300 caracteres.")

        if tipo not in ("Certificado", "Inscripción", "Consulta"):
            raise ValueError("El tipo de solicitud no es válido.")

        if prioridad not in ("Baja", "Media", "Alta"):
            raise ValueError("La prioridad no es válida.")

        nuevo_id = max(
            (s["id"] for s in self.datos["solicitudes"]),
            default=0,
        ) + 1

        solicitud = {
            "id": nuevo_id,
            "estudiante_id": estudiante_id,
            "descripcion": descripcion,
            "tipo": tipo,
            "prioridad": prioridad,
            "estado": "Pendiente",
            "responsable_id": None,
        }

        nuevos_datos = {
            **self.datos,
            "solicitudes": self.datos["solicitudes"] + [solicitud],
        }

        self.archivo.parent.mkdir(parents=True, exist_ok=True)
        temporal = self.archivo.with_suffix(".tmp")

        with temporal.open("w", encoding="utf-8") as archivo:
            json.dump(nuevos_datos, archivo, ensure_ascii=False, indent=4)

        temporal.replace(self.archivo)
        self.datos = nuevos_datos
        return nuevo_id

    def asignar(self, solicitud_id, responsable_id):
        solicitud = next(
            (
                s
                for s in self.datos["solicitudes"]
                if s["id"] == solicitud_id
            ),
            None,
        )

        if solicitud is None:
            raise ValueError("La solicitud no existe.")

        responsable = next(
            (
                r
                for r in self.datos["responsables"]
                if r["id"] == responsable_id
            ),
            None,
        )

        if responsable is None:
            raise ValueError("El responsable no existe.")

        if solicitud["estado"] in ("Resuelta", "Cancelada"):
            raise ValueError("No se puede reasignar una solicitud finalizada.")

        actualizada = {**solicitud, "responsable_id": responsable_id}
        nuevas_solicitudes = [
            actualizada if s["id"] == solicitud_id else s
            for s in self.datos["solicitudes"]
        ]
        nuevos_datos = {**self.datos, "solicitudes": nuevas_solicitudes}

        self.archivo.parent.mkdir(parents=True, exist_ok=True)
        temporal = self.archivo.with_suffix(".tmp")

        with temporal.open("w", encoding="utf-8") as archivo:
            json.dump(nuevos_datos, archivo, ensure_ascii=False, indent=4)

        temporal.replace(self.archivo)
        self.datos = nuevos_datos

    def cambiar_estado(self, solicitud_id, nuevo_estado):
        solicitud = next(
            (
                s
                for s in self.datos["solicitudes"]
                if s["id"] == solicitud_id
            ),
            None,
        )

        if solicitud is None:
            raise ValueError("La solicitud no existe.")

        estado_actual = solicitud["estado"]

        if estado_actual == "Pendiente":
            if nuevo_estado not in ("En atención", "Cancelada"):
                raise ValueError("La transición de estado no está permitida.")
        elif estado_actual == "En atención":
            if nuevo_estado not in ("Resuelta", "Cancelada"):
                raise ValueError("La transición de estado no está permitida.")
        else:
            raise ValueError("La solicitud ya está finalizada.")

        if nuevo_estado == "En atención":
            if solicitud["responsable_id"] is None:
                raise ValueError("Primero se debe asignar un responsable.")

        actualizada = {**solicitud, "estado": nuevo_estado}
        nuevas_solicitudes = [
            actualizada if s["id"] == solicitud_id else s
            for s in self.datos["solicitudes"]
        ]
        nuevos_datos = {**self.datos, "solicitudes": nuevas_solicitudes}

        self.archivo.parent.mkdir(parents=True, exist_ok=True)
        temporal = self.archivo.with_suffix(".tmp")

        with temporal.open("w", encoding="utf-8") as archivo:
            json.dump(nuevos_datos, archivo, ensure_ascii=False, indent=4)

        temporal.replace(self.archivo)
        self.datos = nuevos_datos

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
        por_estado = {
            "Pendiente": 0,
            "En atención": 0,
            "Resuelta": 0,
            "Cancelada": 0,
        }
        por_prioridad = {"Baja": 0, "Media": 0, "Alta": 0}

        for solicitud in self.datos["solicitudes"]:
            por_estado[solicitud["estado"]] += 1
            por_prioridad[solicitud["prioridad"]] += 1

        return {
            "total": len(self.datos["solicitudes"]),
            "por_estado": por_estado,
            "por_prioridad": por_prioridad,
        }

    def ejecutar(self):
        while True:
            print("\nSISTEMA DE GESTIÓN DE SOLICITUDES ACADÉMICAS")
            print("1. Registrar solicitud")
            print("2. Asignar responsable")
            print("3. Cambiar estado")
            print("4. Consultar solicitudes")
            print("5. Generar reporte")
            print("6. Ver estudiantes y responsables")
            print("0. Salir")

            opcion = input("Seleccione una opción: ").strip()

            try:
                if opcion == "1":
                    estudiante_id = input("ID del estudiante: ").strip().upper()
                    descripcion = input("Descripción: ")
                    print("Tipos: Certificado / Inscripción / Consulta")
                    tipo = input("Tipo: ").strip()
                    print("Prioridades: Baja / Media / Alta")
                    prioridad = input("Prioridad: ").strip()

                    nuevo_id = self.registrar(
                        estudiante_id, descripcion, tipo, prioridad
                    )
                    print(f"Solicitud registrada con ID {nuevo_id}.")

                elif opcion == "2":
                    solicitud_id = int(input("ID de la solicitud: "))
                    responsable_id = input("ID del responsable: ").strip().upper()
                    self.asignar(solicitud_id, responsable_id)
                    print("Responsable asignado correctamente.")

                elif opcion == "3":
                    solicitud_id = int(input("ID de la solicitud: "))
                    print("Estados: Pendiente / En atención / Resuelta / Cancelada")
                    nuevo_estado = input("Nuevo estado: ").strip()
                    self.cambiar_estado(solicitud_id, nuevo_estado)
                    print("Estado actualizado correctamente.")

                elif opcion == "4":
                    print("Deje los campos vacíos para no aplicar ese filtro.")
                    texto_id = input("ID de solicitud: ").strip()
                    solicitud_id = int(texto_id) if texto_id else None
                    estado = input("Estado: ").strip()
                    tipo = input("Tipo: ").strip()
                    prioridad = input("Prioridad: ").strip()

                    resultados = self.consultar(
                        solicitud_id, estado, tipo, prioridad
                    )

                    if not resultados:
                        print("No se encontraron solicitudes.")

                    for solicitud in resultados:
                        print(
                            f"\nID: {solicitud['id']}"
                            f"\nEstudiante: {solicitud['estudiante_id']}"
                            f"\nDescripción: {solicitud['descripcion']}"
                            f"\nTipo: {solicitud['tipo']}"
                            f"\nPrioridad: {solicitud['prioridad']}"
                            f"\nEstado: {solicitud['estado']}"
                            f"\nResponsable: "
                            f"{solicitud['responsable_id'] or 'Sin asignar'}"
                        )

                elif opcion == "5":
                    reporte = self.reporte()
                    print(f"\nTotal de solicitudes: {reporte['total']}")

                    print("\nPor estado:")
                    for estado, cantidad in reporte["por_estado"].items():
                        print(f"  {estado}: {cantidad}")

                    print("\nPor prioridad:")
                    for prioridad, cantidad in reporte["por_prioridad"].items():
                        print(f"  {prioridad}: {cantidad}")

                elif opcion == "6":
                    print("\nEstudiantes:")
                    for estudiante in self.datos["estudiantes"]:
                        print(
                            f"{estudiante['id']} - {estudiante['nombre']} "
                            f"- Legajo: {estudiante['legajo']}"
                        )

                    print("\nResponsables:")
                    for responsable in self.datos["responsables"]:
                        print(
                            f"{responsable['id']} - {responsable['nombre']} "
                            f"- Área: {responsable['area']}"
                        )

                elif opcion == "0":
                    print("Programa finalizado.")
                    break

                else:
                    print("La opción ingresada no es válida.")

            except ValueError as error:
                print(f"No se pudo completar la operación: {error}")
            except OSError as error:
                print(f"No se pudo acceder al archivo de datos: {error}")


if __name__ == "__main__":
    try:
        sistema = SistemaAcademico(ARCHIVO)
    except (OSError, ValueError) as error:
        print(f"No se pudo iniciar el sistema: {error}")
        print("Revise el archivo de datos antes de volver a intentarlo.")
    else:
        sistema.ejecutar()