from sqlmodel import Session, select
from app.modules.usuarios.model import Usuario, Rol, UsuarioRol, utc_now


class UsuarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> Usuario | None:
        # Incluye inactivos: la dependencia verifica deleted_at y responde 400.
        return self.session.get(Usuario, user_id)

    def get_by_email(self, email: str) -> Usuario | None:
        return self.session.exec(select(Usuario).where(Usuario.email == email.strip().lower())).first()

    def get_all(self) -> list[Usuario]:
        return list(self.session.exec(select(Usuario).order_by(Usuario.id)).all())

    def roles_vigentes(self, user_id: int) -> list[str]:
        from sqlalchemy import or_
        return list(self.session.exec(select(Rol.nombre).join(UsuarioRol, Rol.id == UsuarioRol.rol_id).where(
            UsuarioRol.usuario_id == user_id,
            or_(UsuarioRol.expires_at.is_(None), UsuarioRol.expires_at > utc_now()),
        ).order_by(Rol.nombre)).all())

    def add(self, user: Usuario) -> Usuario:
        self.session.add(user)
        self.session.flush()
        return user
