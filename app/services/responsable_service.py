from fastapi import HTTPException
from sqlmodel import select

from app.dependencies import SessionDep
from app.models.responsable import Responsable
from app.schemas.responsable import ResponsableCreate, ResponsableUpdate


def get_one_responsable(idResponsable: int, db: SessionDep):
    return db.get(Responsable, idResponsable)


def get_responsable_by_dni(db: SessionDep, dni: str):
    stmt = select(Responsable).where(Responsable.dni == dni)
    return db.exec(stmt).first()


def add_responsable(db: SessionDep, responsable_in: ResponsableCreate):
    existente = get_responsable_by_dni(db, responsable_in.dni)
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un responsable con ese DNI")

    db_resp = Responsable.model_validate(responsable_in.model_dump())
    db.add(db_resp)
    db.commit()
    db.refresh(db_resp)
    return db_resp


def update_responsable(db: SessionDep, responsable_existente: Responsable, responsable_nuevo: ResponsableUpdate):
    data = responsable_nuevo.model_dump(exclude_unset=True)
    responsable_existente.sqlmodel_update(data)
    db.add(responsable_existente)
    db.commit()
    db.refresh(responsable_existente)
    return responsable_existente


def delete_responsable(db: SessionDep, responsable: Responsable):
    db.delete(responsable)
    db.commit()
