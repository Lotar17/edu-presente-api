from sqlmodel import SQLModel, Field
from datetime import date


class ResponsableBase(SQLModel):
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)
    dni: str = Field(index=True, max_length=8)
    fecha_nac: date = Field(nullable=False)
    email: str = Field(index=True, max_length=255)
    nro_celular: str = Field(max_length=15)
    direccion: str = Field(max_length=100)

class ResonsablePublic(ResponsableBase):
    idResponsable: int

class ResponsableCreate(ResponsableBase):
    idAlumno: int

class ResponsableUpdate(SQLModel):
    nombre: str | None = None
    apellido: str | None = None
    dni: str | None = None
    fecha_nac: date | None = None
    nro_celular: str | None = None
    direccion: str | None = None
    email: str | None = None

