from datetime import date
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from app.dependencies import SessionDep

from app.schemas.asistencia import AsistenciaCreate

from app.services.asistencia_service import (
    upsert_asistencia,
    upsert_asistencias_bulk,   # ✅ NUEVO
    get_one_asistencia,
    get_asistencias_by_curso_fecha,
    get_asistencias_by_curso,
)

router = APIRouter(prefix="/asistencias", tags=["Asistencias"])


@router.post("/", response_model=AsistenciaCreate)
def create_or_update_asistencia(payload: AsistenciaCreate, session: SessionDep):
    """
    Crea o actualiza una asistencia (UPsert) por PK: (idCurso, idAlumno, fecha).
    Devuelve el mismo shape que AsistenciaCreate para no tocar schemas.
    """
    try:
        row = upsert_asistencia(db=session, payload=payload)
        return AsistenciaCreate(
            idCurso=row.idCurso,
            idAlumno=row.idAlumno,
            fecha=row.fecha,
            estado=row.estado,
            lluvia=row.lluvia,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ NUEVO: Bulk upsert (recomendado para Tomar Asistencia)
@router.post("/bulk", response_model=list[AsistenciaCreate])
def create_or_update_asistencias_bulk(payloads: list[AsistenciaCreate], session: SessionDep):
    """
    Upsert masivo de asistencias.
    Ideal para guardar toda la lista del curso en 1 request.
    """
    try:
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
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{idCurso}/{fecha}", response_model=list[AsistenciaCreate])
def read_asistencias_by_curso_fecha(
    idCurso: int,
    fecha: date,
    session: SessionDep
):
    """
    Devuelve asistencias de un curso en una fecha.
    Ideal para la pantalla Tomar Asistencia.
    """
    try:
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
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/curso/{idCurso}", response_model=list[AsistenciaCreate])
def read_asistencias_by_curso(
    idCurso: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=200)] = 100
):
    """
    Historial de asistencias de un curso (todas las fechas), paginado.
    """
    try:
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
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/one/{idCurso}/{idAlumno}/{fecha}", response_model=AsistenciaCreate)
def read_one_asistencia(
    idCurso: int,
    idAlumno: int,
    fecha: date,
    session: SessionDep
):
    """
    Trae una asistencia puntual por PK compuesta.
    """
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
