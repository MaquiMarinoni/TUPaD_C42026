from pathlib import Path

if __package__:
    from .consola import Consola
    from .repositorio import RepositorioJSON
    from .servicio import SistemaAcademico
else:
    from consola import Consola
    from repositorio import RepositorioJSON
    from servicio import SistemaAcademico


ARCHIVO = Path(__file__).resolve().parent.parent / "datos" / "solicitudes.json"


def main():
    try:
        repositorio = RepositorioJSON(ARCHIVO)
        sistema = SistemaAcademico(ARCHIVO, repositorio=repositorio)
    except (OSError, ValueError) as error:
        print(f"No se pudo iniciar el sistema: {error}")
        print("Revise el archivo de datos antes de volver a intentarlo.")
        return

    Consola(sistema).ejecutar()


if __name__ == "__main__":
    main()
