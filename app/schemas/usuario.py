from sqlmodel import SQLModel, Field
from app.schemas.rol import RolDescripcion

class UsuarioBase(SQLModel):
    dni: str = Field(index=True, max_length=8)
    cuil: str = Field(index=True, max_length=11)
    celular: str = Field(max_length=15)
    mailABC: str = Field(index=True)
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)

class UsuarioPublic(UsuarioBase):
    idUsuario: int

class UsuarioCreate(UsuarioBase):
    contrasena: str
    rol: RolDescripcion
    escuelasCUE: list[str]

class UsuarioUpdate(SQLModel):
    dni: str | None = None
    cuil: str | None = None
    celular: str | None =None 
    mailABC: str | None = None
    contrasena: str|None = None

