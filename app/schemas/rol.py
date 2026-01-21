from sqlmodel import SQLModel, Field

class RolBase(SQLModel):
    descripcion: str = Field(max_length=255)
    estado: str = Field(default="Pendiente", max_length=20)

class RolPublic(RolBase):
    idRol: int
    idUsuario: int
    idEscuela: int

class RolCreate(RolBase):
    idUsuario: int
    idEscuela: int

class RolUpdate(SQLModel):
    descripcion: str | None = None
    estado: str | None = None
