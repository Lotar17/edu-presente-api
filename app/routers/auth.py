from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import List, Optional
from app.db.database import get_session
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.escuela import Escuela  

router = APIRouter()

class LoginRequest(BaseModel):
    dni: str
    password: str

# Estructura para devolver cada opción de rol
class OpcionRol(BaseModel):
    idRol: int
    descripcion: str     # "Docente", "Director"
    idEscuela: int
    nombre_escuela: str  # "Escuela Técnica N°1"

# Estructura de respuesta del login
class LoginResponse(BaseModel):
    mensaje: str
    usuario_id: int
    nombre: str
    apellido: str
    roles_disponibles: List[OpcionRol] 

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, session: Session = Depends(get_session)):
    # 1. Buscar usuario
    user = session.exec(select(Usuario).where(Usuario.dni == data.dni)).first()
    
    if not user or user.contrasena != data.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # 2. Buscar Roles + Nombre de Escuela
    resultados = session.exec(
        select(Rol, Escuela)
        .join(Escuela, Rol.idEscuela == Escuela.idEscuela)
        .where(Rol.idUsuario == user.idUsuario)
    ).all()
    
    # 3. Filtrar solo los Aprobados (o Admin)
    opciones_validas = []
    
    for rol, escuela in resultados:
        if rol.descripcion == "Admin" or rol.estado == "Aprobado":
            opciones_validas.append(OpcionRol(
                idRol=rol.idRol,
                descripcion=rol.descripcion,
                idEscuela=escuela.idEscuela,
                nombre_escuela=escuela.nombre
            ))

    # 4. Validar si quedó alguno
    if not opciones_validas:
        raise HTTPException(status_code=403, detail="Usuario pendiente de aprobación o sin roles.")

    # 5. Devolver TODO al Frontend (para que el usuario elija)
    return LoginResponse(
        mensaje="Login exitoso",
        usuario_id=user.idUsuario,
        nombre=user.nombre,
        apellido=user.apellido,
        roles_disponibles=opciones_validas
    )