from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING
from app.schemas.curso import CursoBase
from app.models.inscriptos import Inscriptos

if TYPE_CHECKING:
    from .alumno import Alumno

class Curso(CursoBase, table=True):
    idCurso: int | None = Field(default=None, primary_key=True)
    password: str
    CUE: str = Field(nullable=False, foreign_key="escuela.CUE")
    alumnos: list["Alumno"] = Relationship(back_populates="cursos", link_model=Inscriptos)
