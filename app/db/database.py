from typing import Generator

from sqlmodel import SQLModel, Session, create_engine

from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)


def create_db_and_tables() -> None:
    import app.models.usuario
    import app.models.escuela
    import app.models.rol
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
