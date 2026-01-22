from typing import Optional
from pydantic import BaseModel, ConfigDict


class ResponsableCreate(BaseModel):
    nombre: str
    apellido: str
    dni: str
    telefono: Optional[str] = None
    correo_electronico: Optional[str] = None


class ResponsableUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    dni: Optional[str] = None
    telefono: Optional[str] = None
    correo_electronico: Optional[str] = None


class ResponsablePublic(BaseModel):
    idResponsable: int
    nombre: str
    apellido: str
    dni: str
    telefono: Optional[str] = None
    correo_electronico: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class VincularResponsableRequest(BaseModel):
    idAlumno: int
    idResponsable: int
    parentesco: str  # "Madre", "Padre", "Tutor", etc.
