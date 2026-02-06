from fastapi import HTTPException
from sqlmodel import select

from app.dependencies import SessionDep
from app.models.responsable import Responsable
from app.schemas.responsable import ResponsableCreate, ResponsableUpdate



# HELPERS


def _clean_str(v: str | None) -> str | None:
    if v is None:
        return None
    return str(v).strip()

def _clean_email(v: str | None) -> str | None:
    if v is None:
        return None
    return str(v).strip().lower()

def _require_not_empty(value: str | None, field_name: str):
    if value is not None and not str(value).strip():
        raise HTTPException(status_code=400, detail=f"El campo '{field_name}' no puede estar vacío")

def _exists_responsable_by_field(
    db: SessionDep,
    field,
    value: str,
    exclude_id: int | None = None,
) -> bool:
    stmt = select(Responsable).where(field == value)
    if exclude_id is not None:
        stmt = stmt.where(Responsable.idResponsable != exclude_id)
    return db.exec(stmt).first() is not None



# GETTERS


def get_one_responsable(idResponsable: int, db: SessionDep):
    return db.get(Responsable, idResponsable)

def get_responsable_by_dni(db: SessionDep, dni: str):
    stmt = select(Responsable).where(Responsable.dni == dni)
    return db.exec(stmt).first()



# CREATE


def add_responsable(db: SessionDep, responsable_in: ResponsableCreate):
    dni = _clean_str(responsable_in.dni) or ""
    email = _clean_email(getattr(responsable_in, "email", None)) or ""
    nro = _clean_str(getattr(responsable_in, "nro_celular", None)) or ""

    # obligatorios
    if not dni:
        raise HTTPException(status_code=400, detail="El DNI es obligatorio")
    if not email:
        raise HTTPException(status_code=400, detail="El email es obligatorio")
    if not nro:
        raise HTTPException(status_code=400, detail="El nro_celular es obligatorio")

    # unicidad (create)
    if _exists_responsable_by_field(db, Responsable.dni, dni):
        raise HTTPException(status_code=400, detail="Ya existe otro responsable con ese DNI")
    if _exists_responsable_by_field(db, Responsable.email, email):
        raise HTTPException(status_code=400, detail="Ya existe otro responsable con ese EMAIL")
    if _exists_responsable_by_field(db, Responsable.nro_celular, nro):
        raise HTTPException(status_code=400, detail="Ya existe otro responsable con ese Número de Celular")

    data = responsable_in.model_dump()
    data["dni"] = dni
    data["email"] = email
    data["nro_celular"] = nro

    db_resp = Responsable.model_validate(data)
    db.add(db_resp)
    db.commit()
    db.refresh(db_resp)
    return db_resp



# UPDATE


def update_responsable(db: SessionDep, responsable_existente: Responsable, responsable_nuevo: ResponsableUpdate):
    data = responsable_nuevo.model_dump(exclude_unset=True)

    # limpieza + no vacíos (si vienen)
    if "dni" in data:
        data["dni"] = _clean_str(data["dni"])
        _require_not_empty(data["dni"], "dni")

    if "email" in data:
        data["email"] = _clean_email(data["email"])
        _require_not_empty(data["email"], "email")

    if "nro_celular" in data:
        data["nro_celular"] = _clean_str(data["nro_celular"])
        _require_not_empty(data["nro_celular"], "nro_celular")

    if "nombre" in data:
        data["nombre"] = _clean_str(data["nombre"])
        _require_not_empty(data["nombre"], "nombre")

    if "apellido" in data:
        data["apellido"] = _clean_str(data["apellido"])
        _require_not_empty(data["apellido"], "apellido")

    if "direccion" in data:
        data["direccion"] = _clean_str(data["direccion"])
        _require_not_empty(data["direccion"], "direccion")

    # unicidad (update) excluyendo el mismo responsable
    rid = int(responsable_existente.idResponsable)

    if data.get("dni"):
        if _exists_responsable_by_field(db, Responsable.dni, data["dni"], exclude_id=rid):
            raise HTTPException(status_code=400, detail="Ya existe otro responsable con ese DNI")

    if data.get("email"):
        if _exists_responsable_by_field(db, Responsable.email, data["email"], exclude_id=rid):
            raise HTTPException(status_code=400, detail="Ya existe otro responsable con ese EMAIL")

    if data.get("nro_celular"):
        if _exists_responsable_by_field(db, Responsable.nro_celular, data["nro_celular"], exclude_id=rid):
            raise HTTPException(status_code=400, detail="Ya existe otro responsable con ese Número de Celular")

    responsable_existente.sqlmodel_update(data)
    db.add(responsable_existente)
    db.commit()
    db.refresh(responsable_existente)
    return responsable_existente



# DELETE


def delete_responsable(db: SessionDep, responsable: Responsable):
    db.delete(responsable)
    db.commit()
