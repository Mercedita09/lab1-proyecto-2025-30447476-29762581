from sqlalchemy import Column, Integer, String, Date, Enum, Boolean, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PersonaAtendida(Base):
    __tablename__ = 'PersonasAtendidas'

    id = Column(Integer, primary_key=True, index=True)
    tipoDocumento = Column(String(10))
    numeroDocumento = Column(String(20), unique=True)
    nombres = Column(String(100))
    apellidos = Column(String(100))
    fechaNacimiento = Column(Date)
    sexo = Column(Enum('M', 'F', 'Otro'))
    correo = Column(String(100))
    telefono = Column(String(20))
    direccion = Column(String(255))
    contactoEmergencia = Column(String(255))
    estado = Column(Enum('activo', 'inactivo'), default='activo')
 