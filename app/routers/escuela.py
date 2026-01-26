from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select, or_
from sqlalchemy import func

from app.dependencies import SessionDep
from app.models.escuela import Escuela
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.curso import Curso
from app.models.alumno import Alumno
from app.schemas.escuela import EscuelaCreate, EscuelaPublic, EscuelaUpdate
from app.schemas.usuario import UsuarioPublic

router = APIRouter(prefix="/escuelas", tags=["Escuelas"])

@router.get("/", response_model=list[EscuelaPublic])
def list_escuelas(session: SessionDep, q: str | None = None):
    stmt = select(Escuela)
    if q:
        stmt = stmt.where(or_(Escuela.nombre.contains(q), func.coalesce(Escuela.cue, "").contains(q)))
    return session.exec(stmt).all()

@router.get("/{escuela_id}", response_model=EscuelaPublic)
def get_escuela(session: SessionDep, escuela_id: int):
    escuela = session.get(Escuela, escuela_id)
    if not escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    return escuela

@router.post("/", response_model=EscuelaPublic, status_code=201)
def create_escuela(session: SessionDep, data: EscuelaCreate):
    escuela = Escuela.model_validate(data)
    session.add(escuela)
    session.commit()
    session.refresh(escuela)
    return escuela

@router.patch("/{escuela_id}", response_model=EscuelaPublic)
def update_escuela(session: SessionDep, escuela_id: int, data: EscuelaUpdate):
    escuela = session.get(Escuela, escuela_id)
    if not escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    escuela.sqlmodel_update(data.model_dump(exclude_unset=True))
    session.add(escuela)
    session.commit()
    session.refresh(escuela)
    return escuela

@router.delete("/{escuela_id}", status_code=204)
def delete_escuela(session: SessionDep, escuela_id: int):
    escuela = session.get(Escuela, escuela_id)
    if not escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    session.delete(escuela)
    session.commit()
    return None

@router.get("/{escuela_id}/solicitudes", response_model=list[UsuarioPublic])
def get_solicitudes_pendientes(escuela_id: int, session: SessionDep):
    try:
        statement = (
            select(Usuario)
            .join(Rol, Usuario.idUsuario == Rol.idUsuario)
            .where(Rol.idEscuela == escuela_id)
            .where(Rol.descripcion == "Docente")
            .where(Rol.estado == "Pendiente")
        )
        usuarios = session.exec(statement).all()

        resultados = []
        for u in usuarios:
            print(f"   -> Procesando usuario: {u.nombre} {u.apellido} (ID: {u.idUsuario})")
            
            u_pub = UsuarioPublic(
                idUsuario=u.idUsuario,
                dni=u.dni,
                cuil=u.cuil,
                nombre=u.nombre,
                apellido=u.apellido,
                celular=u.celular or "",
                mailABC=u.mailABC or "",
                fechaNacimiento=u.fechaNacimiento, 
                rol="Docente",
                idEscuela=escuela_id
            )
            resultados.append(u_pub)
            
        return resultados

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{escuela_id}/docentes", response_model=list[UsuarioPublic])
def get_docentes_activos(escuela_id: int, session: SessionDep):
    try:
        statement = (
            select(Usuario)
            .join(Rol, Usuario.idUsuario == Rol.idUsuario)
            .where(Rol.idEscuela == escuela_id)
            .where(Rol.descripcion == "Docente")
            .where(or_(Rol.estado == "Activo", Rol.estado == "Aprobado"))
        )
        usuarios = session.exec(statement).all()
        
        resultados = []
        for u in usuarios:
            u_pub = UsuarioPublic(
                idUsuario=u.idUsuario,
                dni=u.dni,
                cuil=u.cuil,
                nombre=u.nombre,
                apellido=u.apellido,
                celular=u.celular or "",
                mailABC=u.mailABC or "",
                fechaNacimiento=u.fechaNacimiento,
                rol="Docente",
                idEscuela=escuela_id
            )
            resultados.append(u_pub)
        return resultados

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{escuela_id}/cursos")
def get_cursos_por_escuela(escuela_id: int, session: SessionDep):
    try:
        statement = select(Curso).where(Curso.idEscuela == escuela_id)
        cursos = session.exec(statement).all()
        
        resultado = []
        for curso in cursos:
            cantidad = session.exec(
                select(func.count())
                .select_from(Alumno)
                .where(Alumno.idCurso == curso.idCurso)
            ).one()
            
            curso_dict = curso.model_dump()
            curso_dict["cantidadAlumnos"] = cantidad 
            resultado.append(curso_dict)
            
        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{escuela_id}/docentes/{usuario_id}/aprobar")
def aprobar_docente(escuela_id: int, usuario_id: int, session: SessionDep):
    rol = session.exec(select(Rol).where(Rol.idUsuario == usuario_id, Rol.idEscuela == escuela_id)).first()
    if not rol: raise HTTPException(404, detail="Solicitud no encontrada")
    rol.estado = "Activo"
    session.add(rol)
    session.commit()
    return {"message": "Aprobado"}

@router.delete("/{escuela_id}/docentes/{usuario_id}/rechazar")
def rechazar_docente(escuela_id: int, usuario_id: int, session: SessionDep):
    rol = session.exec(select(Rol).where(Rol.idUsuario == usuario_id, Rol.idEscuela == escuela_id)).first()
    if not rol: raise HTTPException(404, detail="Solicitud no encontrada")
    session.delete(rol)
    session.commit()
    return {"message": "Rechazado"}

@router.get("/cursos/{curso_id}/alumnos", response_model=list[Alumno])
def get_alumnos_por_curso(curso_id: int, session: SessionDep):
    try:
        statement = select(Alumno).where(Alumno.idCurso == curso_id)
        alumnos = session.exec(statement).all()
        return alumnos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))