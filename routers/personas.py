# app/routers/personas.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import exc
from typing import List

from app.database import get_db
from app.models.persona import PersonaAtendida
from app.schemas.persona import PersonaCreate, PersonaResponse

router = APIRouter(
    prefix="/personas",
    tags=["2.1 Identidades - Personas Atendidas"] # Tag para Swagger
)

# ----------------- Funciones CRUD Básicas (Repositorio/Servicio simplificado) -----------------

def get_persona_by_doc(db: Session, doc_num: str):
    """Consulta si el documento ya existe (Regla de unicidad)."""
    return db.query(PersonaAtendida).filter(
        PersonaAtendida.numeroDocumento == doc_num
    ).first()

def create_persona(db: Session, persona: PersonaCreate):
    """Crea un nuevo registro de Persona Atendida."""
    # Convertir Pydantic a diccionario para crear el modelo ORM
    db_persona = PersonaAtendida(**persona.model_dump())
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona

# ----------------- Endpoints (Controladores) -----------------

@router.post("/", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED)
def alta_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    """
    POST /personas: Crea una nueva Persona Atendida (Paciente).
    Regla: Documento de identidad debe ser único.
    """
    # Validación de unicidad
    if get_persona_by_doc(db, persona.numeroDocumento):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error: Ya existe una persona registrada con ese número de documento."
        )
    return create_persona(db=db, persona=persona)

@router.get("/{persona_id}", response_model=PersonaResponse)
def consulta_persona(persona_id: int, db: Session = Depends(get_db)):
    """GET /personas/{id}: Consulta los datos de una persona."""
    db_persona = db.query(PersonaAtendida).filter(
        PersonaAtendida.id == persona_id
    ).first()
    if db_persona is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Persona no encontrada"
        )
    return db_persona
    
@router.get("/", response_model=List[PersonaResponse])
def listar_personas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """GET /personas: Lista personas con paginación (Requisito: paginación)"""
    return db.query(PersonaAtendida).offset(skip).limit(limit).all()

# Falta implementar PATCH (cambios) y DELETE lógico (cambio de estado a 'inactivo')