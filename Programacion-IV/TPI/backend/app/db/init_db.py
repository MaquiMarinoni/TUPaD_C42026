from sqlmodel import SQLModel

import app.models
from app.db.session import engine


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
    print("Esquema de Food Store creado correctamente.")
