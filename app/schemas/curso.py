# app/schemas/curso.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class CursoCreate(BaseModel):
    escuelaId: int
    nombre: str
    grado: Optional[str] = None
    division: Optional[str] = None
    turno: Optional[str] = None
    cicloLectivo: int

class CursoPublic(BaseModel):
    id: int = Field(alias="idCurso")
    escuelaId: int = Field(alias="idEscuela")

    nombre: str
    grado: Optional[str] = None
    division: Optional[str] = None
    turno: Optional[str] = None
    cicloLectivo: int

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
