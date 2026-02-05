from __future__ import annotations

from typing import Annotated

from fastapi import HTTPException, Query
from sqlmodel import select

from app.core.security import get_password_hash
from app.dependencies import SessionDep
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.schemas.rol import RolDescripcion, RolEstado
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate


def get_all_usuarios(db: SessionDep, offset: int, limit: Annotated[int, Query(le=100)]):
    usuarios = db.exec(select(Usuario).offset(offset).limit(limit)).all()
    return usuarios


def get_usuario_by_dni(db: SessionDep, dni: str):
    statement = select(Usuario).where(Usuario.dni == dni)
    return db.exec(statement).first()


def get_usuario_by_mail(db: SessionDep, mail: str):
    statement = select(Usuario).where(Usuario.mailABC == mail)
    return db.exec(statement).first()


def get_one_usuario(idUsuario: int, db: SessionDep):
    return db.get(Usuario, idUsuario)


def add_usuario(usuario: UsuarioCreate, db: SessionDep):
    # ✅ Validar DNI único
    if get_usuario_by_dni(db, usuario.dni):
        raise HTTPException(status_code=400, detail="Ya existe un usuario con este DNI")

    # ✅ Validar email único
    if get_usuario_by_mail(db, usuario.mailABC):
        raise HTTPException(status_code=400, detail="Ya existe un usuario con este email")

    # Crear usuario (sin escuelas/rol porque van por tabla Rol)
    usuario_validado = usuario.model_dump(exclude={"escuelasCUE", "rol"})
    db_usuario = Usuario.model_validate(usuario_validado)

    # Guardar contraseña hasheada
    db_usuario.contrasena = get_password_hash(usuario.contrasena)

    db.add(db_usuario)
    db.flush()  # para obtener idUsuario

    # Crear roles por escuela (por defecto RolBase trae estado=Pendiente)
    for cue in usuario.escuelasCUE:
        nuevo_rol = Rol(
            descripcion=usuario.rol,
            idUsuario=db_usuario.idUsuario,
            CUE=cue,
            # estado queda por default en Pendiente (RolBase)
        )
        db.add(Rol.model_validate(nuevo_rol))

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def change_usuario(usuario_nuevo: UsuarioUpdate, usuario_existente: Usuario, db: SessionDep):
    usuario_data = usuario_nuevo.model_dump(exclude_unset=True)

    # Si actualiza contraseña, se hashea
    if usuario_nuevo.contrasena:
        usuario_data["contrasena"] = get_password_hash(usuario_nuevo.contrasena)

    # Si actualiza DNI o mail, validar duplicados (sin contar al mismo usuario)
    if "dni" in usuario_data and usuario_data["dni"]:
        otro = get_usuario_by_dni(db, usuario_data["dni"])
        if otro and otro.idUsuario != usuario_existente.idUsuario:
            raise HTTPException(status_code=400, detail="Ya existe un usuario con este DNI")

    if "mailABC" in usuario_data and usuario_data["mailABC"]:
        otro = get_usuario_by_mail(db, usuario_data["mailABC"])
        if otro and otro.idUsuario != usuario_existente.idUsuario:
            raise HTTPException(status_code=400, detail="Ya existe un usuario con este email")

    usuario_existente.sqlmodel_update(usuario_data)
    db.add(usuario_existente)
    db.commit()
    db.refresh(usuario_existente)
    return usuario_existente



def delete_one_usuario(usuario: Usuario, db: SessionDep):
    db.delete(usuario)
    db.commit()


def get_usuarios_by_escuela(tipo: RolDescripcion, CUE: str, db: SessionDep):
    statement = (
        select(Usuario)
        .select_from(Usuario)
        .join(Rol, Rol.idUsuario == Usuario.idUsuario)
        .where(
            Rol.estado == RolEstado.Activo,
            Rol.descripcion == tipo,
            Rol.CUE == CUE,
        )
    )
    return db.exec(statement).all()
