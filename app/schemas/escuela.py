from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, Field


class EscuelaBase(BaseModel):
    cue: Optional[str] = None
    nombre: str
    numero: Union[str, int]
    nivel_educativo: str
    turno: str
    matricula: Optional[int] = None
    direccion: str
    codigo_postal: str
    codigo_provincial: Optional[str] = None
    telefono: Optional[str] = None
    correo_electronico: Optional[str] = None
    provincia: str
    localidad: str


class EscuelaCreate(EscuelaBase):
    pass


class EscuelaPublic(EscuelaBase):
    idEscuela: int
    model_config = ConfigDict(from_attributes=True)


class EscuelaUpdate(BaseModel):
    cue: Optional[str] = None
    nombre: Optional[str] = None
    numero: Optional[Union[str, int]] = None
    nivel_educativo: Optional[str] = None
    turno: Optional[str] = None
    matricula: Optional[int] = None
    direccion: Optional[str] = None
    codigo_postal: Optional[str] = None
    codigo_provincial: Optional[str] = None
    telefono: Optional[str] = None
    correo_electronico: Optional[str] = None
    provincia: Optional[str] = None
    localidad: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
