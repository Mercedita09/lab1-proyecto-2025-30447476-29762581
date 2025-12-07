from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import Base

class EpisodioAtencion(Base):
    __tablename__ = "episodios"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("personas.id"))

class NotaClinica(Base):
    __tablename__ = "notas_clinicas"
    id = Column(Integer, primary_key=True, index=True)
    episodio_id = Column(Integer, ForeignKey("episodios.id"))
    contenido = Column(String(500))

class Diagnostico(Base):
    __tablename__ = "diagnosticos"
    id = Column(Integer, primary_key=True, index=True)
    episodio_id = Column(Integer, ForeignKey("episodios.id"))
    descripcion = Column(String(200))
    principal = Column(Boolean, default=False)

class Consentimiento(Base):
    __tablename__ = "consentimientos"
    id = Column(Integer, primary_key=True, index=True)
    episodio_id = Column(Integer, ForeignKey("episodios.id"))
    tipo = Column(String(100))
