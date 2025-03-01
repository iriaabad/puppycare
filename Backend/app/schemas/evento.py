from pydantic import BaseModel

class EventoBase(BaseModel):
    descripcion: str

class EventoCreate(EventoBase):
    pass

class EventoResponse(EventoBase):
    id_evento: int
    descripcion: str

    class Config:
        from_attributes = True
