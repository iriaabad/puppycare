from pydantic import BaseModel

class EstadoReservaBase(BaseModel):
    descripcion: str

class EstadoReservaCreate(EstadoReservaBase):
    pass

class EstadoReservaUpdate(EstadoReservaBase):
    pass

class EstadoReservaResponse(EstadoReservaBase):
    id_estado: int

    class Config:
        from_attributes = True
