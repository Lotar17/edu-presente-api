from datetime import date
from sqlmodel import SQLModel, Field

from app.schemas.asistencia import AsistenciaBase


class Asistencia(AsistenciaBase, SQLModel, table=True):
    idCurso: int = Field(foreign_key="curso.idCurso", primary_key=True, index=True)
    idAlumno: int = Field(foreign_key="alumno.idAlumno", primary_key=True, index=True)
    fecha: date = Field(primary_key=True, index=True)