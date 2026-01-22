from typing import Optional
from sqlmodel import SQLModel, Field


class AlumnoResponsable(SQLModel, table=True):
    __tablename__ = "alumno_responsable"

    # tabla puente
    idAlumno: int = Field(foreign_key="alumno.idAlumno", primary_key=True)
    idResponsable: int = Field(foreign_key="responsable.idResponsable", primary_key=True)

    # atributo extra de la relación
    parentesco: str = Field(index=True, max_length=50)
