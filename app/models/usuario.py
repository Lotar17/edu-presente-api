# app/models/usuario.py
from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship

from app.models.rol import Rol

if TYPE_CHECKING:
    from app.models.escuela import Escuela
    from app.models.curso import Curso


class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"

    idUsuario: Optional[int] = Field(default=None, primary_key=True)
    dni: str = Field(index=True)
    cuil: Optional[str] = None
    mailABC: Optional[str] = None

    contrasena: str
    celular: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None

    # many-to-many Usuario <-> Escuela vía Rol (ya lo tenías)
    escuelas: List["Escuela"] = Relationship(
        back_populates="usuarios",
        link_model=Rol
    )

    # ✅ NUEVO: 1 Usuario (docente) -> muchos Cursos
    cursos: List["Curso"] = Relationship(back_populates="docente")
