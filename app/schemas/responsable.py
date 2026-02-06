from sqlmodel import SQLModel, Field
from datetime import date


# BASE (TODOS OBLIGATORIOS)

class ResponsableBase(SQLModel):
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)

    dni: str = Field(index=True, max_length=20)
    fecha_nacimiento: date

    email: str = Field(index=True, max_length=255)
    nro_celular: str = Field(max_length=15)

    direccion: str = Field(max_length=100)


# RESPUESTA

class ResponsablePublic(ResponsableBase):
    idResponsable: int


# CREATE

class ResponsableCreate(ResponsableBase):
    pass


# UPDATE

class ResponsableUpdate(SQLModel):
    nombre: str | None = None
    apellido: str | None = None
    dni: str | None = None
    fecha_nacimiento: date | None = None

    email: str | None = None
    nro_celular: str | None = None
    direccion: str | None = None
