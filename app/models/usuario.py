from sqlmodel import Field, Relationship
from app.models.escuela import Escuela
from app.models.rol import Rol
from app.schemas.usuario import UsuarioBase 


class Usuario(UsuarioBase, table=True):
    idUsuario: int | None = Field(default=None, primary_key=True)
    contrasena: str
    escuelas: list["Escuela"] = Relationship(back_populates="usuarios", link_model=Rol)


