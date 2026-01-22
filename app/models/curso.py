# app/models/curso.py
from typing import Optional
from sqlmodel import SQLModel, Field

class Curso(SQLModel, table=True):
    idCurso: Optional[int] = Field(default=None, primary_key=True)
    idEscuela: int = Field(index=True, foreign_key="escuela.idEscuela")

    nombre: str
    grado: Optional[str] = None
    division: Optional[str] = None
    turno: Optional[str] = None

    cicloLectivo: int  # ✅ tu front lo exige
