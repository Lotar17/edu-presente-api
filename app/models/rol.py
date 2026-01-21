from typing import Optional
from sqlmodel import Field, table
from app.schemas.rol import RolBase

class Rol(RolBase, table=True):
    idRol: Optional[int] = Field(default=None, primary_key=True)
    idUsuario: int | None = Field(default=None, foreign_key="usuario.idUsuario", primary_key=True)
    idEscuela: int | None = Field(default=None, foreign_key="escuela.idEscuela", primary_key=True)
