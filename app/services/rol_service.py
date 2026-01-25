from app.models.rol import Rol
from app.dependencies import SessionDep

def get_one_rol(idUsuario: int, CUE: str, db: SessionDep):
    db_rol = db.get(Rol, (idUsuario, CUE))
    return db_rol
