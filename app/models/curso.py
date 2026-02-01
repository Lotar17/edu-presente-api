from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING
from app.models.asistencia import Asistencia
from app.schemas.curso import CursoBase 

if TYPE_CHECKING:
    from .alumno import Alumno

class Curso(CursoBase, table=True):
    idCurso: int | None = Field(default=None, primary_key=True)
    password: str
    idUsuario: int | None = Field(default=None,nullable=False, foreign_key="rol.idUsuario")
    CUE: str | None = Field(default=None,nullable=False, foreign_key="rol.CUE")
    alumnos: list["Alumno"] = Relationship(back_populates="cursos", link_model=Asistencia)

