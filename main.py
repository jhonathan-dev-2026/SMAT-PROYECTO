from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SMAT Pro - Sistema de Monitoreo Ambiental",
    description="API profesional con persistencia en SQLite y lógica de riesgo avanzada"
)

class EstacionCreate(BaseModel):
    id: int = Field(..., gt=0, description="El ID debe ser mayor a 0")
    nombre: str = Field(..., min_length=3)
    ubicacion: str

class LecturaCreate(BaseModel):
    estacion_id: int
    valor: float = Field(..., description="Valor de la lectura capturada")


@app.post("/estaciones/", status_code=status.HTTP_201_CREATED)
def crear_estacion(estacion: EstacionCreate, db: Session = Depends(get_db)):
    if db.query(models.EstacionDB).filter(models.EstacionDB.id == estacion.id).first():
        raise HTTPException(status_code=400, detail="Error: ID de estación ya registrado")
    
    nueva = models.EstacionDB(**estacion.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return {"status": "success", "data": nueva}

@app.post("/lecturas/", status_code=status.HTTP_201_CREATED)
def registrar_lectura(lectura: LecturaCreate, db: Session = Depends(get_db)):
    estacion = db.query(models.EstacionDB).filter(models.EstacionDB.id == lectura.estacion_id).first()
    if not estacion:
        raise HTTPException(status_code=404, detail="Operación fallida: Estación no existe")
    
    nueva_l = models.LecturaDB(**lectura.dict())
    db.add(nueva_l)
    db.commit()
    return {"status": "success", "message": "Lectura guardada en base de datos"}

@app.get("/estaciones/{id}/historial")
def obtener_historial(id: int, db: Session = Depends(get_db)):
    estacion = db.query(models.EstacionDB).filter(models.EstacionDB.id == id).first()
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    
    lecturas = db.query(models.LecturaDB).filter(models.LecturaDB.estacion_id == id).all()
    valores = [l.valor for l in lecturas]
    promedio = sum(valores) / len(valores) if valores else 0
    
    return {
        "estacion": estacion.nombre,
        "ubicacion": estacion.ubicacion,
        "historial": valores,
        "promedio": round(promedio, 2),
        "total_registros": len(valores)
    }

@app.get("/estaciones/{id}/riesgo")
def consultar_riesgo(id: int, db: Session = Depends(get_db)):
    ultima = db.query(models.LecturaDB).filter(models.LecturaDB.estacion_id == id).order_by(models.LecturaDB.id.desc()).first()
    
    if not ultima:
        raise HTTPException(status_code=404, detail="Sin lecturas suficientes para calcular riesgo")
    
    v = ultima.valor
    if v > 30: 
        nivel, color = "PELIGRO", "Rojo"
    elif 15 <= v <= 30: 
        nivel, color = "ALERTA", "Naranja"
    else: 
        nivel, color = "NORMAL", "Verde"
        
    return {"id": id, "valor_actual": v, "nivel": nivel, "indicador": color}