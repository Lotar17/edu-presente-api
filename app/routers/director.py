from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.database import get_session 
from app.models.usuario import Usuario

# 👇 ESTA ES LA LÍNEA QUE TE FALTA O QUE PYTHON NO ENCUENTRA
router = APIRouter(
    prefix="",
    tags=["Director"]
)

# 1. Obtener Docentes de una Escuela
@router.get("/escuelas/{escuela_id}/docentes")
def get_docentes_por_escuela(escuela_id: int, session: Session = Depends(get_session)):
    statement = select(Usuario).where(Usuario.escuela_id == escuela_id).where(Usuario.rol == "Docente")
    results = session.exec(statement).all()
    return results

# 2. Obtener Solicitudes Pendientes
@router.get("/escuelas/{escuela_id}/solicitudes")
def get_solicitudes_pendientes(escuela_id: int, session: Session = Depends(get_session)):
    statement = select(Usuario).where(Usuario.escuela_id == escuela_id).where(Usuario.rol == "Pendiente")
    results = session.exec(statement).all()
    return results

# 3. Aprobar Docente
@router.post("/usuarios/{usuario_id}/aprobar-docente")
def aprobar_docente(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario.rol = "Docente"
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return {"message": "Docente aprobado exitosamente"}

# 4. Rechazar Solicitud
@router.delete("/usuarios/{usuario_id}/rechazar-solicitud")
def rechazar_solicitud(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    session.delete(usuario)
    session.commit()
    return {"message": "Solicitud rechazada y usuario eliminado"}

# 5. Generar Código
@router.post("/escuelas/{escuela_id}/generar-codigo")
def generar_codigo(escuela_id: int):
    import random
    codigo = f"DOC-{random.randint(1000, 9999)}"
    return {"codigo": codigo}