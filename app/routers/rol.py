from fastapi import APIRouter, HTTPException
from app.dependencies import SessionDep
from app.models.rol import Rol
from app.schemas.rol import RolCreate, RolPublic

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=RolPublic, status_code=201)
def create_rol(session: SessionDep, data: RolCreate):
    rol = Rol(**data.model_dump())
    session.add(rol)
    session.commit()
    session.refresh(rol)
    return rol
