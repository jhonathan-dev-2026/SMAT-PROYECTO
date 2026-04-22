from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SMAT - Sistema de Monitoreo de Alerta Temprana",
    description="""
API robusta para la gestión y monitoreo de desastres naturales.
Permite la telemetría de sensores en tiempo real y el cálculo de niveles de riesgo.

**Entidades principales:**
* **Estaciones:** Puntos de monitoreo físico.
* **Lecturas:** Datos capturados por sensores.
* **Riesgos:** Análisis de criticidad basado en umbrales.
""",
    version="1.0.0",
    terms_of_service="http://unmsm.edu.pe/terms/",
    contact={
        "name": "Soporte Técnico SMAT - FISI - Jhonathan",
        "url": "http://fisi.unmsm.edu.pe",
        "email": "desarrollo.smat@unmsm.edu.pe",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

class EstacionCreate(BaseModel):
    id: int = Field(..., gt=0, description="ID único de la estación física")
    nombre: str = Field(..., min_length=3, description="Nombre descriptivo de la estación")
    ubicacion: str = Field(..., description="Ubicación o zona geográfica de monitoreo")

class LecturaCreate(BaseModel):
    estacion_id: int = Field(..., description="ID de la estación que envía el dato")
    valor: float = Field(..., description="Valor numérico capturado por el sensor")

@app.post(
    "/estaciones/", 
    status_code=status.HTTP_201_CREATED,
    tags=["Gestión de Infraestructura"],
    summary="Registrar una nueva estación de monitoreo",
    description="Inserta una estación física (ej. río, volcán, zona sísmica) en la base de datos relacional."
)
def crear_estacion(estacion: EstacionCreate, db: Session = Depends(get_db)):
    if db.query(models.EstacionDB).filter(models.EstacionDB.id == estacion.id).first():
        raise HTTPException(status_code=400, detail="Error: ID de estación ya registrado")
    nueva = models.EstacionDB(**estacion.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return {"status": "success", "data": nueva}

@app.post(
    "/lecturas/", 
    status_code=status.HTTP_201_CREATED,
    tags=["Telemetría de Sensores"],
    summary="Recibir datos de telemetría (IoT)",
    description="Recibe el valor capturado por un sensor y lo vincula a una estación existente mediante su ID."
)
def registrar_lectura(lectura: LecturaCreate, db: Session = Depends(get_db)):
    estacion = db.query(models.EstacionDB).filter(models.EstacionDB.id == lectura.estacion_id).first()
    if not estacion:
        raise HTTPException(status_code=404, detail="Operación fallida: Estación no existe")
    nueva_l = models.LecturaDB(**lectura.dict())
    db.add(nueva_l)
    db.commit()
    return {"status": "success", "message": "Lectura guardada en base de datos"}

@app.get(
    "/estaciones/{id}/historial",
    tags=["Reportes Históricos"],
    summary="Consultar historial y estadísticas",
    description="Realiza cálculos estadísticos (conteo y promedio) de las lecturas capturadas para una estación específica.",
    responses={404: {"description": "Estación no encontrada"}}
)
def obtener_historial(id: int, db: Session = Depends(get_db)):
    estacion = db.query(models.EstacionDB).filter(models.EstacionDB.id == id).first()
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    lecturas = db.query(models.LecturaDB).filter(models.LecturaDB.estacion_id == id).all()
    valores = [l.valor for l in lecturas]
    promedio = sum(valores) / len(valores) if valores else 0
    return {
        "estacion": estacion.nombre, 
        "promedio": round(promedio, 2), 
        "total_registros": len(valores),
        "historial": valores
    }

@app.get(
    "/estaciones/{id}/riesgo",
    tags=["Análisis de Riesgo"],
    summary="Evaluar nivel de peligro actual",
    description="Analiza la última lectura recibida y determina si el estado es NORMAL, ALERTA o PELIGRO según umbrales.",
    responses={404: {"description": "Sin lecturas suficientes para calcular riesgo"}}
)
def consultar_riesgo(id: int, db: Session = Depends(get_db)):
    ultima = db.query(models.LecturaDB).filter(models.LecturaDB.estacion_id == id).order_by(models.LecturaDB.id.desc()).first()
    if not ultima:
        raise HTTPException(status_code=404, detail="Sin lecturas suficientes")
    v = ultima.valor
    nivel = "PELIGRO" if v > 30 else "ALERTA" if v >= 15 else "NORMAL"
    color = "Rojo" if nivel == "PELIGRO" else "Naranja" if nivel == "ALERTA" else "Verde"
    return {"id": id, "valor_actual": v, "nivel": nivel, "indicador": color}

@app.get(
    "/reportes/criticos",
    tags=["Auditoría"],
    summary="Listar estaciones en estado crítico",
    description="Filtra y contabiliza estaciones cuyas lecturas superan un umbral de riesgo opcional (por defecto 30)."
)
def obtener_criticos(umbral: float = 30.0, db: Session = Depends(get_db)):
    lecturas_criticas = db.query(models.LecturaDB).filter(models.LecturaDB.valor > umbral).all()
    return {"criterio": f"Mayor a {umbral}", "cantidad_detecciones": len(lecturas_criticas)}

@app.get(
    "/estaciones/stats",
    tags=["Resumen Ejecutivo"],
    summary="Estado global del sistema",
    description="Proporciona un resumen administrativo del total de infraestructura y datos procesados por el SMAT."
)
def obtener_stats(db: Session = Depends(get_db)):
    total_e = db.query(models.EstacionDB).count()
    total_l = db.query(models.LecturaDB).count()
    return {"total_estaciones": total_e, "total_lecturas_procesadas": total_l}