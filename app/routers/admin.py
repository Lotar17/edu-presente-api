# app/routers/admin.py
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from typing import List, Optional, Dict
from pydantic import BaseModel

from app.dependencies import SessionDep
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.escuela import Escuela

router = APIRouter(
    prefix="/admin",
    tags=["Administracion"]
)

# =========================================================
# ✅ RESPUESTA: DIRECTORES PENDIENTES
# =========================================================
class DirectorPendienteResponse(BaseModel):
    usuario: Usuario
    escuela: Escuela
    id_rol: int


@router.get("/pendientes", response_model=List[DirectorPendienteResponse])
def get_directores_pendientes(session: SessionDep):
    resultados = session.exec(
        select(Usuario, Escuela, Rol)
        .join(Rol, Rol.idUsuario == Usuario.idUsuario)
        .join(Escuela, Rol.idEscuela == Escuela.idEscuela)
        .where(Rol.descripcion == "Director")
        .where(Rol.estado == "Pendiente")
    ).all()

    response: List[DirectorPendienteResponse] = []
    for user, escuela, rol in resultados:
        response.append(
            DirectorPendienteResponse(
                usuario=user,
                escuela=escuela,
                id_rol=getattr(rol, "idRol", 0)  # por si cambia el modelo
            )
        )
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

    # ✅ Unificamos con el resto del sistema (login filtra por "Activo")
    rol.estado = "Activo"
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

    session.delete(rol)
    session.commit()
    return {"message": "Rechazado y eliminado"}


# =========================================================
# ✅ LISTADO ADMIN DE USUARIOS + ROLES + ESCUELAS (+ DATOS EXTRA)
# =========================================================
class UsuarioAdminRow(BaseModel):
    idUsuario: int
    dni: str
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    mailABC: Optional[str] = None

    # ✅ ESTOS SON LOS CAMPOS QUE TE FALTABAN
    cuil: Optional[str] = None
    celular: Optional[str] = None
    fechaNacimiento: Optional[str] = None  # se devuelve como string (ISO / str(date))

    roles: List[str] = []
    escuelas: List[str] = []
    estados: List[str] = []


@router.get("/usuarios", response_model=List[UsuarioAdminRow])
def admin_list_usuarios(session: SessionDep):
    # LEFT JOIN para incluir usuarios sin rol/escuela
    rows = session.exec(
        select(Usuario, Rol, Escuela)
        .join(Rol, Rol.idUsuario == Usuario.idUsuario, isouter=True)
        .join(Escuela, Rol.idEscuela == Escuela.idEscuela, isouter=True)
    ).all()

    out: Dict[int, UsuarioAdminRow] = {}

    for u, r, e in rows:
        if u.idUsuario not in out:
            # 🔥 Traemos estos campos sin asumir el nombre exacto
            cuil = getattr(u, "cuil", None) or getattr(u, "cuit", None)
            celular = getattr(u, "celular", None) or getattr(u, "telefono", None)

            fn = getattr(u, "fechaNacimiento", None) or getattr(u, "fecha_nacimiento", None)
            fecha_nac_str = str(fn) if fn is not None else None

            out[u.idUsuario] = UsuarioAdminRow(
                idUsuario=u.idUsuario,
                dni=u.dni,
                nombre=u.nombre,
                apellido=u.apellido,
                mailABC=getattr(u, "mailABC", None) or getattr(u, "email", None),

                cuil=cuil,
                celular=celular,
                fechaNacimiento=fecha_nac_str,

                roles=[],
                escuelas=[],
                estados=[],
            )

        # Puede venir None por el LEFT JOIN
        if r:
            if r.descripcion and r.descripcion not in out[u.idUsuario].roles:
                out[u.idUsuario].roles.append(r.descripcion)

            # estado puede ser enum o string, lo normalizamos a string
            estado = getattr(r, "estado", None)
            estado_str = str(estado.value) if hasattr(estado, "value") else (str(estado) if estado is not None else None)
            if estado_str and estado_str not in out[u.idUsuario].estados:
                out[u.idUsuario].estados.append(estado_str)

        if e and getattr(e, "nombre", None):
            if e.nombre not in out[u.idUsuario].escuelas:
                out[u.idUsuario].escuelas.append(e.nombre)

    return list(out.values())
