from datetime import date
from enum import Enum
from sqlmodel import SQLModel, Field

class AsistenciaEstado(Enum):
    Presente = "Presente"
    Ausente = "Ausente"
    Tarde = "Tarde"

class AsistenciaBase(SQLModel):
    estado: AsistenciaEstado = Field()
    lluvia: bool = Field()

class AsistenciaPublic(AsistenciaBase):
    idAlumno: int


class AsistenciaCreate(AsistenciaBase):
    fecha: date 
    idAlumno: int
    idCurso: int
