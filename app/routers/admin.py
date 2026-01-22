from fastapi import APIRouter, HTTPException
from sqlmodel import select
from typing import List
from pydantic import BaseModel

from app.dependencies import SessionDep
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.escuela import Escuela

router = APIRouter(
    prefix="/admin",
    tags=["Administracion"]
)

# Esquema para respuesta combinada
class DirectorPendienteResponse(BaseModel):
    usuario: Usuario
    escuela: Escuela
    id_rol: int

@router.get("/pendientes", response_model=List[DirectorPendienteResponse])
def get_directores_pendientes(session: SessionDep):
    # Join: Usuario -> Rol -> Escuela (Solo "Director" y "Pendiente")
    resultados = session.exec(
        select(Usuario, Escuela, Rol)
        .join(Rol, Rol.idUsuario == Usuario.idUsuario)
        .join(Escuela, Rol.idEscuela == Escuela.idEscuela)
        .where(Rol.descripcion == "Director")
        .where(Rol.estado == "Pendiente")
    ).all()

    response = []
    for user, escuela, rol in resultados:
        response.append(DirectorPendienteResponse(
            usuario=user,
            escuela=escuela,
            id_rol=rol.idRol
        ))
    
    return response

@router.post("/aprobar")
def aprobar_director(session: SessionDep, id_usuario: int, id_escuela: int):
    rol = session.exec(
        select(Rol).where(
            Rol.idUsuario == id_usuario, 
            Rol.idEscuela == id_escuela,
            Rol.descripcion == "Director"
        )
    ).first()

    if not rol:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    rol.estado = "Aprobado"
    session.add(rol)
    session.commit()
    return {"message": "Aprobado"}

@router.post("/rechazar")
def rechazar_director(session: SessionDep, id_usuario: int, id_escuela: int):
    rol = session.exec(
        select(Rol).where(
            Rol.idUsuario == id_usuario, 
            Rol.idEscuela == id_escuela,
            Rol.descripcion == "Director"
        )
    ).first()

    if not rol:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    # Opción A: Borrar el rol (como si nunca solicitó)
    session.delete(rol)
    session.commit()
    return {"message": "Rechazado y eliminado"}