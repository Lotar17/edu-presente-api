from typing import Annotated, Sequence
from sqlmodel import select
from fastapi import APIRouter, HTTPException, Query
from app.dependencies import SessionDep

# Importamos los modelos y esquemas
from app.models.escuela import Escuela
from app.schemas.escuela import EscuelaCreate, EscuelaPublic, EscuelaUpdate

router = APIRouter(prefix="/escuelas", tags=["Escuelas"])

@router.get("/escuelas/", response_model=list[EscuelaPublic])
def getAllEscuelas(
    session: SessionDep, 
    offset: int = 0, 
    limit: Annotated[int, Query(le=100)] = 100
):
    """Obtiene la lista de todas las escuelas con paginación."""
    statement = select(Escuela).offset(offset).limit(limit)
    escuelas = session.exec(statement).all()
    return escuelas

@router.post("/escuelas/", response_model=EscuelaPublic)
def create_escuela(escuela: EscuelaCreate, session: SessionDep):
    """Crea una nueva escuela. El CUE debe ser enviado en el cuerpo."""
    # Verificamos si ya existe una escuela con ese CUE para evitar error 500
    escuela_existente = session.get(Escuela, escuela.CUE)
    if escuela_existente:
        raise HTTPException(status_code=400, detail="Ya existe una escuela con este CUE")
    
    db_escuela = Escuela.model_validate(escuela)
    session.add(db_escuela)
    session.commit()
    session.refresh(db_escuela)
    return db_escuela

@router.get("/escuelas/{cue}", response_model=EscuelaPublic)
def read_escuela(cue: str, session: SessionDep):
    """Obtiene una escuela específica por su CUE."""
    db_escuela = session.get(Escuela, cue)
    if not db_escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    return db_escuela

@router.patch("/escuelas/{cue}", response_model=EscuelaPublic)
def update_escuela(cue: str, escuela: EscuelaUpdate, session: SessionDep):
    """Actualiza los datos de una escuela de forma parcial (PATCH)."""
    db_escuela = session.get(Escuela, cue)
    if not db_escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    
    escuela_data = escuela.model_dump(exclude_unset=True)
   
    db_escuela.sqlmodel_update(escuela_data)
    
    session.add(db_escuela)
    session.commit()
    session.refresh(db_escuela)
    return db_escuela

@router.delete("/escuelas/{cue}")
def delete_escuela(cue: str, session: SessionDep):
    """Elimina una escuela por su CUE."""
    db_escuela = session.get(Escuela, cue)
    if not db_escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    
    session.delete(db_escuela)
    session.commit()
    return {"ok": True, "message": f"Escuela con CUE {cue} eliminada correctamente"}
