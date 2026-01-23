from typing import Optional
from sqlmodel import SQLModel, Field


class Rol(SQLModel, table=True):
    __tablename__ = "rol"

    # PK compuesta para tabla puente usuario-escuela
    idUsuario: int = Field(foreign_key="usuario.idUsuario", primary_key=True)
    idEscuela: int = Field(foreign_key="escuela.idEscuela", primary_key=True)

    descripcion: str  # "Docente", "Director", "Admin", etc.
    estado: str = "Activo"  # Activo | Pendiente | Rechazado
