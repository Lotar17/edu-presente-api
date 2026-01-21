from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship

from app.models.rol import Rol
from app.schemas.usuario import UsuarioBase 

if TYPE_CHECKING:
    from app.models.escuela import Escuela

class Usuario(UsuarioBase, table=True):
    idUsuario: int | None = Field(default=None, primary_key=True)
    contrasena: str
    escuelas: list["Escuela"] = Relationship(back_populates="usuarios", link_model=Rol)


