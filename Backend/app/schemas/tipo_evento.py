from pydantic import BaseModel
from typing import Optional


class TipoEventoBase(BaseModel):
    descripcion: Optional[str]

    class Config:
        from_attributes = True
        
class TipoEventoCreate(TipoEventoBase):
    pass

class TipoEventoResponse(TipoEventoBase):
    id_evento: int
    descripcion: str

    class Config:
        from_attributes = True
