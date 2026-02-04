from typing import Annotated
from datetime import date

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.dependencies import SessionDep
from app.schemas.usuario import UsuarioCreate, UsuarioPublic, UsuarioUpdate
from app.schemas.rol import RolDescripcion
from app.core.security import verify_password, get_password_hash

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


# LISTAR USUARIOS

@router.get("/", response_model=list[UsuarioPublic])
def get_all(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
):
    return get_all_usuarios(session, offset, limit)



# CREAR USUARIO

@router.post("/", response_model=UsuarioPublic, status_code=201)
def create(usuario: UsuarioCreate, session: SessionDep):
    usuario_existente = get_usuario_by_dni(session, usuario.dni)
    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un usuario con este DNI"
        )
    return add_usuario(usuario, session)



# OBTENER USUARIO POR ID

@router.get("/{usuario_id}", response_model=UsuarioPublic)
def read(usuario_id: int, session: SessionDep):
    usuario = get_one_usuario(usuario_id, session)
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    return usuario



# ACTUALIZAR USUARIO (EDITAR PERFIL)

@router.patch("/{usuario_id}", response_model=UsuarioPublic)
def update(usuario_id: int, usuario: UsuarioUpdate, session: SessionDep):
    usuario_db = get_one_usuario(usuario_id, session)
    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return change_usuario(usuario, usuario_db, session)



# CAMBIAR CONTRASEÑA (SEGURO)

class CambiarContrasenaIn(BaseModel):
    currentPassword: str
    newPassword: str


@router.post("/{usuario_id}/cambiar-contrasena")
def cambiar_contrasena(
    usuario_id: int,
    payload: CambiarContrasenaIn,
    session: SessionDep
):
    usuario_db = get_one_usuario(usuario_id, session)
    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    # Validar contraseña actual
    if not verify_password(payload.currentPassword, usuario_db.contrasena):
        raise HTTPException(
            status_code=400,
            detail="Contraseña actual incorrecta"
        )

    # Guardar nueva contraseña (hasheada)
    usuario_db.contrasena = get_password_hash(payload.newPassword)

    session.add(usuario_db)
    session.commit()
    session.refresh(usuario_db)

    return {"ok": True}



# ELIMINAR USUARIO

@router.delete("/{usuario_id}", status_code=204)
def delete(usuario_id: int, session: SessionDep):
    usuario_db = get_one_usuario(usuario_id, session)
    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    delete_one_usuario(usuario_db, session)
    return None



#  USUARIOS POR ESCUELA

@router.get("/escuelas/{CUE}/docentes/", response_model=list[UsuarioPublic])
def get_docentes_por_escuela(CUE: str, session: SessionDep):
    rol = RolDescripcion.Docente
    return get_usuarios_by_escuela(
        tipo=rol,
        CUE=CUE,
        db=session
    )


@router.get("/escuelas/{CUE}/asistentes/", response_model=list[UsuarioPublic])
def get_asistentes_por_escuela(CUE: str, session: SessionDep):
    rol = RolDescripcion.Asistente
    return get_usuarios_by_escuela(
        tipo=rol,
        CUE=CUE,
        db=session
    )
