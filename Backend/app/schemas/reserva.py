from pydantic import BaseModel
from datetime import date
from typing import Optional  


class ReservaBase(BaseModel):
    cliente_id_cliente: int
    cuidador_id_cuidador: int
    fecha_inicio: date
    fecha_fin: date
    cantidad_mascotas: int
    precio_total: float
    estado_reserva_id_estado: int

class ReservaCreate(ReservaBase):
    pass

class ReservaUpdate(ReservaBase):
    pass

class ReservaResponse(ReservaBase):
    id_reserva: int
    fecha_inicio: date
    fecha_fin: date
    cantidad_mascotas: int
    nombre_cuidador: Optional[str] = None  # Campo opcional
    estado_reserva_id_estado: Optional[int] = None  # Campo opcional
    descripcion: Optional[str] = None  # Campo opcional


    class Config:
        from_attributes = True  
