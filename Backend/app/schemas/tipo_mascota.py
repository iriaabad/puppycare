from pydantic import BaseModel

class TipoMascotaBase(BaseModel):
    tipo: str

class TipoMascotaCreate(TipoMascotaBase):
    pass

class TipoMascotaUpdate(TipoMascotaBase):
    pass

class TipoMascotaResponse(TipoMascotaBase):
    id_tipo_mascota: int

    class Config:
        orm_mode = True
