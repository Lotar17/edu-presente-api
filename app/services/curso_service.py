from typing import Annotated
from sqlmodel import Session, and_, select
import logging
from fastapi import Query
from app.core.security import get_password_hash
from app.models.curso import Curso
from app.dependencies import SessionDep
from app.models.rol import Rol

from app.models.escuela import Escuela
from app.schemas.curso import CursoCreate, CursoUpdate
from app.schemas.rol import RolEstado
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

def change_curso(curso_nuevo: CursoUpdate, curso_existente: Curso, db: SessionDep):
    # Extraemos solo los campos presentes en la solicitud JSON
    curso_data = curso_nuevo.model_dump(exclude_unset=True)
    if curso_nuevo.password:
        curso_data["password"] = get_password_hash(curso_nuevo.password)
    # Actualización atómica de SQLModel
    curso_existente.sqlmodel_update(curso_data)
    db.add(curso_existente)
    db.commit()
    db.refresh(curso_existente)
    return curso_existente

def get_cursos_by_usuario(db: SessionDep, idUsuario: int):
    statement = (
        select(Curso, Escuela)
        .select_from(Curso)
        .join(Rol, and_(Curso.idUsuario == Rol.idUsuario, Curso.CUE == Rol.CUE))  
        .join(Escuela, Escuela.CUE == Curso.CUE)
        .where(
            and_(
                Rol.idUsuario == idUsuario,           
                Rol.estado == RolEstado.Activo       
            )
        )
    )
    return db.exec(statement).all()


def get_cursos_by_cue(db, cue: str):
    statement = (select(Curso).where(Curso.CUE == cue))
    return db.exec(statement).all()



