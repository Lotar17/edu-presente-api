from sqlmodel import SQLModel, Field


class CursoBase(SQLModel):
    nombre: str = Field(max_length=255)
    cicloLectivo: str = Field(max_length=50)
    divison: str = Field(max_length=50)


class CursoPublic(CursoBase):
    idCurso: int

class CursoCreate(CursoBase):
    idUsuario: int
    CUE: str
    password: str 

class CursoUpdate(SQLModel):
    nombre: str | None = None
    cicloLectivo: str | None = None
    division: str | None = None
    password: str | None = None
    idUsuario: str | None = None
    CUE: str | None = None


