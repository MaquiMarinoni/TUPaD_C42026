import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from src.main import SistemaAcademico


class PruebasSistemaAcademico(unittest.TestCase):
    def setUp(self):
        # Cada prueba utiliza su propia carpeta y sus propios datos.
        self.carpeta_temporal = TemporaryDirectory()
        self.addCleanup(self.carpeta_temporal.cleanup)

        self.archivo = (
            Path(self.carpeta_temporal.name) / "solicitudes.json"
        )
        self.sistema = SistemaAcademico(self.archivo)

    def registrar_solicitud(self, **cambios):
        datos = {
            "estudiante_id": "E001",
            "descripcion": "Solicito una constancia de alumno regular.",
            "tipo": "Certificado",
            "prioridad": "Media",
        }
        datos.update(cambios)
        return self.sistema.registrar(**datos)

    def test_01_registrar_solicitud_valida(self):
        solicitud_id = self.registrar_solicitud()

        resultados = self.sistema.consultar(solicitud_id=solicitud_id)

        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0]["estudiante_id"], "E001")
        self.assertEqual(
            resultados[0]["descripcion"],
            "Solicito una constancia de alumno regular.",
        )
        self.assertEqual(resultados[0]["tipo"], "Certificado")
        self.assertEqual(resultados[0]["prioridad"], "Media")
        self.assertEqual(resultados[0]["estado"], "Pendiente")
        self.assertIsNone(resultados[0]["responsable_id"])
        self.assertTrue(self.archivo.exists())

    def test_02_rechazar_estudiante_inexistente(self):
        with self.assertRaises(ValueError):
            self.registrar_solicitud(estudiante_id="E999")

        self.assertEqual(self.sistema.consultar(), [])
        self.assertFalse(self.archivo.exists())

    def test_03_validar_limites_de_descripcion(self):
        for longitud, es_valida in (
            (9, False),
            (10, True),
            (300, True),
            (301, False),
        ):
            with self.subTest(longitud=longitud):
                cantidad_anterior = len(self.sistema.consultar())

                if es_valida:
                    solicitud_id = self.registrar_solicitud(
                        descripcion="a" * longitud
                    )
                    resultado = self.sistema.consultar(
                        solicitud_id=solicitud_id
                    )
                    self.assertEqual(
                        len(resultado[0]["descripcion"]),
                        longitud,
                    )
                else:
                    with self.assertRaises(ValueError):
                        self.registrar_solicitud(
                            descripcion="a" * longitud
                        )

                    self.assertEqual(
                        len(self.sistema.consultar()),
                        cantidad_anterior,
                    )

    def test_04_rechazar_tipo_y_prioridad_invalidos(self):
        for cambios in (
            {"tipo": "Beca"},
            {"prioridad": "Urgente"},
        ):
            with self.subTest(cambios=cambios):
                with self.assertRaises(ValueError):
                    self.registrar_solicitud(**cambios)

        self.assertEqual(self.sistema.consultar(), [])
        self.assertFalse(self.archivo.exists())

    def test_05_asignar_y_rechazar_responsable_inexistente(self):
        solicitud_id = self.registrar_solicitud()
        self.sistema.asignar(solicitud_id, "R001")
        archivo_anterior = self.archivo.read_bytes()

        with self.assertRaises(ValueError):
            self.sistema.asignar(solicitud_id, "R999")

        resultado = self.sistema.consultar(solicitud_id=solicitud_id)
        self.assertEqual(resultado[0]["responsable_id"], "R001")
        self.assertEqual(self.archivo.read_bytes(), archivo_anterior)

    def test_06_rechazar_atencion_sin_responsable(self):
        solicitud_id = self.registrar_solicitud()
        archivo_anterior = self.archivo.read_bytes()

        with self.assertRaises(ValueError):
            self.sistema.cambiar_estado(solicitud_id, "En atención")

        resultado = self.sistema.consultar(solicitud_id=solicitud_id)
        self.assertEqual(resultado[0]["estado"], "Pendiente")
        self.assertEqual(self.archivo.read_bytes(), archivo_anterior)

    def test_07_completar_transiciones_validas(self):
        solicitud_id = self.registrar_solicitud()
        self.sistema.asignar(solicitud_id, "R001")

        self.sistema.cambiar_estado(solicitud_id, "En atención")
        resultado = self.sistema.consultar(solicitud_id=solicitud_id)
        self.assertEqual(resultado[0]["estado"], "En atención")

        self.sistema.cambiar_estado(solicitud_id, "Resuelta")
        resultado = self.sistema.consultar(solicitud_id=solicitud_id)
        self.assertEqual(resultado[0]["estado"], "Resuelta")

    def test_08_rechazar_cambios_en_solicitud_resuelta(self):
        solicitud_id = self.registrar_solicitud()
        self.sistema.asignar(solicitud_id, "R001")
        self.sistema.cambiar_estado(solicitud_id, "En atención")
        self.sistema.cambiar_estado(solicitud_id, "Resuelta")
        archivo_anterior = self.archivo.read_bytes()

        with self.assertRaises(ValueError):
            self.sistema.cambiar_estado(solicitud_id, "Pendiente")

        with self.assertRaises(ValueError):
            self.sistema.asignar(solicitud_id, "R002")

        resultado = self.sistema.consultar(solicitud_id=solicitud_id)
        self.assertEqual(resultado[0]["estado"], "Resuelta")
        self.assertEqual(resultado[0]["responsable_id"], "R001")
        self.assertEqual(self.archivo.read_bytes(), archivo_anterior)

    def test_09_combinar_filtros(self):
        esperado = self.registrar_solicitud(prioridad="Alta")
        self.registrar_solicitud(prioridad="Media")
        self.registrar_solicitud(tipo="Consulta", prioridad="Alta")

        resultados = self.sistema.consultar(
            tipo="Certificado",
            prioridad="Alta",
        )

        self.assertEqual([s["id"] for s in resultados], [esperado])

    def test_10_consultar_y_reportar_sin_resultados(self):
        self.assertEqual(self.sistema.consultar(), [])
        self.assertEqual(
            self.sistema.consultar(solicitud_id=999),
            [],
        )

        reporte = self.sistema.reporte()
        self.assertEqual(reporte["total"], 0)
        self.assertTrue(
            all(cantidad == 0 for cantidad in reporte["por_estado"].values())
        )
        self.assertTrue(
            all(
                cantidad == 0
                for cantidad in reporte["por_prioridad"].values()
            )
        )

    def test_11_recuperar_datos_y_conservar_ids_unicos(self):
        primer_id = self.registrar_solicitud()
        self.sistema.asignar(primer_id, "R001")
        self.sistema.cambiar_estado(primer_id, "En atención")
        datos_anteriores = self.sistema.consultar()

        # Una nueva instancia representa el reinicio del programa.
        reiniciado = SistemaAcademico(self.archivo)

        self.assertEqual(reiniciado.consultar(), datos_anteriores)

        segundo_id = reiniciado.registrar(
            "E002",
            "Necesito consultar las fechas de inscripción.",
            "Consulta",
            "Baja",
        )

        self.assertNotEqual(primer_id, segundo_id)
        ids = [s["id"] for s in reiniciado.consultar()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_12_rechazar_json_corrupto_sin_reemplazarlo(self):
        contenido_corrupto = '{"solicitudes":'
        self.archivo.write_text(contenido_corrupto, encoding="utf-8")

        with self.assertRaises(ValueError):
            SistemaAcademico(self.archivo)

        self.assertEqual(
            self.archivo.read_text(encoding="utf-8"),
            contenido_corrupto,
        )

    def test_13_generar_reporte_coherente(self):
        self.registrar_solicitud(prioridad="Baja")
        self.registrar_solicitud(prioridad="Media")
        tercera = self.registrar_solicitud(prioridad="Alta")

        self.sistema.asignar(tercera, "R001")
        self.sistema.cambiar_estado(tercera, "En atención")
        self.sistema.cambiar_estado(tercera, "Resuelta")

        reporte = self.sistema.reporte()

        self.assertEqual(reporte["total"], 3)
        self.assertEqual(
            reporte["por_estado"],
            {
                "Pendiente": 2,
                "En atención": 0,
                "Resuelta": 1,
                "Cancelada": 0,
            },
        )
        self.assertEqual(
            reporte["por_prioridad"],
            {"Baja": 1, "Media": 1, "Alta": 1},
        )

    def test_14_conservar_datos_si_falla_el_guardado(self):
        solicitud_id = self.registrar_solicitud()
        datos_anteriores = self.sistema.consultar()
        archivo_anterior = self.archivo.read_bytes()

        # Se simula un fallo al reemplazar el archivo original.
        with patch.object(
            Path,
            "replace",
            side_effect=OSError("Fallo de escritura simulado"),
        ):
            with self.assertRaises(OSError):
                self.sistema.asignar(solicitud_id, "R001")

        self.assertEqual(self.sistema.consultar(), datos_anteriores)
        self.assertEqual(self.archivo.read_bytes(), archivo_anterior)

        contenido = json.loads(self.archivo.read_text(encoding="utf-8"))
        self.assertIsNone(
            contenido["solicitudes"][0]["responsable_id"]
        )


if __name__ == "__main__":
    unittest.main()