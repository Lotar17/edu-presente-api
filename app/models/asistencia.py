from datetime import date
from sqlmodel import Field, table

from app.schemas.asistencia import AsistenciaBase

class Asistencia(AsistenciaBase, table=True):
    idCurso: int | None = Field(default=None, foreign_key="curso.idCurso", primary_key=True)
    idAlumno: int | None = Field(default=None, foreign_key="alumno.idAlumno", primary_key=True)
    fecha: date = Field(primary_key=True)
