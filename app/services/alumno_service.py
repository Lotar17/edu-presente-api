
from typing import Annotated
from app.models.alumno import Alumno
from app.models.asistencia import Asistencia
from fastapi import Query
from sqlmodel import select
from app.dependencies import SessionDep
from app.models.curso import Curso
from app.services.curso_service import get_one_curso


def get_all_alumnos(db: SessionDep, offset: int, limit: Annotated[int, Query(le=100)]):
    alumnos = db.exec(select(Alumno).offset(offset).limit(limit)).all()
    return alumnos


def get_alumnos_by_curso(idCurso: int, db: SessionDep):
    db_curso = get_one_curso(idCurso=idCurso, db=db)
    if db_curso is None:
        raise Exception("El curso ingresado no existe")
    return db_curso.alumnos

