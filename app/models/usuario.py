<<<<<<< HEAD
# app/models/usuario.py
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

=======
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING
>>>>>>> dev
from app.models.rol import Rol

if TYPE_CHECKING:
    from app.models.escuela import Escuela

class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"

    idUsuario: Optional[int] = Field(default=None, primary_key=True)
    dni: str = Field(index=True)
    cuil: Optional[str] = None
    mailABC: Optional[str] = None

<<<<<<< HEAD
=======
if TYPE_CHECKING:
    from .escuela import Escuela

class Usuario(UsuarioBase, table=True):
    idUsuario: int | None = Field(default=None, primary_key=True)
>>>>>>> dev
    contrasena: str
    celular: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None

    escuelas: list["Escuela"] = Relationship(
        back_populates="usuarios",
        link_model=Rol
    )
