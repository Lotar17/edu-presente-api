from typing import Annotated, Sequence
from fastapi import APIRouter, HTTPException, Query
from app.dependencies import SessionDep
from app.models.curso import Curso
from app.schemas.curso import CursoCreate, CursoPublic, CursoUpdate
from app.services.curso_service import delete_one_curso, get_all_cursos, get_one_curso, add_curso
from app.services.rol_service import get_one_rol

router = APIRouter(prefix="/cursos", tags=["Cursos"])

@router.get("/", response_model=list[CursoPublic])
def getAllCursos(
    session: SessionDep, 
    offset: int = 0, 
    limit: Annotated[int, Query(le=100)] = 100
):
    """Obtiene la lista de todos los cursos con paginación."""
    return get_all_cursos(session, offset, limit)

@router.post("/", response_model=CursoPublic)
def create_curso(curso: CursoCreate, session: SessionDep):
    """Crea un nuevo curso."""
    curso_creado = add_curso(session, curso)
    if not curso_creado:
        raise HTTPException(status_code=404, detail="El rol ingresado no se encuentra habilitado")
    return curso_creado

@router.get("/{idCurso}", response_model=CursoPublic)
def read_curso(idCurso: int, session: SessionDep):
    """Obtiene un curso específico por su ID."""
    db_curso = get_one_curso(idCurso, session)
    if not db_curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return db_curso

@router.patch("/{idCurso}", response_model=CursoPublic)
def update_curso(idCurso: int, curso: CursoUpdate, session: SessionDep):
    """Actualiza los datos de un curso de forma parcial (PATCH)."""
    db_curso = get_one_curso(idCurso, session)
    if not db_curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    # Extraemos solo los campos presentes en la solicitud JSON
    curso_data = curso.model_dump(exclude_unset=True)
    
    # Actualización atómica de SQLModel
    db_curso.sqlmodel_update(curso_data)
    
    session.add(db_curso)
    session.commit()
    session.refresh(db_curso)
    return db_curso

@router.delete("/{idCurso}")
def delete_curso(idCurso: int, session: SessionDep):
    """Elimina un curso por su ID."""
    try:
        delete_one_curso(idCurso, session)
    except Exception:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return {"ok": True, "message": f"Curso {idCurso} eliminado correctamente"}
