# app/routers/citas.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from typing import List

from app.database import get_db
from app.models.cita import Cita
from app.models.agenda import Agenda
from app.schemas.cita import CitaCreate, CitaResponse

router = APIRouter(
    prefix="/citas",
    tags=["2.2 Disponibilidad - Citas"]
)

# ----------------- Lógica de Negocio Clave -----------------

def validar_y_crear_cita(db: Session, cita: CitaCreate):
    # 1. Validación de Solapamiento con Agenda (Bloque Abierto)
    bloque_agenda = db.query(Agenda).filter(
        Agenda.profesionalId == cita.profesionalId,
        Agenda.unidadId == cita.unidadId,
        # La cita debe estar contenida en algún bloque de agenda
        Agenda.inicio <= cita.inicio,
        Agenda.fin >= cita.fin,
        Agenda.estado == 'abierto'
    ).first()

    if not bloque_agenda:
        raise HTTPException(status_code=400, detail="No hay disponibilidad de agenda para el profesional en ese horario y unidad.")
        
    # 2. Validación de Solapamiento con OTRAS Citas (Regla de No Solapamiento)
    # Buscamos citas existentes (confirmadas o solicitadas) que se solapen.
    # Solapamiento ocurre si: (inicio_existente < fin_nueva) AND (fin_existente > inicio_nueva)
    citas_existentes = db.query(Cita).filter(
        Cita.profesionalId == cita.profesionalId,
        Cita.unidadId == cita.unidadId,
        # Excluir citas canceladas o no asistidas
        Cita.estado.in_(['solicitada', 'confirmada']),
        or_(
            # Si el inicio de la cita existente cae dentro del nuevo periodo
            and_(Cita.inicio >= cita.inicio, Cita.inicio < cita.fin),
            # Si el fin de la cita existente cae dentro del nuevo periodo
            and_(Cita.fin > cita.inicio, Cita.fin <= cita.fin),
            # Si la cita existente contiene completamente al nuevo periodo
            and_(Cita.inicio <= cita.inicio, Cita.fin >= cita.fin)
        )
    ).count()

    if citas_existentes > 0 and bloque_agenda.capacidad == 1:
        # Si la capacidad es 1, cualquier solapamiento es un conflicto
        raise HTTPException(status_code=409, detail="Conflicto de horario: Ya existe una cita activa con ese profesional en el rango solicitado.")
    
    # 3. Validación de Capacidad (Regla de No Exceder Capacidad)
    if bloque_agenda.capacidad > 1:
        # Si la capacidad es mayor a 1, contamos cuántas citas caben en el bloque total
        # (Lógica simplificada, ya que la validación de solapamiento puede ser más compleja
        # en capacidad > 1, pero para la entrega inicial es aceptable).
        conteo_citas_en_bloque = db.query(Cita).filter(
            Cita.profesionalId == cita.profesionalId,
            Cita.unidadId == cita.unidadId,
            Cita.inicio >= bloque_agenda.inicio,
            Cita.fin <= bloque_agenda.fin,
            Cita.estado.in_(['solicitada', 'confirmada'])
        ).count()
        
        if conteo_citas_en_bloque >= bloque_agenda.capacidad:
             raise HTTPException(status_code=409, detail="Capacidad máxima excedida para el bloque de agenda del profesional.")

    # 4. Creación de la Cita
    db_cita = Cita(**cita.model_dump())
    db.add(db_cita)
    db.commit()
    db.refresh(db_cita)
    return db_cita

# ----------------- Endpoints -----------------

@router.post("/", response_model=CitaResponse, status_code=status.HTTP_201_CREATED)
def crear_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    """
    POST /citas: Crea una cita validando las reglas de No Solapamiento y Capacidad (Regla 2.2).
    """
    return validar_y_crear_cita(db, cita)

@router.get("/", response_model=List[CitaResponse])
def listar_citas(db: Session = Depends(get_db)):
    return db.query(Cita).all()