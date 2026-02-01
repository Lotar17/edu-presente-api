from sqlmodel import Field, Relationship
from app.models.parentesco import Parentesco
from app.schemas.responsable import ResponsableBase
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .alumno import Alumno


class Responsable(ResponsableBase, table=True):
    idResponsable: int | None = Field(default=None, primary_key=True)
    alumnos: list["Alumno"] = Relationship(back_populates="responsables", link_model=Parentesco)
