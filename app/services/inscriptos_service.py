from datetime import date
from fastapi import HTTPException
from sqlmodel import select

from app.dependencies import SessionDep
from app.models.inscriptos import Inscriptos
from app.models.alumno import Alumno
from app.services.curso_service import get_one_curso


# =========================
# INSCRIBIR
# =========================
def inscribir_alumno(idCurso: int, idAlumno: int, db: SessionDep):
    curso = get_one_curso(idCurso=idCurso, db=db)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    alumno = db.get(Alumno, idAlumno)
    if alumno is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    existente = db.get(Inscriptos, (idCurso, idAlumno))
    if existente:
        raise HTTPException(status_code=400, detail="El alumno ya está inscripto en el curso")

    inscripcion = Inscriptos(
        idCurso=idCurso,
        idAlumno=idAlumno,
        fechaAlta=date.today(),
        estado="Activo"
    )

    db.add(inscripcion)
    db.commit()
    db.refresh(inscripcion)
    return inscripcion


# =========================
# BAJA / DESINSCRIBIR
# =========================
def desinscribir_alumno(idCurso: int, idAlumno: int, db: SessionDep):
    inscripcion = db.get(Inscriptos, (idCurso, idAlumno))
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")

    inscripcion.estado = "Inactivo"
    inscripcion.fechaBaja = date.today()

    db.add(inscripcion)
    db.commit()
    db.refresh(inscripcion)
    return inscripcion


# =========================
# LISTAR INSCRIPTOS DE UN CURSO
# =========================
def get_inscriptos_by_curso(idCurso: int, db: SessionDep):
    curso = get_one_curso(idCurso=idCurso, db=db)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    stmt = (
        select(Alumno)
        .join(Inscriptos, Inscriptos.idAlumno == Alumno.idAlumno)
        .where(
            Inscriptos.idCurso == idCurso,
            Inscriptos.estado == "Activo"
        )
    )

    return db.exec(stmt).all()
