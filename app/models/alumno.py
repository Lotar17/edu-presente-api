from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.schemas.alumno import AlumnoBase
from app.models.parentesco import Parentesco
from app.models.inscriptos import Inscriptos

if TYPE_CHECKING:
    from .curso import Curso
    from .responsable import Responsable


class Alumno(AlumnoBase, table=True):
    idAlumno: int | None = Field(default=None, primary_key=True)

    # ✅ MATRÍCULA REAL
    # Cursos a los que el alumno está inscripto, independientemente de la asistencia
    cursos: list["Curso"] = Relationship(
        back_populates="alumnos",
        link_model=Inscriptos
    )

    # ✅ Responsables por parentesco
    responsables: list["Responsable"] = Relationship(
        back_populates="alumnos",
        link_model=Parentesco
    )
