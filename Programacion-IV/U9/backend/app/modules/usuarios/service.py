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

    def public(self, usuario: Usuario) -> UserPublic:
        self.session.refresh(usuario)
        roles = self.repo.roles_vigentes(usuario.id)

        # La respuesta incluye los datos del usuario, pero nunca el hash.
        return UserPublic(
            id=usuario.id,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            email=usuario.email,
            celular=usuario.celular,
            roles=roles,
            created_at=usuario.created_at,
            updated_at=usuario.updated_at,
            deleted_at=usuario.deleted_at,
        )

    def register(self, data: UserCreate) -> UserPublic:
        usuario_existente = self.repo.get_by_email(data.email)
        if usuario_existente:
            raise HTTPException(409, "El email ya está registrado")

        consulta_rol = select(Rol).where(Rol.nombre == "user")
        rol_usuario = self.session.exec(consulta_rol).one()

        nuevo_usuario = Usuario(
            nombre=data.nombre,
            apellido=data.apellido,
            email=str(data.email).lower(),
            celular=data.celular,
            password_hash=hash_password(data.password),
        )

        try:
            self.repo.add(nuevo_usuario)

            # El registro público siempre asigna el rol user.
            asignacion = UsuarioRol(
                usuario_id=nuevo_usuario.id,
                rol_id=rol_usuario.id,
            )
            self.session.add(asignacion)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(409, "El email ya está registrado")

        return self.public(nuevo_usuario)

    def authenticate(self, email: str, password: str) -> Usuario:
        usuario = self.repo.get_by_email(email)
        if not usuario or not verify_password(password, usuario.password_hash):
            raise HTTPException(
                401,
                "Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if usuario.deleted_at is not None:
            raise HTTPException(400, "Cuenta de usuario desactivada")

        return usuario

    def list_all(self) -> list[UserPublic]:
        usuarios = self.repo.get_all()
        return [self.public(usuario) for usuario in usuarios]

    def set_active(self, user_id: int, active: bool) -> UserPublic:
        usuario = self.repo.get_by_id(user_id)
        if not usuario:
            raise HTTPException(404, "Usuario no encontrado")

        if active:
            usuario.deleted_at = None
        else:
            usuario.deleted_at = utc_now()

        usuario.updated_at = utc_now()
        self.session.add(usuario)
        self.session.commit()
        return self.public(usuario)
