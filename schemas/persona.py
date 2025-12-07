# app/schemas/persona.py
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

# Esquema para la creación (datos de entrada)
class PersonaCreate(BaseModel):
    tipoDocumento: str
    numeroDocumento: str
    nombres: str
    apellidos: str
    fechaNacimiento: date
    sexo: str
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    contactoEmergencia: Optional[str] = None

# Esquema para la respuesta (datos de salida, incluye el ID y estado)
class PersonaResponse(PersonaCreate):
    id: int
    estado: str

    class Config:
        from_attributes = True # Permite mapear campos desde el modelo ORM (SQLAlchemy)