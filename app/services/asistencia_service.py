# app/services/asistencia_service.py
from datetime import date
from typing import Annotated, Optional, Iterable

from fastapi import HTTPException, Query
from sqlmodel import select, desc

from app.dependencies import SessionDep
from app.models.asistencia import Asistencia
from app.models.alumno import Alumno
from app.services.curso_service import get_one_curso
from app.schemas.asistencia import AsistenciaCreate


# Helpers


def get_one_asistencia(db: SessionDep, idCurso: int, idAlumno: int, fecha: date) -> Optional[Asistencia]:
    return db.get(Asistencia, (idCurso, idAlumno, fecha))


def ensure_curso_exists(db: SessionDep, idCurso: int):
    curso = get_one_curso(idCurso=idCurso, db=db)
    if curso is None:
        raise HTTPException(status_code=404, detail="El curso ingresado no existe")
    return curso


def ensure_alumno_exists(db: SessionDep, idAlumno: int):
    alumno = db.get(Alumno, idAlumno)
    if alumno is None:
        raise HTTPException(status_code=404, detail="El alumno ingresado no existe")
    return alumno


def ensure_alumnos_exist(db: SessionDep, ids_alumnos: Iterable[int]):
    """
    Valida que todos los alumnos existan.
    Evita N queries (una por alumno).
    """
    ids = list({int(x) for x in ids_alumnos})
    if not ids:
        return

    stmt = select(Alumno.idAlumno).where(Alumno.idAlumno.in_(ids))
    existentes = set(db.exec(stmt).all())
    faltantes = [i for i in ids if i not in existentes]
    if faltantes:
        raise HTTPException(status_code=404, detail=f"Alumnos inexistentes: {faltantes}")


# Create / Upsert (uno)


def upsert_asistencia(db: SessionDep, payload: AsistenciaCreate) -> Asistencia:
    """
    Crea o actualiza (upsert) una asistencia por PK compuesta:
    (idCurso, idAlumno, fecha)
    """
    ensure_curso_exists(db, payload.idCurso)
    ensure_alumno_exists(db, payload.idAlumno)

    existente = get_one_asistencia(db, payload.idCurso, payload.idAlumno, payload.fecha)

    if existente:
        existente.estado = payload.estado
        existente.lluvia = payload.lluvia
        db.add(existente)
        db.commit()
        db.refresh(existente)
        return existente

    nueva = Asistencia.model_validate(payload.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


# Bulk Upsert (recomendado)


def upsert_asistencias_bulk(db: SessionDep, payloads: list[AsistenciaCreate]) -> list[Asistencia]:
    """
    Upsert masivo en una sola transacción.
    - Valida curso una vez por cada idCurso presente.
    - Valida alumnos en lote.
    - Hace commit 1 vez.
    """
    if not payloads:
        return []

    cursos_ids = list({p.idCurso for p in payloads})
    for cid in cursos_ids:
        ensure_curso_exists(db, cid)

    ensure_alumnos_exist(db, [p.idAlumno for p in payloads])

    out: list[Asistencia] = []

    for p in payloads:
        existente = get_one_asistencia(db, p.idCurso, p.idAlumno, p.fecha)
        if existente:
            existente.estado = p.estado
            existente.lluvia = p.lluvia
            db.add(existente)
            out.append(existente)
        else:
            nueva = Asistencia.model_validate(p.model_dump())
            db.add(nueva)
            out.append(nueva)

    db.commit()
    for row in out:
        db.refresh(row)

    return out


# Reads


def get_asistencias_by_curso_fecha(db: SessionDep, idCurso: int, fecha: date):
    """
    Devuelve todas las asistencias registradas para un curso en una fecha.
    """
    ensure_curso_exists(db, idCurso)

    stmt = select(Asistencia).where(
        Asistencia.idCurso == idCurso,
        Asistencia.fecha == fecha,
    )
    return db.exec(stmt).all()


def get_asistencias_by_curso(db: SessionDep, idCurso: int, offset: int, limit: Annotated[int, Query(le=200)]):
    """
    Historial de asistencias de un curso (todas las fechas).
    """
    ensure_curso_exists(db, idCurso)

    stmt = (
        select(Asistencia)
        .where(Asistencia.idCurso == idCurso)
        .order_by(Asistencia.fecha.desc())
        .offset(offset)
        .limit(limit)
    )
    return db.exec(stmt).all()


def get_asistencias_by_alumno(db: SessionDep, idAlumno: int, offset: int = 0, limit: int = 200):
    """
    Historial de asistencias de un alumno (todas las fechas, todos los cursos).
    """
    ensure_alumno_exists(db, idAlumno)

    stmt = (
        select(Asistencia)
        .where(Asistencia.idAlumno == idAlumno)
        .order_by(desc(Asistencia.fecha))
        .offset(offset)
        .limit(limit)
    )
    return db.exec(stmt).all()


def get_asistencias_by_curso_alumno(
    db: SessionDep,
    idCurso: int,
    idAlumno: int,
    anio: Optional[int] = None,
    offset: int = 0,
    limit: int = 200,
):
    """
    ✅ Historial de asistencias para un alumno dentro de un curso.
    (Opcional) filtra por año.
    """
    ensure_curso_exists(db, idCurso)
    ensure_alumno_exists(db, idAlumno)

    stmt = select(Asistencia).where(
        Asistencia.idCurso == idCurso,
        Asistencia.idAlumno == idAlumno,
    )

    if anio:
        desde = date(anio, 1, 1)
        hasta = date(anio, 12, 31)
        stmt = stmt.where(Asistencia.fecha >= desde, Asistencia.fecha <= hasta)

    stmt = (
        stmt.order_by(desc(Asistencia.fecha))
        .offset(offset)
        .limit(limit)
    )
    return db.exec(stmt).all()
