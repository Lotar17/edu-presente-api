# app/schemas/alumno_responsables.py
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import date


class CursoLite(BaseModel):
    idCurso: int
    nombre: str
    division: str
    cicloLectivo: int

    model_config = ConfigDict(from_attributes=True)


class ResponsableConParentesco(BaseModel):
    idResponsable: int
    nombre: str
    apellido: str
    dni: str
    telefono: Optional[str] = None
    correo_electronico: Optional[str] = None
    direccion: Optional[str] = None  # ✅ para mostrar "DIRECCIÓN" (si existe en Responsable)
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

    # ✅ NUEVO: curso completo para mostrar "5to Año - División A"
    curso: Optional[CursoLite] = None

    # ✅ NUEVO: responsable principal para la UI (el primero)
    responsablePrincipal: Optional[ResponsableConParentesco] = None

    # ✅ lista completa por si la necesitás después
    responsables: List[ResponsableConParentesco] = []

    model_config = ConfigDict(from_attributes=True)
