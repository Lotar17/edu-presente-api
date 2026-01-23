from typing import Optional, Union
from pydantic import BaseModel, Field, ConfigDict

<<<<<<< HEAD
class EscuelaBase(BaseModel):
    cue: str  
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
=======


class EscuelaBase(SQLModel):
    nombre: str = Field(max_length=255)
    numero: int = Field()
    nivel_educativo: str = Field(max_length=255)
    turno: str = Field(max_length=255)
    matricula: str = Field(max_length=255)
    direccion: str = Field(max_length=255)
    codigo_postal: str = Field(max_length=255)
    codigo_provincial: str = Field(max_length=255)
    telefono: str = Field(max_length=15)
    correo_electronico: str = Field(index=True,max_length=255)

class EscuelaPublic(EscuelaBase):
    pass
>>>>>>> dev

class EscuelaCreate(EscuelaBase):
    CUE: str = Field(min_length=9, max_length=9)

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