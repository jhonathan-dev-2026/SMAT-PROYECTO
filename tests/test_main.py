from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def get_auth_headers():
    response = client.post("/token")
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_01_crear_estacion_con_token():
    headers = get_auth_headers()
    resp = client.post("/estaciones/", headers=headers, json={
        "id": 800, 
        "nombre": "Estación Volcán Misti", 
        "ubicacion": "Arequipa"
    })
    assert resp.status_code == 201

def test_02_error_sin_token():
    """Verifica que el sistema protege los endpoints"""
    resp = client.post("/estaciones/", json={"id": 999, "nombre": "Hacker", "ubicacion": "Web"})
    assert resp.status_code == 401

def test_03_reto_integridad_estacion_inexistente():
    """Verifica el Reto de Integridad del Lab 4.4"""
    headers = get_auth_headers()
    resp = client.post("/lecturas/", headers=headers, json={
        "estacion_id": 9999,
        "valor": 25.5
    })
    assert resp.status_code == 404
    assert "Error de Integridad" in resp.json()["detail"]

def test_04_flujo_completo_protegido():
    headers = get_auth_headers()
    client.post("/estaciones/", headers=headers, json={"id": 801, "nombre": "Lima", "ubicacion": "Cercado"})
    client.post("/lecturas/", headers=headers, json={"estacion_id": 801, "valor": 10.0})
    client.post("/lecturas/", headers=headers, json={"estacion_id": 801, "valor": 50.0})
    
    resp = client.get("/estaciones/801/riesgo")
    assert resp.json()["nivel"] == "PELIGRO"

def test_05_verificar_stats_dashboard():
    resp = client.get("/estaciones/stats")
    assert resp.status_code == 200
    assert "punto_critico_maximo" in resp.json()