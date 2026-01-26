# app/models/curso.py
from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer

if TYPE_CHECKING:
    from app.models.escuela import Escuela
    from app.models.alumno import Alumno
    from app.models.usuario import Usuario


class Curso(SQLModel, table=True):
    __tablename__ = "curso"

    idCurso: Optional[int] = Field(default=None, primary_key=True)
    idEscuela: int = Field(index=True, foreign_key="escuela.idEscuela")

    # ✅ NUEVO: docente asignado al curso
    # (nullable para permitir curso sin docente por ahora)
    idDocente: Optional[int] = Field(
        default=None,
        index=True,
        foreign_key="usuario.idUsuario"
    )

    nombre: str = Field(max_length=50)
    division: str = Field(max_length=50)

    cicloLectivo: int = Field(sa_column=Column("ciclo_lectivo", Integer, nullable=False))

    escuela: Optional["Escuela"] = Relationship(back_populates="cursos")
    alumnos: List["Alumno"] = Relationship(back_populates="curso")

    # ✅ NUEVO: relación con Usuario (docente)
    docente: Optional["Usuario"] = Relationship(back_populates="cursos")
