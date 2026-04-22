from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_01_crear_estacion_principal():
    """Verifica la creación de la estación base en el volcán"""
    resp = client.post("/estaciones/", json={
        "id": 500, 
        "nombre": "Estación Misti-Alpha", 
        "ubicacion": "Arequipa Norte"
    })
    assert resp.status_code == 201
    assert resp.json()["data"]["nombre"] == "Estación Misti-Alpha"

def test_02_error_id_repetido():
    """Verifica que el sistema no duplique estaciones existentes"""
    client.post("/estaciones/", json={
        "id": 501, 
        "nombre": "Estación Rímac-Central", 
        "ubicacion": "Lima Este"
    })
    resp = client.post("/estaciones/", json={
        "id": 501, 
        "nombre": "Estación Duplicada", 
        "ubicacion": "Error"
    })
    assert resp.status_code == 400

def test_03_flujo_historial_y_promedio():
    """Verifica el cálculo de promedio con datos de sensores reales"""
    client.post("/lecturas/", json={"estacion_id": 501, "valor": 12.5})
    client.post("/lecturas/", json={"estacion_id": 501, "valor": 25.0})
    client.post("/lecturas/", json={"estacion_id": 501, "valor": 37.5})
    
    resp = client.get("/estaciones/501/historial")
    assert resp.json()["promedio"] == 25.0
    assert resp.json()["total_registros"] == 3

def test_04_evaluacion_riesgo_critico():
    """Verifica que el sistema detecte el nivel de PELIGRO (>30)"""
    client.post("/lecturas/", json={"estacion_id": 501, "valor": 45.0})
    resp = client.get("/estaciones/501/riesgo")
    assert resp.json()["nivel"] == "PELIGRO"

def test_05_error_estacion_no_configurada():
    """Verifica el manejo de errores para estaciones que no existen"""
    resp = client.get("/estaciones/9999/riesgo")
    assert resp.status_code == 404