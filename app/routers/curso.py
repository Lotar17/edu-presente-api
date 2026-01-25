from typing import Annotated, Sequence
from sqlmodel import select
from fastapi import APIRouter, HTTPException, Query
from app.dependencies import SessionDep
from app.models.curso import Curso
from app.schemas.curso import CursoCreate, CursoPublic, CursoUpdate

router = APIRouter(prefix="/cursos", tags=["Cursos"])

@router.get("/", response_model=list[CursoPublic])
def getAllCursos(
    session: SessionDep, 
    offset: int = 0, 
    limit: Annotated[int, Query(le=100)] = 100
):
    """Obtiene la lista de todos los cursos con paginación."""
    statement = select(Curso).offset(offset).limit(limit)
    cursos = session.exec(statement).all()
    return cursos

@router.post("/", response_model=CursoPublic)
def create_curso(curso: CursoCreate, session: SessionDep):
    """Crea un nuevo curso."""
    db_curso = Curso.model_validate(curso)
    session.add(db_curso)
    session.commit()
    session.refresh(db_curso)
    return db_curso

@router.get("/{idCurso}", response_model=CursoPublic)
def read_curso(idCurso: int, session: SessionDep):
    """Obtiene un curso específico por su ID."""
    db_curso = session.get(Curso, idCurso)
    if not db_curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return db_curso

@router.patch("/{idCurso}", response_model=CursoPublic)
def update_curso(idCurso: int, curso: CursoUpdate, session: SessionDep):
    """Actualiza los datos de un curso de forma parcial (PATCH)."""
    db_curso = session.get(Curso, idCurso)
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
    db_curso = session.get(Curso, idCurso)
    if not db_curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    session.delete(db_curso)
    session.commit()
    return {"ok": True, "message": f"Curso {idCurso} eliminado correctamente"}
