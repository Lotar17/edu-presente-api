from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from app.dependencies import SessionDep
from app.schemas.usuario import UsuarioCreate, UsuarioPublic, UsuarioUpdate
from app.schemas.rol import RolDescripcion

from app.services.usuario_service import (
    add_usuario,
    change_usuario,
    delete_one_usuario,
    get_all_usuarios,
    get_one_usuario,
    get_usuario_by_dni,
    get_usuarios_by_escuela,
)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=list[UsuarioPublic])
def get_all(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    return get_all_usuarios(session, offset, limit)


@router.post("/", response_model=UsuarioPublic, status_code=201)
def create(usuario: UsuarioCreate, session: SessionDep):
    usuario_existente = get_usuario_by_dni(session, usuario.dni)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con este DNI")
    return add_usuario(usuario, session)


@router.get("/{usuario_id}", response_model=UsuarioPublic)
def read(usuario_id: int, session: SessionDep):
    usuario = get_one_usuario(usuario_id, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.patch("/{usuario_id}", response_model=UsuarioPublic)
def update(usuario_id: int, usuario: UsuarioUpdate, session: SessionDep):
    usuario_db = get_one_usuario(usuario_id, session)
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return change_usuario(usuario, usuario_db, session)


@router.delete("/{usuario_id}", status_code=204)
def delete(usuario_id: int, session: SessionDep):
    usuario_db = get_one_usuario(usuario_id, session)
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    delete_one_usuario(usuario_db, session)
    return None


@router.get("/escuelas/{CUE}/docentes/", response_model=list[UsuarioPublic])
def get_docentes_por_escuela(CUE: str, session: SessionDep):
    rol = RolDescripcion.Docente
    return get_usuarios_by_escuela(tipo=rol, CUE=CUE, db=session)


@router.get("/escuelas/{CUE}/asistentes/", response_model=list[UsuarioPublic])
def get_asistentes_por_escuela(CUE: str, session: SessionDep):
    rol = RolDescripcion.Asistente
    return get_usuarios_by_escuela(tipo=rol, CUE=CUE, db=session)

