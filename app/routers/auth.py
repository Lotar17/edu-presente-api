from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import List

from app.db.database import get_session
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.escuela import Escuela

router = APIRouter()


class LoginRequest(BaseModel):
    dni: str
    password: str


class OpcionRol(BaseModel):
    # ⚠️ En el merge, Rol NO tiene idRol. Usamos idEscuela como identificador estable
    idRol: int
    descripcion: str
    idEscuela: int
    nombre_escuela: str


class LoginResponse(BaseModel):
    mensaje: str
    usuario_id: int
    nombre: str
    apellido: str
    roles_disponibles: List[OpcionRol]


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, session: Session = Depends(get_session)):
    # 1) Buscar usuario
    user = session.exec(select(Usuario).where(Usuario.dni == data.dni)).first()

    if not user or user.contrasena != data.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # 2) Traer roles + escuela
    resultados = session.exec(
        select(Rol, Escuela)
        .join(Escuela, Rol.idEscuela == Escuela.idEscuela)
        .where(Rol.idUsuario == user.idUsuario)
    ).all()

    # 3) Filtrar aprobados
    # Tu sistema usa "Activo/Pendiente/Rechazado".
    # Acepto "Aprobado" por compatibilidad con datos viejos.
    estados_ok = {"Activo", "Aprobado"}

    opciones_validas: list[OpcionRol] = []
    for rol, escuela in resultados:
        if rol.descripcion == "Admin" or (rol.estado in estados_ok):
            opciones_validas.append(
                OpcionRol(
                    idRol=rol.idEscuela,  # <-- reemplazo del viejo idRol
                    descripcion=rol.descripcion,
                    idEscuela=escuela.idEscuela,
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
