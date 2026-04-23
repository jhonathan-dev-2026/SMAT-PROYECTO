from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import engine, get_db
from .auth import crear_token_acceso, obtener_identidad_actual, Token

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SMAT - Sistema de Monitoreo de Alerta Temprana",
    description="""
## 🔐 Ecosistema SMAT v2.5 - Seguridad Avanzada JWT
API Profesional con protección de endpoints y validación de integridad cruzada.

**Seguridad Implementada:**
* **Autenticación:** JWT (JSON Web Tokens) con algoritmo HS256.
* **Autorización:** Protección de endpoints de escritura (POST).
* **Integridad:** Validación de existencia de llaves foráneas antes de inserción.
""",
    version="2.5.0",
    contact={
        "name": "Jhonathan Gomez - UNMSM FISI",
        "url": "https://github.com/jhonathan-dev-2026",
        "email": "jhonathan.gomez@unmsm.edu.pe",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token", response_model=Token, tags=["Seguridad"], summary="Login para obtener Token JWT")
async def login_para_obtener_token():
    """Genera un token válido para el administrador del sistema"""
    return {"access_token": crear_token_acceso({"sub": "admin_smat"}), "token_type": "bearer"}


@app.post("/estaciones/", status_code=201, tags=["Gestión de Infraestructura"], summary="Crear nueva estación (Protegido)")
def post_estacion(
    estacion: schemas.EstacionCreate, 
    db: Session = Depends(get_db),
    usuario_audit: str = Depends(obtener_identidad_actual)
):
    if crud.obtener_estacion_por_id(db, estacion.id):
        raise HTTPException(status_code=400, detail="ID de estación ya registrado")
    return crud.crear_nueva_estacion(db, estacion)

@app.get("/estaciones/", response_model=List[schemas.EstacionResponse], tags=["Gestión de Infraestructura"])
def get_estaciones(db: Session = Depends(get_db)):
    return crud.obtener_todas_las_estaciones(db)

@app.post("/lecturas/", status_code=201, tags=["Telemetría de Sensores"], summary="Registrar lectura (Protegido + Reto Integridad)")
def post_lectura(
    lectura: schemas.LecturaCreate, 
    db: Session = Depends(get_db),
    usuario_audit: str = Depends(obtener_identidad_actual)
):
    estacion_db = crud.obtener_estacion_por_id(db, lectura.estacion_id)
    if not estacion_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Error de Integridad: La estación con ID {lectura.estacion_id} no existe en la base de datos."
        )
    return crud.registrar_nueva_lectura(db, lectura)


@app.get("/estaciones/{id}/historial", tags=["Reportes Históricos"])
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

@app.get("/estaciones/{id}/riesgo", tags=["Análisis de Riesgo"])
def get_riesgo(id: int, db: Session = Depends(get_db)):
    ultima = crud.obtener_ultima_lectura(db, id)
    if not ultima:
        raise HTTPException(status_code=404, detail="Sin datos")
    nivel = "PELIGRO" if ultima.valor > 30 else "ALERTA" if ultima.valor >= 15 else "NORMAL"
    return {"id": id, "valor": ultima.valor, "nivel": nivel}

@app.get("/estaciones/stats", tags=["Resumen Ejecutivo"])
def get_stats(db: Session = Depends(get_db)):
    max_v = crud.obtener_valor_maximo(db)
    return {
        "total_estaciones": db.query(models.EstacionDB).count(),
        "total_lecturas_procesadas": db.query(models.LecturaDB).count(),
        "punto_critico_maximo": max_v if max_v else 0,
        "estado_global": "CRÍTICO" if (max_v and max_v > 30) else "ESTABLE"
    }