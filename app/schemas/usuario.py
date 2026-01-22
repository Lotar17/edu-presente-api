from datetime import date
from sqlmodel import SQLModel, Field

class UsuarioBase(SQLModel):
    dni: str = Field(index=True, max_length=8)
    cuil: str = Field(index=True, max_length=11)
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)
    celular: str | None = Field(default=None, max_length=20)
    mailABC: str | None = Field(default=None, max_length=100)
    fechaNacimiento: date | None = None

class UsuarioPublic(UsuarioBase):
    idUsuario: int

class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioUpdate(SQLModel):
    dni: str | None = None
    cuil: str | None = None
    nombre: str | None = None 
    apellido: str | None = None
    celular: str | None =None 
    mailABC: str | None = None
    contrasena: str|None = None
    fechaNacimiento: date | None = None

