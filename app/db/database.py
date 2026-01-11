import os
from sqlmodel import SQLModel, create_engine
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
        import app.models
        SQLModel.metadata.create_all(engine)
