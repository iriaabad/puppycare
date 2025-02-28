from pydantic import BaseModel

class TamanoBase(BaseModel):
    descripcion: str

class TamanoCreate(TamanoBase):
    pass

class TamanoUpdate(TamanoBase):
    pass

class TamanoResponse(TamanoBase):
    id_tamano: int

    class Config:
        orm_mode = True
