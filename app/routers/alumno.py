from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from app.dependencies import SessionDep
from app.models.alumno import Alumno
from app.models.responsable import Responsable
from app.models.alumno_responsable import AlumnoResponsable

from app.schemas.alumno import AlumnoCreate, AlumnoPublic
from app.schemas.alumno_responsables import (
    AlumnoDetalleConResponsables,
    ResponsableConParentesco,
)

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])


# --------------------------------------------------
# LISTAR ALUMNOS (opcional por curso)
# --------------------------------------------------
@router.get("/", response_model=list[AlumnoPublic])
def list_alumnos(
    session: SessionDep,
    cursoId: int | None = Query(default=None),
):
    stmt = select(Alumno)
    if cursoId is not None:
        stmt = stmt.where(Alumno.idCurso == cursoId)
    return session.exec(stmt).all()


# --------------------------------------------------
# OBTENER ALUMNO SIMPLE
# --------------------------------------------------
@router.get("/{alumno_id}", response_model=AlumnoPublic)
def get_alumno(session: SessionDep, alumno_id: int):
    alumno = session.get(Alumno, alumno_id)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return alumno


# --------------------------------------------------
# OBTENER ALUMNO + RESPONSABLES + PARENTESCO ✅
# --------------------------------------------------
@router.get("/{alumno_id}/detalle", response_model=AlumnoDetalleConResponsables)
def get_alumno_detalle(session: SessionDep, alumno_id: int):
    alumno = session.get(Alumno, alumno_id)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    # JOIN responsable + tabla puente para traer parentesco
    rows = session.exec(
        select(Responsable, AlumnoResponsable.parentesco)
        .join(
            AlumnoResponsable,
            AlumnoResponsable.idResponsable == Responsable.idResponsable,
        )
        .where(AlumnoResponsable.idAlumno == alumno_id)
    ).all()

    responsables = [
        ResponsableConParentesco(
            idResponsable=r.idResponsable,
            nombre=r.nombre,
            apellido=r.apellido,
            dni=r.dni,
            telefono=r.telefono,
            correo_electronico=r.correo_electronico,
            parentesco=parentesco,
        )
        for (r, parentesco) in rows
    ]

    return AlumnoDetalleConResponsables(
        idAlumno=alumno.idAlumno,
        idCurso=alumno.idCurso,
        nombre=alumno.nombre,
        apellido=alumno.apellido,
        dni=alumno.dni,
        fechaNac=alumno.fechaNac,
        fechaIngreso=alumno.fechaIngreso,
        direccion=alumno.direccion,
        responsables=responsables,
    )


# --------------------------------------------------
# CREAR ALUMNO
# --------------------------------------------------
@router.post("/", response_model=AlumnoPublic, status_code=201)
def create_alumno(session: SessionDep, data: AlumnoCreate):
    alumno = Alumno(
        idCurso=data.cursoId,
        nombre=data.nombre,
        apellido=data.apellido,
        dni=data.dni,
        fechaNac=data.fechaNac,
        fechaIngreso=data.fechaIngreso,
        direccion=data.direccion,
    )

    session.add(alumno)
    session.commit()
    session.refresh(alumno)
    return alumno


# --------------------------------------------------
# ELIMINAR ALUMNO
# --------------------------------------------------
@router.delete("/{alumno_id}", status_code=204)
def delete_alumno(session: SessionDep, alumno_id: int):
    alumno = session.get(Alumno, alumno_id)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    # borrar vínculos con responsables primero (FK safe)
    links = session.exec(
        select(AlumnoResponsable).where(
            AlumnoResponsable.idAlumno == alumno_id
        )
    ).all()
    for l in links:
        session.delete(l)

    session.delete(alumno)
    session.commit()
    return None
