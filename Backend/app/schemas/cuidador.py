from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional
from typing_extensions import Annotated


class CuidadorBase(BaseModel):
    usuario_id_usuario: int  
    tarifa_dia: Optional[Decimal] = Field(None, max_digits=4, decimal_places=2)
    capacidad_mascota: Optional[int]
    descripcion: Optional[str]
    disponibilidad_activa: Optional[bool]

class CuidadorCreate(CuidadorBase):
    usuario_id_usuario: int  # Requerido para la creación
    tarifa_dia: Optional[Decimal] = Field(None, max_digits=4, decimal_places=2)
    capacidad_mascota: Optional[int]
    descripcion: Optional[str]
    disponibilidad_activa: Optional[bool]

class CuidadorUpdate(CuidadorBase):
    pass  # Permite actualizar solo los campos enviados

class CuidadorResponse(CuidadorBase):
    id_cuidador: int
    usuario_id_usuario: int

    class Config:
        from_attributes = True
