from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import engine, get_db

# Generación de tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SMAT - Sistema de Monitoreo de Alerta Temprana",
    description="""
## API Profesional de Monitoreo Ambiental
### Laboratorio 4.3 - Refactorización, Middleware y Seguridad

Este ecosistema digital ha sido diseñado bajo estándares de **Clean Code** y **Arquitectura Modular**, asegurando una base de datos sólida y una comunicación segura para clientes externos.

**Funcionalidades Implementadas:**
* **Modularización:** Estructura basada en módulos especializados (Models, Schemas, CRUD).
* **Middleware CORS:** Configuración de seguridad para interoperabilidad multiplataforma.
* **Dashboard de Auditoría:** Reportes ejecutivos dinámicos con funciones SQL avanzadas.
* **TDD (Test Driven Development):** Validación integral del sistema mediante Pytest.

**Información del Desarrollador:**
* **Facultad:** Ingeniería de Sistemas e Informática (UNMSM)
* **Materia:** Desarrollo Basado en Plataformas
""",
    version="2.0.1",
    contact={
        "name": "Jhonathan Gomez - Soporte SMAT",
        "url": "https://github.com/jhonathan-dev-2026",
        "email": "jhonathan.gomez@unmsm.edu.pe",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Configuración de Seguridad CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoints de Gestión de Infraestructura ---

@app.post("/estaciones/", status_code=201, tags=["Gestión de Infraestructura"], summary="Crear nueva estación")
def post_estacion(estacion: schemas.EstacionCreate, db: Session = Depends(get_db)):
    if crud.obtener_estacion_por_id(db, estacion.id):
        raise HTTPException(status_code=400, detail="ID ya registrado")
    return crud.crear_nueva_estacion(db, estacion)

@app.get("/estaciones/", response_model=List[schemas.EstacionResponse], tags=["Gestión de Infraestructura"], summary="Listar todas las estaciones")
def get_estaciones(db: Session = Depends(get_db)):
    return crud.obtener_todas_las_estaciones(db)

# --- Endpoints de Telemetría ---

@app.post("/lecturas/", status_code=201, tags=["Telemetría de Sensores"], summary="Registrar lectura de sensor")
def post_lectura(lectura: schemas.LecturaCreate, db: Session = Depends(get_db)):
    if not crud.obtener_estacion_por_id(db, lectura.estacion_id):
        raise HTTPException(status_code=404, detail="Estación no existe")
    return crud.registrar_nueva_lectura(db, lectura)

# --- Endpoints de Reportes y Análisis ---

@app.get("/estaciones/{id}/historial", tags=["Reportes Históricos"], summary="Obtener historial y promedio")
def get_historial(id: int, db: Session = Depends(get_db)):
    estacion = crud.obtener_estacion_por_id(db, id)
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    lecturas = crud.obtener_lecturas_por_estacion(db, id)
    valores = [l.valor for l in lecturas]
    promedio = sum(valores) / len(valores) if valores else 0
    return {
        "estacion": estacion.nombre, 
        "promedio": round(promedio, 2), 
        "total_registros": len(valores), 
        "data": valores
    }

@app.get("/estaciones/{id}/riesgo", tags=["Análisis de Riesgo"], summary="Evaluar nivel de riesgo actual")
def get_riesgo(id: int, db: Session = Depends(get_db)):
    ultima = crud.obtener_ultima_lectura(db, id)
    if not ultima:
        raise HTTPException(status_code=404, detail="Sin datos registrados para esta estación")
    nivel = "PELIGRO" if ultima.valor > 30 else "ALERTA" if ultima.valor >= 15 else "NORMAL"
    return {"id": id, "valor": ultima.valor, "nivel": nivel}

# --- Endpoints de Resumen Ejecutivo (Reto Final) ---

@app.get("/estaciones/stats", tags=["Resumen Ejecutivo"], summary="Dashboard de Auditoría")
def get_stats(db: Session = Depends(get_db)):
    max_v = crud.obtener_valor_maximo(db)
    return {
        "total_estaciones": db.query(models.EstacionDB).count(),
        "total_lecturas_procesadas": db.query(models.LecturaDB).count(),
        "punto_critico_maximo": max_v if max_v else 0,
        "estado_global": "CRÍTICO" if (max_v and max_v > 30) else "ESTABLE"
    }