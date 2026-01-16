from typing import Annotated, Sequence

from sqlmodel import select
from app.dependencies import SessionDep
from app.models.escuela import Escuela 
from fastapi import APIRouter, HTTPException, Query

from app.schemas.escuela import EscuelaCreate, EscuelaPublic, EscuelaUpdate

router = APIRouter()


