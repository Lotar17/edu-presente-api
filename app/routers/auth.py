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
    user = get_usuario_by_dni(db=session, dni=data.dni)
    
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    logger.info(f"Intento login: {user.dni} - Pass DB: {user.contrasena}")
    password_valida = False

    if user.contrasena == data.password:
        password_valida = True
    else:
        try:
            if verify_password(plain_password=data.password, hashed_password=user.contrasena):
                password_valida = True
        except Exception as e:
            logger.warning(f"La contraseña en DB no es un hash válido: {e}")
            pass

    if not password_valida:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    try:
        statement = (
            select(Rol, Escuela)
            .join(Escuela, Rol.CUE == Escuela.CUE) 
            .where(Rol.idUsuario == user.idUsuario)
            .where(
                or_(
                    Rol.estado == "Activo",   
                )
            )
        )
        resultados = session.exec(statement).all()
        
    except Exception as e:
        logger.error(f"Error buscando roles: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno al buscar roles: {str(e)}")

    opciones_validas: list[OpcionRol] = []
    
    for rol, escuela in resultados:
        opciones_validas.append(
            OpcionRol(
                idUsuario=rol.idUsuario,  
                descripcion=rol.descripcion, 
                CUE=escuela.CUE,             
                nombre_escuela=escuela.nombre,
            )
        )

    if not opciones_validas:
        logger.warning(f"Usuario {user.idUsuario} sin roles activos válidos.")
        raise HTTPException(status_code=403, detail="Usuario pendiente de aprobación o sin roles asignados.")

    return LoginResponse(
        mensaje="Login exitoso",
        usuario_id=user.idUsuario,
        nombre=user.nombre or "",
        apellido=user.apellido or "",
        roles_disponibles=opciones_validas,
    )