from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from app.dependencies import SessionDep
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioPublic, UsuarioUpdate

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=list[UsuarioPublic])
def get_all_usuarios(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
):
    usuarios = session.exec(
        select(Usuario).offset(offset).limit(limit)
    ).all()
    return usuarios


@router.post("/", response_model=UsuarioPublic, status_code=201)
def create_usuario(
    usuario: UsuarioCreate,
    session: SessionDep
):
    db_usuario = Usuario.model_validate(usuario)
    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)
    return db_usuario


@router.get("/{usuario_id}", response_model=UsuarioPublic)
def read_usuario(
    usuario_id: int,
    session: SessionDep
):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.patch("/{usuario_id}", response_model=UsuarioPublic)
def update_usuario(
    usuario_id: int,
    usuario: UsuarioUpdate,
    session: SessionDep
):
    usuario_db = session.get(Usuario, usuario_id)
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario_data = usuario.model_dump(exclude_unset=True)
    usuario_db.sqlmodel_update(usuario_data)

    session.add(usuario_db)
    session.commit()
    session.refresh(usuario_db)
    return usuario_db


@router.delete("/{usuario_id}", status_code=204)
def delete_usuario(
    usuario_id: int,
    session: SessionDep
):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    session.delete(usuario)
    session.commit()
    return None
