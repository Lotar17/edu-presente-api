from sqlmodel import Field, Relationship
from app.schemas.escuela import EscuelaBase
from app.models.rol import Rol


class Escuela(EscuelaBase, table=True):
        idEscuela: int | None = Field(default=None, primary_key=True)
        usuarios: list["Usuario"] = Relationship(back_populates="escuelas", link_model=Rol)
