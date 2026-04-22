from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas

def obtener_estacion_por_id(db: Session, id: int):
    return db.query(models.EstacionDB).filter(models.EstacionDB.id == id).first()

def obtener_todas_las_estaciones(db: Session):
    return db.query(models.EstacionDB).all()

def crear_nueva_estacion(db: Session, estacion: schemas.EstacionCreate):
    nueva = models.EstacionDB(**estacion.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def registrar_nueva_lectura(db: Session, lectura: schemas.LecturaCreate):
    nueva = models.LecturaDB(**lectura.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def obtener_lecturas_por_estacion(db: Session, estacion_id: int):
    return db.query(models.LecturaDB).filter(models.LecturaDB.estacion_id == estacion_id).all()

def obtener_ultima_lectura(db: Session, estacion_id: int):
    return db.query(models.LecturaDB).filter(models.LecturaDB.estacion_id == estacion_id).order_by(models.LecturaDB.id.desc()).first()

def contar_criticos(db: Session, umbral: float):
    return db.query(models.LecturaDB).filter(models.LecturaDB.valor > umbral).count()

def obtener_valor_maximo(db: Session):
    # Reto Final: Obtiene el valor más alto registrado en el sistema
    return db.query(func.max(models.LecturaDB.valor)).scalar()