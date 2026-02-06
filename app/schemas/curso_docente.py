from datetime import date
from sqlmodel import SQLModel, Field

class CursoDocenteCreate(SQLModel):
    idUsuario: int
    tipo: str = Field(default="Titular")  # Titular | Suplente
    fechaDesde: date | None = None
    fechaHasta: date | None = None

class CursoDocentePublic(SQLModel):
    idCurso: int
    idUsuario: int
    tipo: str
    fechaDesde: date | None = None
    fechaHasta: date | None = None
