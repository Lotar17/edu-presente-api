from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from app.dependencies import SessionDep
from app.models.responsable import Responsable
from app.models.alumno import Alumno
from app.models.alumno_responsable import AlumnoResponsable
from app.schemas.responsable import (
    ResponsableCreate,
    ResponsablePublic,
    ResponsableUpdate,
    VincularResponsableRequest
)

router = APIRouter(prefix="/responsables", tags=["Responsables"])


# ----------------------------
# CRUD Responsables
# ----------------------------
@router.get("/", response_model=list[ResponsablePublic])
def list_responsables(
    session: SessionDep,
    alumnoId: int | None = Query(default=None),
):
    # Si piden por alumno: devolver responsables asociados
    if alumnoId is not None:
        stmt = (
            select(Responsable)
            .join(AlumnoResponsable, AlumnoResponsable.idResponsable == Responsable.idResponsable)
            .where(AlumnoResponsable.idAlumno == alumnoId)
        )
        return session.exec(stmt).all()

    return session.exec(select(Responsable)).all()


@router.get("/{responsable_id}", response_model=ResponsablePublic)
def get_responsable(session: SessionDep, responsable_id: int):
    r = session.get(Responsable, responsable_id)
    if not r:
        raise HTTPException(status_code=404, detail="Responsable no encontrado")
    return r


@router.post("/", response_model=ResponsablePublic, status_code=201)
def create_responsable(session: SessionDep, data: ResponsableCreate):
    r = Responsable.model_validate(data)
    session.add(r)
    session.commit()
    session.refresh(r)
    return r


@router.patch("/{responsable_id}", response_model=ResponsablePublic)
def update_responsable(session: SessionDep, responsable_id: int, data: ResponsableUpdate):
    r = session.get(Responsable, responsable_id)
    if not r:
        raise HTTPException(status_code=404, detail="Responsable no encontrado")

    payload = data.model_dump(exclude_unset=True)
    r.sqlmodel_update(payload)

    session.add(r)
    session.commit()
    session.refresh(r)
    return r


@router.delete("/{responsable_id}", status_code=204)
def delete_responsable(session: SessionDep, responsable_id: int):
    r = session.get(Responsable, responsable_id)
    if not r:
        raise HTTPException(status_code=404, detail="Responsable no encontrado")

    # borrar vínculos primero (evita FK)
    links = session.exec(
        select(AlumnoResponsable).where(AlumnoResponsable.idResponsable == responsable_id)
    ).all()
    for l in links:
        session.delete(l)

    session.delete(r)
    session.commit()
    return None


# ----------------------------
# Vincular / Desvincular con parentesco
# ----------------------------
@router.post("/vincular", status_code=201)
def vincular_responsable(session: SessionDep, data: VincularResponsableRequest):
    alumno = session.get(Alumno, data.idAlumno)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    resp = session.get(Responsable, data.idResponsable)
    if not resp:
        raise HTTPException(status_code=404, detail="Responsable no encontrado")

    # evitar duplicados
    existente = session.get(AlumnoResponsable, (data.idAlumno, data.idResponsable))
    if existente:
        existente.parentesco = data.parentesco
        session.add(existente)
        session.commit()
        return {"ok": True, "mensaje": "Vínculo actualizado"}

    link = AlumnoResponsable(
        idAlumno=data.idAlumno,
        idResponsable=data.idResponsable,
        parentesco=data.parentesco
    )
    session.add(link)
    session.commit()
    return {"ok": True, "mensaje": "Vínculo creado"}


@router.delete("/vincular", status_code=204)
def desvincular_responsable(
    session: SessionDep,
    idAlumno: int = Query(...),
    idResponsable: int = Query(...),
):
    link = session.get(AlumnoResponsable, (idAlumno, idResponsable))
    if not link:
        raise HTTPException(status_code=404, detail="Vínculo no encontrado")

    session.delete(link)
    session.commit()
    return None
