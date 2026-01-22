from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import date


class ResponsableConParentesco(BaseModel):
    idResponsable: int
    nombre: str
    apellido: str
    dni: str
    telefono: Optional[str] = None
    correo_electronico: Optional[str] = None
    parentesco: str

    model_config = ConfigDict(from_attributes=True)


class AlumnoDetalleConResponsables(BaseModel):
    idAlumno: int
    idCurso: int
    nombre: str
    apellido: str
    dni: str
    fechaNac: date
    fechaIngreso: date
    direccion: Optional[str] = None

    responsables: List[ResponsableConParentesco] = []

    model_config = ConfigDict(from_attributes=True)
