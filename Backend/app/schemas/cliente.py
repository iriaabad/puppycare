from pydantic import BaseModel
from typing import Optional

# Base model para el Cliente
class ClienteBase(BaseModel):
    usuario_id_usuario: int

# Modelo para crear un Cliente
class ClienteCreate(ClienteBase):
    pass

# Modelo para la respuesta de un Cliente
class ClienteResponse(ClienteBase):
    id_cliente: int

    class Config:
        from_attributes = True

# Modelo para actualizar un Cliente
class ClienteUpdate(BaseModel):
    usuario_id_usuario: Optional[int]  # Opcional, ya que no necesariamente hay que actualizarlo

    class Config:
        from_attributes = True
