def test_no_solapamiento(client, db_session):
    # Crear cita confirmada
    ...
    # Intentar crear otra en mismo horario
    response = client.post("/citas/", json={...})
    assert response.status_code == 400
