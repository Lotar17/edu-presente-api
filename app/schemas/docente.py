# app/schemas/docente.py
from typing import Optional, List
from sqlmodel import SQLModel


class CursoAsignadoPublic(SQLModel):
    escuelaId: int
    escuelaNombre: str

    cursoId: int
    cursoNombre: str

    alumnosCount: int

    # opcionales para tu UI (si no existen en DB)
    turno: Optional[str] = None
    estado: Optional[str] = "Activo"
    icon: Optional[str] = "groups"


class CursoOption(SQLModel):
    cursoId: int
    cursoNombre: str
    division: str
    cicloLectivo: int


class EscuelaCursosPublic(SQLModel):
    escuelaId: int
    escuelaNombre: str
    cursos: List[CursoOption]
