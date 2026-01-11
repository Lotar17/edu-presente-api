from sqlmodel import Field

from app.schemas.usuario import UsuarioBase 


class Usuario(UsuarioBase, table=True):
    idUsuario: int | None = Field(default=None, primary_key=True)
    contrasena: str


