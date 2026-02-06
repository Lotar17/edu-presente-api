from fastapi import APIRouter, HTTPException

from app.dependencies import SessionDep
from app.schemas.parentesco import ParentescoPublic, ParentescoCreate
from app.services.parentesco_service import add_parentesco

from app.models.parentesco import Parentesco


router = APIRouter(prefix="/parentescos", tags=["Parentescos"])


# CREATE

@router.post("/", response_model=ParentescoPublic)
def create_parentesco(payload: ParentescoCreate, session: SessionDep):
    return add_parentesco(db=session, rel_in=payload)


# UPDATE (solo parentesco)

@router.put("/", response_model=ParentescoPublic)
def update_parentesco(payload: ParentescoCreate, session: SessionDep):
    """
    Usa ParentescoCreate porque ya trae:
    - idAlumno
    - idResponsable
    - parentesco
    """
    rel = session.get(Parentesco, (payload.idAlumno, payload.idResponsable))
    if not rel:
        raise HTTPException(status_code=404, detail="Vínculo alumno-responsable no encontrado")

    rel.parentesco = payload.parentesco
    session.add(rel)
    session.commit()
    session.refresh(rel)
    return rel
