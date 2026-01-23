from typing import Annotated

<<<<<<< HEAD
=======
from sqlmodel import select
from app.dependencies import SessionDep
from app.models.escuela import Escuela
from app.models.rol import Rol
from app.models.usuario import Usuario 
>>>>>>> dev
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from app.dependencies import SessionDep
from app.models.usuario import Usuario
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioPublic,
    UsuarioUpdate
)

<<<<<<< HEAD
router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)
=======
router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
>>>>>>> dev

# =====================================================
# GET /usuarios → Listar usuarios (para Admin)
# =====================================================
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


<<<<<<< HEAD
# =====================================================
# POST /usuarios → Crear usuario (registro / admin)
# =====================================================
@router.post("/", response_model=UsuarioPublic, status_code=201)
def create_usuario(
    usuario: UsuarioCreate,
    session: SessionDep
):
    # Crear instancia del modelo
    db_usuario = Usuario.model_validate(usuario)

=======
@router.post("/usuarios/", response_model=UsuarioPublic)
def create_usuario(usuario: UsuarioCreate, session: SessionDep) :
    usuario_existente = session.get(Usuario, usuario.dni)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con este DNI")
    usuarioValidado = usuario.model_dump(exclude={"escuelasCUE", "rol"})
    db_usuario = Usuario.model_validate(usuarioValidado)
>>>>>>> dev
    session.add(db_usuario)
    session.flush()
    for escuela in usuario.escuelasCUE:
        nuevoRol = Rol(descripcion=usuario.rol, idUsuario=db_usuario.idUsuario, CUE=escuela)
        db_rol = Rol.model_validate(nuevoRol)
        session.add(db_rol)
    session.commit()
    session.refresh(db_usuario)

    return db_usuario


# =====================================================
# GET /usuarios/{id} → Obtener usuario por ID
# =====================================================
@router.get("/{usuario_id}", response_model=UsuarioPublic)
def read_usuario(
    usuario_id: int,
    session: SessionDep
):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
<<<<<<< HEAD
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
=======
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
>>>>>>> dev
    return usuario


# =====================================================
# PATCH /usuarios/{id} → Actualizar usuario
# =====================================================
@router.patch("/{usuario_id}", response_model=UsuarioPublic)
def update_usuario(
    usuario_id: int,
    usuario: UsuarioUpdate,
    session: SessionDep
):
    usuario_db = session.get(Usuario, usuario_id)
    if not usuario_db:
<<<<<<< HEAD
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

=======
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
>>>>>>> dev
    usuario_data = usuario.model_dump(exclude_unset=True)
    usuario_db.sqlmodel_update(usuario_data)

    session.add(usuario_db)
    session.commit()
    session.refresh(usuario_db)

    return usuario_db


# =====================================================
# DELETE /usuarios/{id} → Eliminar usuario
# =====================================================
@router.delete("/{usuario_id}", status_code=204)
def delete_usuario(
    usuario_id: int,
    session: SessionDep
):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    session.delete(usuario)
    session.commit()
    return None
