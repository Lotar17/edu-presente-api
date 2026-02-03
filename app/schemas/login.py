from pydantic import BaseModel
from typing import List

class LoginRequest(BaseModel):
    dni: str
    password: str


class OpcionRol(BaseModel):
    idUsuario: int | None
    descripcion: str
    CUE: str
    nombre_escuela: str


class LoginResponse(BaseModel):
    mensaje: str
    usuario_id: int | None
    nombre: str
    apellido: str
    roles_disponibles: List[OpcionRol]
