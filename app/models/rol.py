from typing import Optional
from sqlmodel import SQLModel, Field

class Rol(SQLModel, table=True):
    __tablename__ = "rol"

    idRol: Optional[int] = Field(default=None, primary_key=True)

    idUsuario: int = Field(foreign_key="usuario.idUsuario")
    idEscuela: int = Field(foreign_key="escuela.idEscuela")

    descripcion: str  # "Docente", "Director", "Admin"
    estado: str = "Activo"  # Activo | Pendiente | Rechazado
