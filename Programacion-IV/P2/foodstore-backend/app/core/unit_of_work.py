from typing import Optional
from sqlmodel import Session
from app.core.database import engine


class UnitOfWork:
    """Unit of Work base: agrupa operaciones en una sola transacción (commit al salir sin error, rollback ante excepción)."""

    def __init__(self, session_factory=lambda: Session(engine)):
        self._session_factory = session_factory
        self.session: Optional[Session] = None

    def __enter__(self):
        self.session = self._session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session is None:
            return
        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        finally:
            self.session.close()

    def commit(self) -> None:
        if self.session is not None:
            self.session.commit()

    def rollback(self) -> None:
        if self.session is not None:
            self.session.rollback()
