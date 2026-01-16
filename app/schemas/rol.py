from sqlmodel import SQLModel, Field

class RolBase(SQLModel):
    descripcion: str = Field(max_length=255)

class RolPublic(RolBase):
    pass

class RolCreate(RolBase):
    pass

class RolUpdate(SQLModel):
    descripcion: str | None = None
