from typing import Optional, List
from pydantic import BaseModel

class AdminUsuarioRow(BaseModel):
    idUsuario: int
    dni: str
    nombre: str
    apellido: str
    mailABC: str | None = None
    cuil: str | None = None
    celular: str | None = None
    fechaNacimiento: date | None = None
    roles: list[str]
    escuelas: list[str]
    estados: list[str]

