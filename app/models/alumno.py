# app/models/alumno.py
from typing import Optional, TYPE_CHECKING, List
from datetime import date

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Date

from app.models.alumno_responsable import AlumnoResponsable

if TYPE_CHECKING:
    from app.models.responsable import Responsable
    from app.models.curso import Curso


class Alumno(SQLModel, table=True):
    __tablename__ = "alumno"

    idAlumno: Optional[int] = Field(default=None, primary_key=True)

    idCurso: int = Field(index=True, foreign_key="curso.idCurso")

    nombre: str
    apellido: str
    dni: str

    fechaNac: date = Field(sa_column=Column("fecha_nacimiento", Date, nullable=False))
    fechaIngreso: date = Field(sa_column=Column("fecha_ingreso", Date, nullable=False))

    direccion: Optional[str] = None

    # ✅ Relación many-to-many con Responsable
    responsables: List["Responsable"] = Relationship(
        back_populates="alumnos",
        link_model=AlumnoResponsable
    )

    # ✅ Relación curso (many-to-one)
    curso: Optional["Curso"] = Relationship(back_populates="alumnos")
