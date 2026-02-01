from sqlmodel import Field, table
from app.schemas.parentesco import ParentescoBase


class Parentesco(ParentescoBase, table=True):
    idAlumno: int | None = Field(default=None, foreign_key="alumno.idAlumno", primary_key=True)
    idResponsable: int | None = Field(default=None, foreign_key="responsable.idResponsable", primary_key=True)
