# app/routers/profesionales.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.profesional import Profesional
from app.schemas.profesional import ProfesionalBase, ProfesionalResponse

router = APIRouter(
    prefix="/profesionales",
    tags=["2.1 Identidades - Profesionales"]
)

# ----------------- Funciones CRUD Básicas -----------------

def get_profesional_by_reg(db: Session, registro: str):
    return db.query(Profesional).filter(Profesional.registroProfesional == registro).first()

def create_profesional(db: Session, prof: ProfesionalBase):
    db_profesional = Profesional(**prof.model_dump())
    db.add(db_profesional)
    db.commit()
    db.refresh(db_profesional)
    return db_profesional

# ----------------- Endpoints -----------------

@router.post("/", response_model=ProfesionalResponse, status_code=status.HTTP_201_CREATED)
def alta_profesional(profesional: ProfesionalBase, db: Session = Depends(get_db)):
    if get_profesional_by_reg(db, profesional.registroProfesional):
        raise HTTPException(status_code=409, detail="Registro profesional duplicado.")
    return create_profesional(db=db, prof=profesional)

@router.get("/", response_model=List[ProfesionalResponse])
def listar_profesionales(db: Session = Depends(get_db)):
    return db.query(Profesional).all()