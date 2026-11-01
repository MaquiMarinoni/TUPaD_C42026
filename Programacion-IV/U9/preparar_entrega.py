"""Crea los dos ZIP de entrega a partir de los archivos versionados, sin secretos."""
from pathlib import Path
import subprocess
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parent
repo = Path(subprocess.check_output(["git", "-C", str(root), "rev-parse", "--show-toplevel"], text=True).strip())
out = root / "entrega"
out.mkdir(exist_ok=True)
excluded = {"node_modules", ".venv", "venv", "__pycache__", ".pytest_cache", "dist", ".git"}
for project in ("backend", "frontend"):
    source = root / project
    relative = source.relative_to(repo).as_posix()
    paths = subprocess.check_output(["git", "-C", str(repo), "ls-files", "-z", "--", relative]).decode().split("\0")
    archive = out / f"U9_{project}_Marinoni.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as z:
        for item in sorted(filter(None, paths)):
            p = repo / item
            rel = p.relative_to(source)
            if excluded.intersection(rel.parts):
                continue
            if (p.name.startswith(".env") and p.name != ".env.example") or p.suffix in {".db", ".sqlite", ".sqlite3", ".pyc"}:
                continue
            z.write(p, (Path(project) / rel).as_posix())
        # La guía principal permite instalar cada entrega aunque se descargue por separado.
        z.write(root / "README.md", f"{project}/GUIA_U9.md")
    print(archive)
