from typing import Annotated, Sequence

from sqlmodel import select
from app.dependencies import SessionDep
from app.models.escuela import Escuela
from app.models.rol import Rol
from app.models.usuario import Usuario 
from fastapi import APIRouter, HTTPException, Query

from app.schemas.usuario import UsuarioCreate, UsuarioPublic, UsuarioUpdate

router = APIRouter()


@router.get("/usuarios/", response_model=list[UsuarioPublic])
def getAllUsuarios(session: SessionDep, offset: int =0, limit: Annotated[int, Query(le=100)]=100) :
    usuarios = session.exec(select(Usuario).offset(offset).limit(limit)).all()
    return usuarios


@router.post("/usuarios/", response_model=UsuarioPublic)
def create_usuario(usuario: UsuarioCreate, session: SessionDep) :
    usuarioValidado = usuario.model_dump(exclude={"escuelasCUE", "rol"})
    db_usuario = Usuario.model_validate(usuarioValidado)
    session.add(db_usuario)
    session.flush()
    for escuela in usuario.escuelasCUE:
        nuevoRol = Rol(descripcion=usuario.rol, idUsuario=db_usuario.idUsuario, CUE=escuela)
        db_rol = Rol.model_validate(nuevoRol)
        session.add(db_rol)
    session.commit()
    session.refresh(db_usuario)
    return db_usuario

@router.get("/usuarios/{usuario_id}", response_model=UsuarioPublic)
def read_usuario(usuario_id:int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return usuario

@router.patch("/usuarios/{usuario_id}", response_model=UsuarioPublic)
def update_usuario(usuario_id: int, usuario: UsuarioUpdate, session: SessionDep):
    usuario_db = session.get(Usuario, usuario_id)
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    usuario_data = usuario.model_dump(exclude_unset=True)
    usuario_db.sqlmodel_update(usuario_data)
    session.add(usuario_db)
    session.commit()
    session.refresh(usuario_db)
    return usuario_db

@router.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id:int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")
    session.delete(usuario)
    session.commit()
    return {"ok": True}
