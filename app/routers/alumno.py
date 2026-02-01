from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from app.dependencies import SessionDep
from app.schemas.alumno import AlumnoPublic
from app.services.alumno_service import get_all_alumnos, get_alumnos_by_curso


router = APIRouter(prefix="/alumnos", tags=["Alumnos"])


@router.get("/", response_model=list[AlumnoPublic])
def getAllAlumnos(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)]=100):
    alumnos = get_all_alumnos(db=session, offset=offset, limit=limit)
    return alumnos

@router.get("/cursos/{idCurso}", response_model=list[AlumnoPublic])
def getAlumnosByCurso(idCurso: int, session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)]=100):
    try:
        alumnos = get_alumnos_by_curso(idCurso=idCurso, db=session)
        alumnos_validado = AlumnoPublic.model_validate(alumnos)
        return alumnos_validado
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
