from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from app.dependencies import SessionDep
from app.schemas.alumno import AlumnoPublic, AlumnoCreate
from app.services.alumno_service import get_all_alumnos, get_alumnos_by_curso, add_alumno
from app.services.alumno_service import get_one_alumno
from app.schemas.parentesco import ResponsableConParentescoPublic
from app.services.parentesco_service import get_responsables_by_alumno

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])

@router.get("/", response_model=list[AlumnoPublic])
def getAllAlumnos(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    return get_all_alumnos(db=session, offset=offset, limit=limit)

@router.get("/cursos/{idCurso}", response_model=list[AlumnoPublic])
def getAlumnosByCurso(idCurso: int, session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    try:
        return get_alumnos_by_curso(idCurso=idCurso, db=session)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=AlumnoPublic)
def create_alumno(alumno: AlumnoCreate, session: SessionDep):
    return add_alumno(db=session, alumno_in=alumno)

@router.get("/{idAlumno}", response_model=AlumnoPublic)
def getAlumnoById(idAlumno: int, session: SessionDep):
    alumno = get_one_alumno(idAlumno=idAlumno, db=session)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return alumno

@router.get("/{idAlumno}/responsables", response_model=list[ResponsableConParentescoPublic])
def getResponsablesAlumno(idAlumno: int, session: SessionDep):
    return get_responsables_by_alumno(db=session, idAlumno=idAlumno)