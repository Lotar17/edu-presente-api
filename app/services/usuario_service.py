from operator import and_
from app.core.security import get_password_hash
from app.models.usuario import Usuario
from app.models.rol import Rol
from enum import Enum
from typing import Annotated
from sqlmodel import Session, select
from fastapi import Query
from app.dependencies import SessionDep
from app.schemas.rol import RolDescripcion, RolEstado
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.services.escuela_service import get_one_escuela



def get_all_usuarios(db: SessionDep, offset: int, limit: Annotated[int, Query(le=100)]):
    usuarios = db.exec(select(Usuario).offset(offset).limit(limit)).all()
    return usuarios

def get_usuario_by_dni(db: SessionDep, dni: str):
    statement = select(Usuario).where(Usuario.dni == dni)
    usuario_existente = db.exec(statement).first()
    return usuario_existente
    

def add_usuario(usuario: UsuarioCreate, db: SessionDep):
    usuarioValidado = usuario.model_dump(exclude={"escuelasCUE", "rol"})
    db_usuario = Usuario.model_validate(usuarioValidado)
    db_usuario.contrasena = get_password_hash(usuario.contrasena)
    db.add(db_usuario)
    db.flush()
    for escuela in usuario.escuelasCUE:
        nuevoRol = Rol(descripcion=usuario.rol, idUsuario=db_usuario.idUsuario, CUE=escuela)
        db_rol = Rol.model_validate(nuevoRol)
        db.add(db_rol)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario
    
def get_one_usuario(idUsuario: int, db: SessionDep):
    usuario = db.get(Usuario, idUsuario)
    return usuario

def change_usuario(usuario_nuevo: UsuarioUpdate, usuario_existente: Usuario, db: SessionDep):
    usuario_data = usuario_nuevo.model_dump(exclude_unset=True)
    if usuario_nuevo.contrasena:
        usuario_data["contrasena"] = get_password_hash(usuario_nuevo.contrasena)
    usuario_existente.sqlmodel_update(usuario_data)
    db.add(usuario_existente)
    db.commit()
    db.refresh(usuario_existente)
    return usuario_existente

def delete_one_usuario(usuario: Usuario, db: SessionDep):
    db.delete(usuario)
    db.commit()

def get_usuarios_by_escuela(tipo: RolDescripcion, CUE: str, db: SessionDep):
    statement = select(Usuario).select_from(Usuario).join(Rol, (Rol.idUsuario == Usuario.idUsuario)).where(Rol.estado == RolEstado.Activo, Rol.descripcion == tipo, Rol.CUE == CUE)
    resultados = db.exec(statement).all()
    return resultados




