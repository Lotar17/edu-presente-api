# app/routers/asistencia.py
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.dependencies import SessionDep
from app.models.curso import Curso
from app.models.alumno import Alumno

router = APIRouter(prefix="/asistencia", tags=["Asistencia"])

@router.get("/alumnos")
def alumnos_para_asistencia(session: SessionDep, cursoId: int, docenteId: int):
    curso = session.get(Curso, cursoId)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    if curso.idDocente != docenteId:
        raise HTTPException(status_code=403, detail="Curso no asignado a este docente")

    alumnos = session.exec(select(Alumno).where(Alumno.idCurso == cursoId)).all()

    # devolvemos en formato compatible con tu front (Alumno)
    return [
        {
            "id": a.idAlumno,
            "nombre": a.nombre,
            "apellido": a.apellido,
            "dni": getattr(a, "dni", None),
            "estado": getattr(a, "estado", "Activo"),
            "cursoId": a.idCurso,
        }
        for a in alumnos
    ]
