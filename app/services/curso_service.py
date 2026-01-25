from typing import Annotated
from sqlmodel import Session, select
import logging
from fastapi import Query
from app.core.security import get_password_hash
from app.models.curso import Curso
from app.dependencies import SessionDep

from app.schemas.curso import CursoCreate
from app.services.rol_service import get_one_rol

logger = logging.getLogger()

def get_all_cursos(db: SessionDep, offset: int, limit: Annotated[int, Query(le=100)]):
    statement = select(Curso).offset(offset).limit(limit)
    cursos = db.exec(statement).all()
    return cursos
    

def add_curso(db: SessionDep, curso: CursoCreate):
    rol = get_one_rol(curso.idUsuario, curso.CUE, db)
    logger.info(rol)
    if not rol or rol.estado.value != "Activo":
        return None
    db_curso = Curso.model_validate(curso)
    db_curso.password = get_password_hash(curso.password)
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

def get_one_curso(idCurso: int, db: SessionDep):
    db_curso = db.get(Curso, idCurso)
    return db_curso

def delete_one_curso(idCurso: int, db: SessionDep):
    db_curso = db.get(Curso, idCurso)
    if not db_curso:
        raise Exception("Curso no encontrado")
    db.delete(db_curso)
    db.commit()



