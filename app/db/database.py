import os
from sqlmodel import SQLModel, create_engine
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
        import app.models.usuario
        import app.models.escuela
        import app.models.rol
        SQLModel.metadata.create_all(engine)
