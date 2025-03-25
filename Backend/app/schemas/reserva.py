from pydantic import BaseModel
from datetime import date

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
    nombre_cuidador: str
    estado_reserva: str

    class Config:
        from_attributes = True  
