from sqlmodel import SQLModel, Field

class UsuarioBase(SQLModel):
    dni: str = Field(index=True, max_length=8)
    cuil: str = Field(index=True, max_length=11)
    celular: str = Field(max_length=15)
    mailABC: str = Field(index=True)

class UsuarioPublic(UsuarioBase):
    idUsuario: int

class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioUpdate(SQLModel):
    dni: str | None = None
    cuil: str | None = None
    celular: str | None =None 
    mailABC: str | None = None
    contrasena: str|None = None

