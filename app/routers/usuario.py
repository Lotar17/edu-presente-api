from typing import Annotated, Sequence

from app.dependencies import SessionDep
from app.models.escuela import Escuela
from app.models.rol import Rol
from app.models.usuario import Usuario 
from fastapi import APIRouter, HTTPException, Query

from app.schemas.rol import RolDescripcion
from app.schemas.usuario import UsuarioCreate, UsuarioPublic, UsuarioUpdate
from app.services.usuario_service import add_usuario, change_usuario, delete_one_usuario, get_all_usuarios, get_one_usuario, get_usuario_by_dni, get_usuarios_by_escuela

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/usuarios/", response_model=list[UsuarioPublic])
def getAllUsuarios(session: SessionDep, offset: int =0, limit: Annotated[int, Query(le=100)]=100) :
    usuarios = get_all_usuarios(session, offset, limit)
    return usuarios


@router.post("/usuarios/", response_model=UsuarioPublic)
def create_usuario(usuario: UsuarioCreate, session: SessionDep) :
    usuario_existente = get_usuario_by_dni(session, usuario.dni)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con este DNI")
    db_usuario = add_usuario(usuario, session)
    return db_usuario

@router.get("/usuarios/{usuario_id}", response_model=UsuarioPublic)
def read_usuario(usuario_id:int, session: SessionDep):
    usuario = get_one_usuario(usuario_id, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.patch("/usuarios/{usuario_id}", response_model=UsuarioPublic)
def update_usuario(usuario_id: int, usuario: UsuarioUpdate, session: SessionDep):
    usuario_db = get_one_usuario(usuario_id, session)
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario_db = change_usuario(usuario, usuario_db, session)
    return usuario_db

@router.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id:int, session: SessionDep):
    usuario = get_one_usuario(usuario_id, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")
    delete_one_usuario(usuario, session)
    return {"ok": True}

@router.get("/escuelas/{CUE}/docentes/", response_model=list[UsuarioPublic])
def get_docentes_por_escuela(CUE: str, session: SessionDep):
    rol = RolDescripcion.Docente
    docentes = get_usuarios_by_escuela(tipo=rol, CUE=CUE, db=session)
    return docentes

        



