from datetime import datetime, timezone
from typing import Generic, Optional, Type, TypeVar
from sqlmodel import SQLModel, Session, select

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):
    """Repositorio genérico que encapsula el acceso a datos sin confirmar la transacción (no llama a commit)."""

    def __init__(self, session: Session, model: Type[ModelType]):
        self.session = session
        self.model = model

    def get_all(self) -> list[ModelType]:
        statement = select(self.model)
        if hasattr(self.model, "deleted_at"):
            statement = statement.where(getattr(self.model, "deleted_at").is_(None))
        return list(self.session.exec(statement).all())

    def get_by_id(self, entity_id: int) -> Optional[ModelType]:
        obj = self.session.get(self.model, entity_id)
        if obj is not None and hasattr(obj, "deleted_at") and getattr(obj, "deleted_at") is not None:
            return None
        return obj

    def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        self.session.flush()
        self.session.refresh(obj)
        return obj

    def update(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        self.session.flush()
        self.session.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        if hasattr(obj, "deleted_at"):
            setattr(obj, "deleted_at", datetime.now(timezone.utc))
            self.session.add(obj)
        else:
            self.session.delete(obj)
        self.session.flush()
