from pydantic import BaseModel

class ClienteBase(BaseModel):
    usuario_id_usuario: int

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id_cliente: int

    class Config:
        from_attributes = True
