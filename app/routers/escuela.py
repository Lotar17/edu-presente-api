# app/routers/escuela.py
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select, or_
from sqlalchemy import func

from app.dependencies import SessionDep
from app.models.escuela import Escuela
from app.schemas.escuela import EscuelaCreate, EscuelaPublic, EscuelaUpdate

router = APIRouter(prefix="/escuelas", tags=["Escuelas"])


@router.get("/", response_model=list[EscuelaPublic])
def list_escuelas(
    session: SessionDep,
    q: str | None = Query(default=None, description="Búsqueda por nombre/CUE"),
):
    stmt = select(Escuela)

    if q:
        stmt = stmt.where(
            or_(
                Escuela.nombre.contains(q),
                func.coalesce(Escuela.cue, "").contains(q),
            )
        )

    return session.exec(stmt).all()


@router.get("/{escuela_id}", response_model=EscuelaPublic)
def get_escuela(session: SessionDep, escuela_id: int):
    escuela = session.get(Escuela, escuela_id)
    if not escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    return escuela


@router.post("/", response_model=EscuelaPublic, status_code=201)
def create_escuela(session: SessionDep, data: EscuelaCreate):
    escuela = Escuela.model_validate(data)
    session.add(escuela)
    session.commit()
    session.refresh(escuela)
    return escuela


@router.patch("/{escuela_id}", response_model=EscuelaPublic)
def update_escuela(session: SessionDep, escuela_id: int, data: EscuelaUpdate):
    escuela = session.get(Escuela, escuela_id)
    if not escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")

    payload = data.model_dump(exclude_unset=True)
    escuela.sqlmodel_update(payload)

    session.add(escuela)
    session.commit()
    session.refresh(escuela)
    return escuela


@router.delete("/{escuela_id}", status_code=204)
def delete_escuela(session: SessionDep, escuela_id: int):
    escuela = session.get(Escuela, escuela_id)
    if not escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    session.delete(escuela)
    session.commit()
    return None
