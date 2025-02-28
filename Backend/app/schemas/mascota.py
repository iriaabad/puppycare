from pydantic import BaseModel
from typing import Optional
from schemas.tipo_mascota import TipoMascotaResponse
from schemas.tamano import TamanoResponse

class MascotaBase(BaseModel):
    nombre: str
    tipo_mascota_id_tipo_mascota: int
    edad: Optional[int] = None
    tamano_id_tamano: Optional[int] = None
    necesidades_especiales: Optional[str] = None
    cliente_id_cliente: Optional[int] = None

class MascotaCreate(MascotaBase):
    pass

class MascotaUpdate(MascotaBase):
    pass

class MascotaResponse(MascotaBase):
    id_mascota: int
    tipo_mascota: Optional[TipoMascotaResponse]  # Objeto anidado con la información del tipo
    tamano: Optional[TamanoResponse]         

    class Config:
        orm_mode = True
