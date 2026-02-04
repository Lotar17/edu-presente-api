from fastapi import APIRouter
from app.dependencies import SessionDep
from app.schemas.parentesco import ParentescoPublic, ParentescoCreate
from app.services.parentesco_service import add_parentesco

router = APIRouter(prefix="/parentescos", tags=["Parentescos"])

@router.post("/", response_model=ParentescoPublic)
def create_parentesco(payload: ParentescoCreate, session: SessionDep):
    return add_parentesco(db=session, rel_in=payload)
