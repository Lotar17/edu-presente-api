# routers/responsables.py
from fastapi import APIRouter, HTTPException
from app.dependencies import SessionDep
from app.schemas.responsable import ResponsablePublic, ResponsableCreate
from app.services.responsable_service import (
    add_responsable,
    get_one_responsable,
    get_responsable_by_dni,
)

router = APIRouter(prefix="/responsables", tags=["Responsables"])


@router.post("/", response_model=ResponsablePublic)
def create_responsable(payload: ResponsableCreate, session: SessionDep):
    return add_responsable(db=session, responsable_in=payload)


@router.get("/dni/{dni}", response_model=ResponsablePublic)
def get_responsable_by_dni_route(dni: str, session: SessionDep):
    r = get_responsable_by_dni(db=session, dni=dni)
    if not r:
        raise HTTPException(status_code=404, detail="Responsable no encontrado")
    return r


@router.get("/{idResponsable}", response_model=ResponsablePublic)
def get_responsable(idResponsable: int, session: SessionDep):
    r = get_one_responsable(idResponsable=idResponsable, db=session)
    if not r:
        raise HTTPException(status_code=404, detail="Responsable no encontrado")
    return r
