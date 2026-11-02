import copy
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.dominio import DatosNuevaSolicitud, Solicitud
from src.main import SistemaAcademico
from src.repositorio import RepositorioJSON


class RepositorioMemoria:
    def __init__(self):
        self.datos = None
        self.fallar = False

    def cargar(self):
        return copy.deepcopy(self.datos)

    def guardar(self, datos):
        if self.fallar:
            raise OSError("Fallo de guardado simulado")
        self.datos = copy.deepcopy(datos)


class PruebasRefactoring(unittest.TestCase):
    def test_registrar_con_objeto_de_parametros(self):
        sistema = SistemaAcademico(
            None,
            repositorio=RepositorioMemoria(),
        )
        datos = DatosNuevaSolicitud(
            estudiante_id="E001",
            descripcion="Solicito una constancia de alumno regular.",
            tipo="Certificado",
            prioridad="Media",
        )

        solicitud_id = sistema.registrar_datos(datos)
        resultado = sistema.consultar(solicitud_id=solicitud_id)

        self.assertEqual(resultado[0]["estudiante_id"], "E001")
        self.assertEqual(resultado[0]["descripcion"], datos.descripcion)

    def test_contrato_comun_de_repositorios(self):
        datos = {
            "estudiantes": [],
            "responsables": [],
            "solicitudes": [],
        }

        with TemporaryDirectory() as carpeta:
            repositorios = [
                RepositorioMemoria(),
                RepositorioJSON(Path(carpeta) / "prueba.json"),
            ]

            for repositorio in repositorios:
                with self.subTest(tipo=type(repositorio).__name__):
                    self.assertIsNone(repositorio.cargar())
                    repositorio.guardar(datos)
                    self.assertEqual(repositorio.cargar(), datos)

                    # Cambiar el objeto recuperado no modifica lo guardado.
                    recuperado = repositorio.cargar()
                    recuperado["solicitudes"].append({"id": 999})
                    self.assertEqual(repositorio.cargar(), datos)

    def test_servicio_con_ambos_repositorios(self):
        with TemporaryDirectory() as carpeta:
            repositorios = [
                RepositorioMemoria(),
                RepositorioJSON(Path(carpeta) / "prueba.json"),
            ]
            resultados = []

            for repositorio in repositorios:
                sistema = SistemaAcademico(None, repositorio=repositorio)
                solicitud_id = sistema.registrar(
                    "E001",
                    "Solicito una constancia de alumno regular.",
                    "Certificado",
                    "Media",
                )
                sistema.asignar(solicitud_id, "R001")
                sistema.cambiar_estado(solicitud_id, "En atención")

                reiniciado = SistemaAcademico(
                    None,
                    repositorio=repositorio,
                )
                resultados.append(reiniciado.consultar())

            self.assertEqual(resultados[0], resultados[1])

    def test_fallo_del_repositorio_no_modifica_memoria(self):
        repositorio = RepositorioMemoria()
        sistema = SistemaAcademico(None, repositorio=repositorio)
        solicitud_id = sistema.registrar(
            "E001",
            "Solicito una constancia de alumno regular.",
            "Certificado",
            "Media",
        )
        anterior = sistema.consultar()
        repositorio.fallar = True

        with self.assertRaises(OSError):
            sistema.asignar(solicitud_id, "R001")

        self.assertEqual(sistema.consultar(), anterior)

    def test_transicion_del_dominio_sin_archivos(self):
        original = Solicitud(
            id=1,
            estudiante_id="E001",
            descripcion="Solicito una constancia de alumno regular.",
            tipo="Certificado",
            prioridad="Media",
        )

        with self.assertRaises(ValueError):
            original.cambiar_estado("En atención")

        asignada = original.asignar_responsable("R001")
        atendida = asignada.cambiar_estado("En atención")
        resuelta = atendida.cambiar_estado("Resuelta")

        self.assertEqual(original.estado, "Pendiente")
        self.assertIsNone(original.responsable_id)
        self.assertEqual(resuelta.estado, "Resuelta")

        with self.assertRaises(ValueError):
            resuelta.cambiar_estado("Pendiente")

    def test_cancelacion_desde_estados_activos(self):
        original = Solicitud(
            id=1,
            estudiante_id="E001",
            descripcion="Solicito una constancia de alumno regular.",
            tipo="Certificado",
            prioridad="Media",
        )
        en_atencion = original.asignar_responsable("R001")
        en_atencion = en_atencion.cambiar_estado("En atención")

        for solicitud in (original, en_atencion):
            with self.subTest(estado=solicitud.estado):
                cancelada = solicitud.cambiar_estado("Cancelada")
                self.assertEqual(cancelada.estado, "Cancelada")

                with self.assertRaises(ValueError):
                    cancelada.cambiar_estado("Pendiente")

                with self.assertRaises(ValueError):
                    cancelada.asignar_responsable("R002")


if __name__ == "__main__":
    unittest.main()
