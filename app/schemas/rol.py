from enum import Enum
from sqlmodel import SQLModel, Field

class RolEstado(Enum):
    Activo = "Activo"
    Pendiente = "Pendiente"
    Rechazado = "Rechazado"


class RolBase(SQLModel):
    descripcion: str = Field(max_length=255)
    estado: RolEstado = Field(default=RolEstado.Pendiente)

class RolPublic(RolBase):
    pass

class RolCreate(RolBase):
    pass

class RolUpdate(SQLModel):
    descripcion: str | None = None
