from sqlalchemy.orm import Session
from app.models.paciente import PersonaAtendida
from app.schemas.persona import PersonaCreate # Esquema Pydantic para la creación

def get_persona(db: Session, persona_id: int):
    return db.query(PersonaAtendida).filter(PersonaAtendida.id == persona_id).first()

def create_persona(db: Session, persona: PersonaCreate):
    db_persona = PersonaAtendida(**persona.model_dump())
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona