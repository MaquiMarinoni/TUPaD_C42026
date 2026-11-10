from sqlalchemy import or_
from sqlmodel import Session, select

from app.modules.usuarios.model import Usuario, Rol, UsuarioRol, utc_now


class UsuarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> Usuario | None:
        # Se buscan también los inactivos para poder mostrar el error de cuenta desactivada.
        return self.session.get(Usuario, user_id)

    def get_by_email(self, email: str) -> Usuario | None:
        email_normalizado = email.strip().lower()
        consulta = select(Usuario).where(Usuario.email == email_normalizado)
        return self.session.exec(consulta).first()

    def get_all(self) -> list[Usuario]:
        consulta = select(Usuario).order_by(Usuario.id)
        return list(self.session.exec(consulta).all())

    def roles_vigentes(self, user_id: int) -> list[str]:
        # Un rol sirve si no tiene vencimiento o si la fecha todavía no pasó.
        sin_vencer = or_(
            UsuarioRol.expires_at.is_(None),
            UsuarioRol.expires_at > utc_now(),
        )
        consulta = (
            select(Rol.nombre)
            .join(UsuarioRol, Rol.id == UsuarioRol.rol_id)
            .where(UsuarioRol.usuario_id == user_id, sin_vencer)
            .order_by(Rol.nombre)
        )
        return list(self.session.exec(consulta).all())

    def add(self, user: Usuario) -> Usuario:
        self.session.add(user)
        # flush obtiene el id; el servicio confirma la transacción con commit.
        self.session.flush()
        return user
