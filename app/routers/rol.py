from fastapi import APIRouter, HTTPException
from app.dependencies import SessionDep
from app.models.rol import Rol
from app.schemas.rol import RolCreate, RolPublic, RolUpdate
from app.services.rol_service import change_rol_status

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/update")
def change_rol_estado(rol: RolUpdate, session: SessionDep):
    """Cambia el rol a 'Activo' si el estado es 'true' y a 'Rechazado' si el estado es 'false'"""
    try:
        db_rol = change_rol_status(rol=rol, db=session)
        return {"ok": True, "message": "Estado del rol modificado correctamente"}
    except Exception:
        raise HTTPException(status_code=404, detail="idUsuario o CUE incorrectos")
