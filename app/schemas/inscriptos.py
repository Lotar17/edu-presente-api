from datetime import date
from sqlmodel import SQLModel, Field


class InscriptosBase(SQLModel):
    fechaAlta: date
    fechaBaja: date | None = None
    estado: str = Field(default="Activo", max_length=20)


class InscriptosCreate(SQLModel):
    idCurso: int
    idAlumno: int
    # opcionales
    fechaAlta: date | None = None
    estado: str = "Activo"


class InscriptosPublic(InscriptosBase):
    idCurso: int
    idAlumno: int
