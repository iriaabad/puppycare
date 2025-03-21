from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional
from typing_extensions import Annotated
from schemas.user import UserResponse


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

class CuidadorUpdate(BaseModel):
    tarifa_dia: Optional[float] = None
    capacidad_mascota: Optional[int] = None
    descripcion: Optional[str] = None
    disponibilidad_activa: Optional[bool] = None


class CuidadorResponse(CuidadorBase):
    id_cuidador: int
    usuario_id_usuario: int
    usuario: UserResponse

    class Config:
        from_attributes = True
