from sqlmodel import Field, Relationship
from app.schemas.curso import CursoBase 


class Curso(CursoBase, table=True):
    idCurso: int | None = Field(default=None, primary_key=True)
    password: str
    idUsuario: int | None = Field(default=None,nullable=False, foreign_key="rol.idUsuario")
    CUE: str | None = Field(default=None,nullable=False, foreign_key="rol.CUE")

