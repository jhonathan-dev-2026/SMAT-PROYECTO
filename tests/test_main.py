from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_01_crear_estacion_principal():
    """Verifica creación (corregido para arquitectura profesional)"""
    resp = client.post("/estaciones/", json={
        "id": 800, 
        "nombre": "Estación Volcán Misti", 
        "ubicacion": "Arequipa"
    })
    assert resp.status_code == 201
    assert resp.json()["nombre"] == "Estación Volcán Misti"

def test_02_error_id_repetido():
    client.post("/estaciones/", json={"id": 801, "nombre": "Test", "ubicacion": "Lima"})
    resp = client.post("/estaciones/", json={"id": 801, "nombre": "Duplicado", "ubicacion": "Lima"})
    assert resp.status_code == 400

def test_03_flujo_historial_y_promedio():
    client.post("/lecturas/", json={"estacion_id": 801, "valor": 10.0})
    client.post("/lecturas/", json={"estacion_id": 801, "valor": 20.0})
    resp = client.get("/estaciones/801/historial")
    assert resp.json()["promedio"] == 15.0
    assert resp.json()["total_registros"] == 2

def test_04_evaluacion_riesgo_critico():
    client.post("/lecturas/", json={"estacion_id": 801, "valor": 50.0})
    resp = client.get("/estaciones/801/riesgo")
    assert resp.json()["nivel"] == "PELIGRO"

def test_05_verificar_stats_dashboad():
    """Prueba del Reto Final"""
    resp = client.get("/estaciones/stats")
    assert resp.status_code == 200
    assert "punto_critico_maximo" in resp.json()