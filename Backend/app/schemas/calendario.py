from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CalendarioBase(BaseModel):
    cuidador_id_cuidador: int
    reserva_id_reserva: Optional[int] = None
    fecha_inicio: datetime
    fecha_fin: datetime
    evento_id_evento: int

class CalendarioCreate(CalendarioBase):
    pass

class CalendarioUpdate(BaseModel):
    cuidador_id_cuidador: Optional[int] = None
    reserva_id_reserva: Optional[int] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    evento_id_evento: Optional[int] = None

class CalendarioResponse(CalendarioBase):
    id_calendario: int

    class Config:
        from_attributes = True
