from sqlmodel import Field, table
from app.schemas.rol import RolBase

class Rol(RolBase, table=True):
    idUsuario: int | None = Field(default=None, foreign_key="usuario.idUsuario", primary_key=True)
    CUE: str | None = Field(default=None, foreign_key="escuela.CUE", primary_key=True)
