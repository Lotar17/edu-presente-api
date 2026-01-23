from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.core.config import DATABASE_URL
from app.db.database import engine

# Routers
from app.routers import (
    auth,
    usuario,
    escuela,
    curso,
    alumno,
    responsable,
    rol,
    admin,
    director,
)

# Importar modelos para que SQLModel cree tablas
from app.models.usuario import Usuario
from app.models.escuela import Escuela
from app.models.rol import Rol
from app.models.curso import Curso
from app.models.alumno import Alumno
from app.models.responsable import Responsable
from app.models.alumno_responsable import AlumnoResponsable


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


app = FastAPI(
    title="EduPresente API",
    version="1.0.0",
)

# CORS (Angular dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    print("✅ DB lista. Conectado a:", DATABASE_URL)


# Healthcheck
@app.get("/health")
def health():
    return {"status": "ok"}


# Routers
app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(escuela.router)
app.include_router(curso.router)
app.include_router(alumno.router)
app.include_router(responsable.router)
app.include_router(rol.router)
app.include_router(admin.router)
app.include_router(director.router)
