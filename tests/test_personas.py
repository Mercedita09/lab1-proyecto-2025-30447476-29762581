# app/tests/test_personas.py
import pytest
from httpx import AsyncClient
from app.main import app

# Cliente asíncrono para interactuar con la aplicación
@pytest.mark.asyncio
async def test_crear_persona_ok():
    """Prueba la creación exitosa de un nuevo paciente (PersonaAtendida)."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        datos_paciente = {
            "tipoDocumento": "CC",
            "numeroDocumento": "1000111222",
            "nombres": "Ana",
            "apellidos": "Gomez",
            "fechaNacimiento": "1990-05-15",
            "sexo": "F",
            "correo": "ana.gomez@mail.com",
            "telefono": "3001234567",
            "direccion": "Calle 10 # 5-20",
            "contactoEmergencia": "Juan Gomez (3001112233)"
        }
        response = await ac.post("/personas/", json=datos_paciente)

    assert response.status_code == 201 # HTTP 201 CREATED
    assert response.json()["nombres"] == "Ana"
    assert response.json()["estado"] == "activo"

@pytest.mark.asyncio
async def test_crear_persona_documento_duplicado():
    """Prueba la regla de negocio: documento de identidad debe ser único (HTTP 409)."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Primer POST (debería ser exitoso)
        datos_paciente = {
            "tipoDocumento": "CC",
            "numeroDocumento": "999888777",
            "nombres": "Pedro",
            "apellidos": "Perez",
            "fechaNacimiento": "1985-01-01",
            "sexo": "M"
        }
        await ac.post("/personas/", json=datos_paciente) 
        
        # Segundo POST con el mismo documento (debería fallar)
        response_duplicado = await ac.post("/personas/", json=datos_paciente) 

    assert response_duplicado.status_code == 409 # HTTP 409 CONFLICT
    assert "Ya existe una persona registrada" in response_duplicado.json()["detail"]