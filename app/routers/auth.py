from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select, or_
from app.core.security import verify_password
from app.dependencies import SessionDep
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.escuela import Escuela
from app.schemas.rol import RolDescripcion, RolEstado
from app.services.usuario_service import get_usuario_by_dni
from app.schemas.login import LoginRequest, OpcionRol, LoginResponse
import logging

router = APIRouter(prefix="/login", tags=["Login"])

logger = logging.getLogger()

@router.post("/", response_model=LoginResponse)
def login(data: LoginRequest, session: SessionDep):
    # 1) Buscar usuario
    user = get_usuario_by_dni(db=session, dni=data.dni)
    logger.error(user)

    #TODO: Borrar primer condicion despues del OR una vez que hayan implementado el hasheo de la contrasena correctamente
    if not user or not verify_password(plain_password=data.password, hashed_password=user.contrasena):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # 2) Traer roles + escuela
    statement = select(Rol, Escuela).join(Escuela).where(Rol.idUsuario == user.idUsuario).where(or_(Rol.estado == RolEstado.Activo, Rol.descripcion == RolDescripcion.Administrador))
    resultados = session.exec(statement)
    opciones_validas: list[OpcionRol] = []
    for rol, escuela in resultados:
        opciones_validas.append(
            OpcionRol(
                idUsuario=rol.idUsuario,  
                descripcion=rol.descripcion.value,
                CUE=escuela.CUE,
                nombre_escuela=escuela.nombre,
            )
        )
    if not opciones_validas:
        raise HTTPException(status_code=403, detail="Usuario pendiente de aprobación o sin roles.")

    return LoginResponse(
        mensaje="Login exitoso",
        usuario_id=user.idUsuario,
        nombre=user.nombre or "",
        apellido=user.apellido or "",
        roles_disponibles=opciones_validas,
    )
