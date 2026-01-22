from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING
from app.models.rol import Rol
from app.schemas.usuario import UsuarioBase 


if TYPE_CHECKING:
    from .escuela import Escuela

class Usuario(UsuarioBase, table=True):
    idUsuario: int | None = Field(default=None, primary_key=True)
    contrasena: str
    escuelas: list["Escuela"] = Relationship(back_populates="usuarios", link_model=Rol)


