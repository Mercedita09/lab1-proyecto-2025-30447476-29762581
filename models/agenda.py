# app/models/agenda.py
from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base

class Agenda(Base):
    """Corresponde a los bloques de Agenda - Sección 2.2"""
    __tablename__ = 'Agenda'

    id = Column(Integer, primary_key=True, index=True)
    profesionalId = Column(Integer, ForeignKey('Profesionales.id'), nullable=False)
    unidadId = Column(Integer, ForeignKey('UnidadesAtencion.id'), nullable=False)
    inicio = Column(DateTime, nullable=False)
    fin = Column(DateTime, nullable=False)
    capacidad = Column(Integer, default=1, nullable=False)
    estado = Column(Enum('abierto', 'cerrado', 'reservado'), default='abierto', nullable=False)

    # Relaciones (opcional, pero útil para SQLAlchemy)
    profesional = relationship("Profesional")
    unidad = relationship("UnidadAtencion")
    
    # Restricción para evitar bloques duplicados en el mismo tiempo
    __table_args__ = (UniqueConstraint('profesionalId', 'inicio', 'fin', name='idx_agenda_profesional_tiempo'),)