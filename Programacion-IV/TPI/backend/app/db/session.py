from collections.abc import Generator

from sqlalchemy.orm import Session
from sqlmodel import create_engine

from app.core.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
