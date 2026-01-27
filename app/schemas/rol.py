from enum import Enum
from sqlmodel import SQLModel, Field

class RolEstado(Enum):
    Activo = "Activo"
    Pendiente = "Pendiente"
    Rechazado = "Rechazado"

class RolDescripcion(Enum):
    Director = "Director"
    Docente = "Docente"
    Administrador = "Administrador"
    Asistente = "Asistente"


class RolBase(SQLModel):
    descripcion: RolDescripcion = Field()
    estado: RolEstado = Field(default=RolEstado.Pendiente)

class RolPublic(RolBase):
    pass

class RolCreate(RolBase):
    pass

class RolUpdate(SQLModel):
    descripcion: str | None = None
