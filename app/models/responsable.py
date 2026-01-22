from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from app.models.alumno_responsable import AlumnoResponsable

if TYPE_CHECKING:
    from app.models.alumno import Alumno


class Responsable(SQLModel, table=True):
    __tablename__ = "responsable"

    idResponsable: Optional[int] = Field(default=None, primary_key=True)

    nombre: str
    apellido: str
    dni: str = Field(index=True, max_length=20)
    telefono: Optional[str] = Field(default=None, max_length=30)
    correo_electronico: Optional[str] = Field(default=None, max_length=120)

    alumnos: list["Alumno"] = Relationship(
        back_populates="responsables",
        link_model=AlumnoResponsable
    )
