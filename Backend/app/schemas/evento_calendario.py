from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from schemas.tipo_evento import TipoEventoBase

class EventoCalendarioBase(BaseModel):
    calendario_id: int
    reserva_id_reserva: Optional[int] = None
    fecha_inicio: datetime
    fecha_fin: datetime
    evento_id_evento: int
    evento: Optional[TipoEventoBase]
                     
    class Config:
        from_attributes = True


class EventoCalendarioCreate(EventoCalendarioBase):
    pass

class EventoCalendarioUpdate(EventoCalendarioBase):
    pass

class EventoCalendarioResponse(EventoCalendarioBase):
    id_evento: int

    class Config:
        from_attributes = True