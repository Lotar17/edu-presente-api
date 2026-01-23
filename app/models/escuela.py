from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship
from app.schemas.escuela import EscuelaBase
from app.models.rol import Rol


if TYPE_CHECKING:
    from .usuario import Usuario

class Escuela(EscuelaBase, table=True):
        CUE: str | None = Field(max_length=9,min_length=9, primary_key=True)
        usuarios: list["Usuario"] = Relationship(back_populates="escuelas", link_model=Rol)
