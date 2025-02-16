from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    nombre: Optional [str] = None
    apellido1: Optional [str] = None
    apellido2: Optional[str] = None
    email: str
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    calle: Optional[str] = None
    numero: Optional[str] = None
    piso: Optional[str] = None
    codigopostal: Optional[int] = None
    ciudad: Optional[str] = None

# Este es el esquema para leer un usuario, excluyendo la contraseña
class User(UserBase):
    id_usuario: int  # Asegúrate de que este campo coincide con el nombre de tu columna en la DB

    class Config:
        orm_mode = True  # Para poder trabajar con instancias ORM de SQLAlchemy


    # Esquema para crear un usuario (entrada de datos)
class UserCreate(BaseModel):
    nombre: Optional[str] = None
    apellido1: Optional[str] = None
    apellido2: Optional[str] = None
    email: EmailStr
    password: str 
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    calle: Optional[str] = None 
    numero: Optional[str]= None
    piso: Optional[str]= None
    codigopostal: Optional[int]= None
    ciudad: Optional[str]= None

# Esquema para la respuesta (salida de datos)
class UserResponse(BaseModel):
    id_usuario: int
    nombre: Optional[str] = None
    apellido1: Optional[str] = None
    apellido2: Optional[str] = None
    email: str
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    calle: Optional[str] = None
    numero: Optional[str] = None
    piso: Optional[str] = None
    codigopostal: Optional[int] = None
    ciudad: Optional[str] = None

    class Config:
        orm_mode = True
