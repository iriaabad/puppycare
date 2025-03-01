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

class Reserva(ReservaBase):
    id_reserva: int

    class Config:
        from_attributes = True
