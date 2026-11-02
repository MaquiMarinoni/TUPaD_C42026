import json
from pathlib import Path


class RepositorioJSON:
    def __init__(self, archivo):
        self.archivo = Path(archivo)

    def cargar(self):
        if not self.archivo.exists():
            return None

        with self.archivo.open("r", encoding="utf-8") as archivo:
            contenido = json.load(archivo)

        if not isinstance(contenido, dict):
            raise ValueError("El archivo debe contener un objeto JSON.")

        for clave in ("estudiantes", "responsables", "solicitudes"):
            if clave not in contenido or not isinstance(contenido[clave], list):
                raise ValueError(f"El archivo no contiene una lista '{clave}'.")

        return contenido

    def guardar(self, datos):
        self.archivo.parent.mkdir(parents=True, exist_ok=True)
        temporal = self.archivo.with_suffix(".tmp")

        with temporal.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)

        temporal.replace(self.archivo)