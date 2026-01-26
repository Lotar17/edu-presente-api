# app/schemas/curso.py
from typing import Optional
from sqlmodel import SQLModel, Field


class CursoCreate(SQLModel):
    escuelaId: int  # lo que manda el front
    nombre: str = Field(max_length=50)
    division: str = Field(max_length=50)
    cicloLectivo: int
    docenteId: Optional[int] = None


class CursoUpdate(SQLModel):
    escuelaId: Optional[int] = None
    nombre: Optional[str] = None
    division: Optional[str] = None
    cicloLectivo: Optional[int] = None
    docenteId: Optional[int] = None


class CursoPublic(SQLModel):
    idCurso: int
    idEscuela: int
    nombre: str
    division: str
    cicloLectivo: int
    idDocente: Optional[int] = None
