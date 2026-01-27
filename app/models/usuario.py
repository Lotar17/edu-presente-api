from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

from app.models.rol import Rol

if TYPE_CHECKING:
    from app.models.escuela import Escuela
    from app.models.curso import Curso

class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"

    idUsuario: Optional[int] = Field(default=None, primary_key=True)
    dni: str = Field(index=True, max_length=8)
    cuil: str = Field(max_length=11)
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)
    celular: str = Field(max_length=15)
    mailABC: str = Field(max_length=255)
    contrasena: str = Field(max_length=255)
    fechaNacimiento: Optional[date] = None
    escuelas: list["Escuela"] = Relationship(back_populates="usuarios", link_model=Rol)
    cursos: List["Curso"] = Relationship(back_populates="docente")
