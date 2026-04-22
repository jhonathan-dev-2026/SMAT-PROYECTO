from pydantic import BaseModel, Field
from typing import List, Optional

class LecturaBase(BaseModel):
    estacion_id: int = Field(..., description="ID de la estación que envía el dato")
    valor: float = Field(..., description="Valor numérico capturado por el sensor")

class LecturaCreate(LecturaBase):
    pass

class LecturaResponse(LecturaBase):
    id: int
    class Config:
        from_attributes = True

# --- Esquemas para Estaciones ---
class EstacionBase(BaseModel):
    id: int = Field(..., gt=0, description="ID único de la estación física")
    nombre: str = Field(..., min_length=3, description="Nombre descriptivo de la estación")
    ubicacion: str = Field(..., description="Ubicación o zona geográfica de monitoreo")

class EstacionCreate(EstacionBase):
    pass

class EstacionResponse(EstacionBase):
    class Config:
        from_attributes = True