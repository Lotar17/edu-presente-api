from fastapi import HTTPException
from sqlmodel import select

from app.dependencies import SessionDep
from app.models.parentesco import Parentesco
from app.models.alumno import Alumno
from app.models.responsable import Responsable
from app.schemas.parentesco import ParentescoCreate, ParentescoPublic, ResponsableConParentescoPublic


def add_parentesco(db: SessionDep, rel_in: ParentescoCreate) -> ParentescoPublic:
    alumno = db.get(Alumno, rel_in.idAlumno)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    resp = db.get(Responsable, rel_in.idResponsable)
    if not resp:
        raise HTTPException(status_code=404, detail="Responsable no encontrado")

    ya = db.get(Parentesco, (rel_in.idAlumno, rel_in.idResponsable))
    if ya:
        raise HTTPException(status_code=400, detail="El responsable ya está vinculado a este alumno")

    rel = Parentesco.model_validate(rel_in.model_dump())
    db.add(rel)
    db.commit()
    db.refresh(rel)
    return rel


def get_responsables_by_alumno(db: SessionDep, idAlumno: int) -> list[ResponsableConParentescoPublic]:
    stmt = (
        select(Responsable, Parentesco.parentesco)
        .join(Parentesco, Parentesco.idResponsable == Responsable.idResponsable)
        .where(Parentesco.idAlumno == idAlumno)
    )

    rows = db.exec(stmt).all()

    return [
        ResponsableConParentescoPublic(
            idResponsable=r.idResponsable,
            nombre=r.nombre,
            apellido=r.apellido,
            dni=r.dni,
            email=r.email,
            nro_celular=r.nro_celular,
            direccion=r.direccion,
            parentesco=parentesco
        )
        for r, parentesco in rows
    ]
