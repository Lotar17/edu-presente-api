from datetime import date
from sqlmodel import SQLModel, Field


class Inscriptos(SQLModel, table=True):
    idCurso: int = Field(foreign_key="curso.idCurso", primary_key=True)
    idAlumno: int = Field(foreign_key="alumno.idAlumno", primary_key=True)

    fechaAlta: date = Field(default_factory=date.today)
    fechaBaja: date | None = Field(default=None)

    # opcional según tu DER (lo dejé como string simple)
    estado: str = Field(default="Activo", max_length=20)
