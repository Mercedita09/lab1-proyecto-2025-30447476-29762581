from pydantic import BaseModel

class ProfesionalBase(BaseModel):
    nombre: str
    especialidad: str
    registro: str

class ProfesionalCreate(ProfesionalBase):
    pass

class ProfesionalResponse(ProfesionalBase):
    id: int
    class Config:
        orm_mode = True
