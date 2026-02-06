# app/routers/asistencia.py
from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, HTTPException, Query
from app.dependencies import SessionDep

from app.schemas.asistencia import AsistenciaCreate
from app.services.asistencia_service import (
    upsert_asistencia,
    upsert_asistencias_bulk,
    get_one_asistencia,
    get_asistencias_by_curso_fecha,
    get_asistencias_by_curso,
    get_asistencias_by_alumno,
    get_asistencias_by_curso_alumno,
)

router = APIRouter(prefix="/asistencias", tags=["Asistencias"])


@router.post("/", response_model=AsistenciaCreate)
def create_or_update_asistencia(payload: AsistenciaCreate, session: SessionDep):
    row = upsert_asistencia(db=session, payload=payload)
    return AsistenciaCreate(
        idCurso=row.idCurso,
        idAlumno=row.idAlumno,
        fecha=row.fecha,
        estado=row.estado,
        lluvia=row.lluvia,
    )


@router.post("/bulk", response_model=list[AsistenciaCreate])
def create_or_update_asistencias_bulk(payloads: list[AsistenciaCreate], session: SessionDep):
    rows = upsert_asistencias_bulk(db=session, payloads=payloads)
    return [
        AsistenciaCreate(
            idCurso=r.idCurso,
            idAlumno=r.idAlumno,
            fecha=r.fecha,
            estado=r.estado,
            lluvia=r.lluvia,
        )
        for r in rows
    ]


# 🔴 MÁS ESPECÍFICA
@router.get("/one/{idCurso}/{idAlumno}/{fecha}", response_model=AsistenciaCreate)
def read_one_asistencia(
    idCurso: int,
    idAlumno: int,
    fecha: date,
    session: SessionDep
):
    row = get_one_asistencia(db=session, idCurso=idCurso, idAlumno=idAlumno, fecha=fecha)
    if not row:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")

    return AsistenciaCreate(
        idCurso=row.idCurso,
        idAlumno=row.idAlumno,
        fecha=row.fecha,
        estado=row.estado,
        lluvia=row.lluvia,
    )


# ✅ HISTORIAL POR CURSO + ALUMNO (opcional por año) — para "curso actual" del alumno
@router.get("/curso/{idCurso}/alumno/{idAlumno}", response_model=list[AsistenciaCreate])
def read_asistencias_by_curso_alumno(
    idCurso: int,
    idAlumno: int,
    session: SessionDep,
    anio: Optional[int] = None,
    offset: int = 0,
    limit: Annotated[int, Query(le=500)] = 200,
):
    rows = get_asistencias_by_curso_alumno(
        db=session,
        idCurso=idCurso,
        idAlumno=idAlumno,
        anio=anio,
        offset=offset,
        limit=limit,
    )
    return [
        AsistenciaCreate(
            idCurso=r.idCurso,
            idAlumno=r.idAlumno,
            fecha=r.fecha,
            estado=r.estado,
            lluvia=r.lluvia,
        )
        for r in rows
    ]


# ✅ HISTORIAL POR ALUMNO (todos los cursos)
@router.get("/alumno/{idAlumno}", response_model=list[AsistenciaCreate])
def read_asistencias_by_alumno(
    idAlumno: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=500)] = 200
):
    rows = get_asistencias_by_alumno(db=session, idAlumno=idAlumno, offset=offset, limit=limit)
    return [
        AsistenciaCreate(
            idCurso=r.idCurso,
            idAlumno=r.idAlumno,
            fecha=r.fecha,
            estado=r.estado,
            lluvia=r.lluvia,
        )
        for r in rows
    ]


# 🟡 HISTORIAL POR CURSO (todas las fechas)
@router.get("/curso/{idCurso}", response_model=list[AsistenciaCreate])
def read_asistencias_by_curso(
    idCurso: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=200)] = 100
):
    rows = get_asistencias_by_curso(db=session, idCurso=idCurso, offset=offset, limit=limit)
    return [
        AsistenciaCreate(
            idCurso=r.idCurso,
            idAlumno=r.idAlumno,
            fecha=r.fecha,
            estado=r.estado,
            lluvia=r.lluvia,
        )
        for r in rows
    ]


# 🔵 LA MÁS GENÉRICA SIEMPRE AL FINAL
@router.get("/{idCurso}/{fecha}", response_model=list[AsistenciaCreate])
def read_asistencias_by_curso_fecha(
    idCurso: int,
    fecha: date,
    session: SessionDep
):
    rows = get_asistencias_by_curso_fecha(db=session, idCurso=idCurso, fecha=fecha)
    return [
        AsistenciaCreate(
            idCurso=r.idCurso,
            idAlumno=r.idAlumno,
            fecha=r.fecha,
            estado=r.estado,
            lluvia=r.lluvia,
        )
        for r in rows
    ]
