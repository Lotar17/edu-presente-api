from typing import List
from fastapi import APIRouter, HTTPException
from app.dependencies import SessionDep
from app.models.rol import Rol
from app.schemas.rol import RolCreate, RolPublic, RolUpdate
from app.schemas.usuario import Usuario_Roles
from app.services.rol_service import change_rol_status, get_docentes_pendientes

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/update")
def change_rol_estado(rol: RolUpdate, session: SessionDep):
    """Cambia el rol a 'Activo' si el estado es 'true' y a 'Rechazado' si el estado es 'false'"""
    try:
        db_rol = change_rol_status(rol=rol, db=session)
        return {"ok": True, "message": "Estado del rol modificado correctamente"}
    except Exception:
        raise HTTPException(status_code=404, detail="idUsuario o CUE incorrectos")


@router.get("/docentes/pendientes", response_model=List[Usuario_Roles])
def get_docentes_estado_pendiente(session: SessionDep):
    """Obtener todos los roles con descripcion 'Docente' cuyo estado sea 'Pendiente'. Devuelve una lista que contiene docentes. Cada docente contiene su rol"""
    resultados = get_docentes_pendientes(db=session)
    docentes_roles = []
    for rol, docente in resultados:
        docente_db = docente.model_dump()
        rol_db = RolPublic.model_validate(rol)
        docente_rol = Usuario_Roles(**docente_db, rol=rol_db)
        docentes_roles.append(docente_rol)
    return docentes_roles



