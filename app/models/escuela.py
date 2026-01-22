# app/models/escuela.py
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from app.models.rol import Rol

if TYPE_CHECKING:
    from app.models.usuario import Usuario

class Escuela(SQLModel, table=True):
    __tablename__ = "escuela"

    idEscuela: Optional[int] = Field(default=None, primary_key=True)

    cue: Optional[str] = Field(default=None, index=True)
    nombre: str
    numero: Optional[str] = None
    nivel_educativo: Optional[str] = None
    turno: Optional[str] = None
    matricula: Optional[int] = None
    direccion: Optional[str] = None
    codigo_postal: Optional[str] = None
    codigo_provincial: Optional[str] = None
    telefono: Optional[str] = None
    correo_electronico: Optional[str] = None
    provincia: Optional[str] = None
    localidad: Optional[str] = None

    usuarios: list["Usuario"] = Relationship(
        back_populates="escuelas",
        link_model=Rol
    )
