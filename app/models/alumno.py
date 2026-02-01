from typing import TYPE_CHECKING
from app.models.asistencia import Asistencia
from app.models.parentesco import Parentesco
from app.schemas.alumno import AlumnoBase
from sqlmodel import Field, Relationship

if TYPE_CHECKING:
    from .curso import Curso
    from .responsable import Responsable

class Alumno(AlumnoBase, table=True):
    idAlumno: int | None = Field(default=None, primary_key=True)
    cursos: list["Curso"] = Relationship(back_populates="alumnos", link_model=Asistencia)
    responsables: list["Responsable"] = Relationship(back_populates="alumnos", link_model=Parentesco)
