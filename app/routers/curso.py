# app/routers/curso.py
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from app.dependencies import SessionDep
from app.models.curso import Curso
from app.schemas.curso import CursoCreate, CursoPublic

router = APIRouter()

@router.get("/", response_model=list[CursoPublic])
def list_cursos(
    session: SessionDep,
    escuelaId: int | None = Query(default=None),
    cicloLectivo: int | None = Query(default=None),
):
    stmt = select(Curso)
    if escuelaId is not None:
        stmt = stmt.where(Curso.idEscuela == escuelaId)
    if cicloLectivo is not None:
        stmt = stmt.where(Curso.cicloLectivo == cicloLectivo)

    return session.exec(stmt).all()

@router.get("/{curso_id}", response_model=CursoPublic)
def get_curso(session: SessionDep, curso_id: int):
    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

@router.post("/", response_model=CursoPublic, status_code=201)
def create_curso(session: SessionDep, data: CursoCreate):
    curso = Curso(
        idEscuela=data.escuelaId,
        nombre=data.nombre,
        grado=data.grado,
        division=data.division,
        turno=data.turno,
        cicloLectivo=data.cicloLectivo,
    )
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso
