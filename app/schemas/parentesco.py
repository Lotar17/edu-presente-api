
from pydantic import Field
from sqlmodel import SQLModel


class ParentescoBase(SQLModel):
    parentesco: str = Field(max_length=50)

class ParentescoPublic(ParentescoBase):
    idAlumno: int
    idResponsable: int

class ParentescoCreate(ParentescoBase):
    idAlumno: int
    idResponsable: int
