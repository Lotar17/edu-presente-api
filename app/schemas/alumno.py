from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date

class AlumnoCreate(BaseModel):
    cursoId: int
    nombre: str
    apellido: str
    dni: str
    fechaNac: date
    fechaIngreso: date
    direccion: Optional[str] = None

class AlumnoPublic(BaseModel):
    id: int = Field(alias="idAlumno")
    cursoId: int = Field(alias="idCurso")
    nombre: str
    apellido: str
    dni: str
    fechaNac: date
    fechaIngreso: date
    direccion: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
