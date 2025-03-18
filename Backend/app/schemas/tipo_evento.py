from pydantic import BaseModel
from typing import Optional


class TipoEventoBase(BaseModel):
    descripcion: Optional[str]

class TipoEventoCreate(TipoEventoBase):
    pass

class TipoEventoResponse(TipoEventoBase):
    id_tipo_evento: int
    descripcion: str

    class Config:
        from_attributes = True
