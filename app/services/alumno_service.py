from typing import Annotated

from fastapi import Query, HTTPException
from sqlmodel import select

from app.dependencies import SessionDep
from app.models.alumno import Alumno
from app.models.inscriptos import Inscriptos
from app.schemas.alumno import AlumnoCreate, AlumnoUpdate
from app.services.curso_service import get_one_curso



# GET ALL

def get_all_alumnos(db: SessionDep, offset: int, limit: Annotated[int, Query(le=100)]):
    alumnos = db.exec(select(Alumno).offset(offset).limit(limit)).all()
    return alumnos



# GET BY CURSO (INSCRIPTOS)

def get_alumnos_by_curso(idCurso: int, db: SessionDep):
    """
    Devuelve los alumnos INSCRIPTOS a un curso (matrícula),
    sin depender de que exista asistencia.
    """
    curso = get_one_curso(idCurso=idCurso, db=db)
    if curso is None:
        raise Exception("El curso ingresado no existe")

    stmt = (
        select(Alumno)
        .join(Inscriptos, Inscriptos.idAlumno == Alumno.idAlumno)
        .where(Inscriptos.idCurso == idCurso)
    )
    return db.exec(stmt).all()



# HELPERS

def get_alumno_by_dni(db: SessionDep, dni: str):
    stmt = select(Alumno).where(Alumno.dni == dni)
    return db.exec(stmt).first()


def get_one_alumno(idAlumno: int, db: SessionDep):
    return db.get(Alumno, idAlumno)



# CREATE

def add_alumno(db: SessionDep, alumno_in: AlumnoCreate):
    dni = (alumno_in.dni or "").strip()

    if not dni:
        raise HTTPException(status_code=400, detail="El DNI del alumno es obligatorio")

    existente = get_alumno_by_dni(db, dni)
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un alumno con ese DNI")

    # Creamos Alumno ignorando idCurso (la matrícula va por Inscriptos)
    data = alumno_in.model_dump(exclude={"idCurso"})
    data["dni"] = dni  # aseguramos el valor limpio

    db_alumno = Alumno.model_validate(data)

    db.add(db_alumno)
    db.commit()
    db.refresh(db_alumno)

    # Inscripción automática si viene idCurso
    if getattr(alumno_in, "idCurso", None) and alumno_in.idCurso > 0:
        curso = get_one_curso(idCurso=alumno_in.idCurso, db=db)
        if curso is None:
            raise HTTPException(status_code=404, detail="El curso ingresado no existe")

        ya = db.get(Inscriptos, (alumno_in.idCurso, db_alumno.idAlumno))
        if not ya:
            insc = Inscriptos(idCurso=alumno_in.idCurso, idAlumno=db_alumno.idAlumno)
            db.add(insc)
            db.commit()

    db.refresh(db_alumno)
    return db_alumno



# UPDATE

def update_alumno(alumno_existente: Alumno, alumno_nuevo: AlumnoUpdate, db: SessionDep):
    alumno_data = alumno_nuevo.model_dump(exclude_unset=True)
    alumno_existente.sqlmodel_update(alumno_data)
    db.add(alumno_existente)
    db.commit()
    db.refresh(alumno_existente)
    return alumno_existente



# DELETE

def delete_alumno(db: SessionDep, alumno: Alumno):
    db.delete(alumno)
    db.commit()
