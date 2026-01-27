# app/routers/curso.py
from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from sqlalchemy import func

from app.dependencies import SessionDep
from app.models.curso import Curso
from app.models.escuela import Escuela
from app.models.usuario import Usuario
from app.models.alumno import Alumno

from app.schemas.curso import CursoCreate, CursoPublic, CursoUpdate
from app.schemas.docente import CursoAsignadoPublic, EscuelaCursosPublic, CursoOption

router = APIRouter(prefix="/cursos", tags=["Cursos"])


@router.get("/", response_model=list[CursoPublic])
def list_cursos(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=200)] = 100,
    escuelaId: int | None = None,
):
    q = select(Curso)
    if escuelaId:
        q = q.where(Curso.idEscuela == escuelaId)
    return session.exec(q.offset(offset).limit(limit)).all()


@router.get("/mis", response_model=list[CursoAsignadoPublic])
def mis_cursos_docente(session: SessionDep, docenteId: int):
    q = (
        select(
            Curso.idCurso.label("cursoId"),
            Curso.nombre.label("cursoNombre"),
            Curso.idEscuela.label("escuelaId"),
            Escuela.nombre.label("escuelaNombre"),
            func.count(Alumno.idAlumno).label("alumnosCount"),
        )
        .join(Escuela, Escuela.idEscuela == Curso.idEscuela)
        .outerjoin(Alumno, Alumno.idCurso == Curso.idCurso)
        .where(Curso.idDocente == docenteId)
        .group_by(Curso.idCurso, Curso.nombre, Curso.idEscuela, Escuela.nombre)
        .order_by(Escuela.nombre.asc(), Curso.nombre.asc())
    )

    rows = session.exec(q).all()

    return [
        CursoAsignadoPublic(
            escuelaId=r.escuelaId,
            escuelaNombre=r.escuelaNombre,
            cursoId=r.cursoId,
            cursoNombre=r.cursoNombre,
            alumnosCount=int(r.alumnosCount or 0),
            turno=None,
            estado="Activo",
            icon="groups",
        )
        for r in rows
    ]


# ✅ IMPORTANTE: ESTE VA ANTES DE /{curso_id}
@router.get("/filtros", response_model=list[EscuelaCursosPublic])
def filtros_docente(session: SessionDep, docenteId: int):
    q = (
        select(
            Escuela.idEscuela,
            Escuela.nombre,
            Curso.idCurso,
            Curso.nombre,
            Curso.division,
            Curso.cicloLectivo,
        )
        .join(Curso, Curso.idEscuela == Escuela.idEscuela)
        .where(Curso.idDocente == docenteId)
        .order_by(Escuela.nombre.asc(), Curso.nombre.asc())
    )

    rows = session.exec(q).all()

    map_esc: dict[int, EscuelaCursosPublic] = {}

    for r in rows:
        esc_id = r[0]
        esc_nom = r[1]

        if esc_id not in map_esc:
            map_esc[esc_id] = EscuelaCursosPublic(
                escuelaId=esc_id,
                escuelaNombre=esc_nom,
                cursos=[]
            )

        map_esc[esc_id].cursos.append(
            CursoOption(
                cursoId=r[2],
                cursoNombre=r[3],
                division=r[4],
                cicloLectivo=r[5],
            )
        )

    return list(map_esc.values())


@router.get("/{curso_id}", response_model=CursoPublic)
def get_curso(curso_id: int, session: SessionDep):
    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso


@router.post("/", response_model=CursoPublic, status_code=201)
def create_curso(payload: CursoCreate, session: SessionDep):
    escuela = session.get(Escuela, payload.escuelaId)
    if not escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")

    if payload.docenteId is not None:
        docente = session.get(Usuario, payload.docenteId)
        if not docente:
            raise HTTPException(status_code=404, detail="Docente no encontrado")

    curso = Curso(
        idEscuela=payload.escuelaId,
        idDocente=payload.docenteId,
        nombre=payload.nombre,
        division=payload.division,
        cicloLectivo=payload.cicloLectivo
    )
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso


@router.patch("/{curso_id}", response_model=CursoPublic)
def update_curso(curso_id: int, payload: CursoUpdate, session: SessionDep):
    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    data = payload.model_dump(exclude_unset=True)

    data.pop("grado", None)
    data.pop("turno", None)

    if "escuelaId" in data:
        escuela = session.get(Escuela, data["escuelaId"])
        if not escuela:
            raise HTTPException(status_code=404, detail="Escuela no encontrada")
        data["idEscuela"] = data.pop("escuelaId")

    if "docenteId" in data:
        docente_id = data.pop("docenteId")
        if docente_id is not None:
            docente = session.get(Usuario, docente_id)
            if not docente:
                raise HTTPException(status_code=404, detail="Docente no encontrado")
        data["idDocente"] = docente_id

    curso.sqlmodel_update(data)
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso


@router.delete("/{curso_id}", status_code=204)
def delete_curso(curso_id: int, session: SessionDep):
    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    session.delete(curso)
    session.commit()
    return None
