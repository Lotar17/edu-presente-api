from typing import Annotated, Sequence, List
from fastapi import APIRouter, HTTPException, Query
from app.dependencies import SessionDep
from app.models.curso import Curso
from app.schemas.curso import CursoCreate, CursoPublic, CursoUpdate
from app.schemas.escuela import EscuelaConCursos
from app.services.curso_service import change_curso, delete_one_curso, get_all_cursos, get_cursos_by_usuario, get_one_curso, add_curso
from app.services.rol_service import get_one_rol
from app.services.usuario_service import change_usuario

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
    db_curso = change_curso(curso_nuevo=curso, curso_existente=db_curso, db=session)
    return db_curso

@router.delete("/{idCurso}")
def delete_curso(idCurso: int, session: SessionDep):
    """Elimina un curso por su ID."""
    try:
        delete_one_curso(idCurso, session)
    except Exception:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return {"ok": True, "message": f"Curso {idCurso} eliminado correctamente"}

@router.get("/escuelas/{idUsuario}", response_model=List[EscuelaConCursos])
def get_cursos_and_escuelas_by_usuario(idUsuario: int, session: SessionDep):
    """Devuelve la lista de escuelas asociada a ese usuario y cada escuela cuenta con una lista de cursos en los que el usuario tiene participación"""
    resultados = get_cursos_by_usuario(db=session, idUsuario=idUsuario)
    agrupados: dict[str, EscuelaConCursos] = {}
    for curso, escuela in resultados:
        if escuela.CUE not in agrupados:
            datos_escuela = escuela.model_dump()
            agrupados[escuela.CUE] = EscuelaConCursos(**datos_escuela, cursos=[])
        curso_validado = CursoPublic.model_validate(curso)
        agrupados[escuela.CUE].cursos.append(curso_validado)
    return list(agrupados.values())


