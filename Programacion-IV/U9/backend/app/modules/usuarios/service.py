from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from app.core.security import hash_password, verify_password
from app.modules.usuarios.model import Usuario, UsuarioRol, Rol, utc_now
from app.modules.usuarios.repository import UsuarioRepository
from app.modules.usuarios.schema import UserCreate, UserPublic


class UsuarioService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = UsuarioRepository(session)

    def public(self, user: Usuario) -> UserPublic:
        self.session.refresh(user)
        return UserPublic(**user.model_dump(exclude={"password_hash"}), roles=self.repo.roles_vigentes(user.id))

    def register(self, data: UserCreate) -> UserPublic:
        if self.repo.get_by_email(data.email):
            raise HTTPException(409, "El email ya está registrado")
        role = self.session.exec(select(Rol).where(Rol.nombre == "user")).one()
        user = Usuario(**data.model_dump(exclude={"password", "email"}), email=str(data.email).lower(), password_hash=hash_password(data.password))
        try:
            self.repo.add(user)
            self.session.add(UsuarioRol(usuario_id=user.id, rol_id=role.id))
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(409, "El email ya está registrado")
        return self.public(user)

    def authenticate(self, email: str, password: str) -> Usuario:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(401, "Credenciales incorrectas", headers={"WWW-Authenticate": "Bearer"})
        if user.deleted_at is not None:
            raise HTTPException(400, "Cuenta de usuario desactivada")
        return user

    def list_all(self) -> list[UserPublic]:
        return [self.public(user) for user in self.repo.get_all()]

    def set_active(self, user_id: int, active: bool) -> UserPublic:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(404, "Usuario no encontrado")
        user.deleted_at = None if active else utc_now()
        user.updated_at = utc_now()
        self.session.add(user)
        self.session.commit()
        return self.public(user)
