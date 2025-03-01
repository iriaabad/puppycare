from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    nombre: Optional [str] = None
    apellido1: Optional [str] = None
    apellido2: Optional[str] = None
    email: EmailStr
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    calle: Optional[str] = None
    numero: Optional[str] = None
    piso: Optional[str] = None
    codigopostal: Optional[int] = None
    ciudad: Optional[str] = None

# Este es el esquema para leer un usuario, excluyendo la contraseña
class User(UserBase):
    id_usuario: int  

    class Config:
        from_attributes = True


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
    email: Optional[EmailStr] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    calle: Optional[str] = None
    numero: Optional[str] = None
    piso: Optional[str] = None
    codigopostal: Optional[int] = None
    ciudad: Optional[str] = None

    class Config:
        from_attributes = True

# Esquema para actualizar un usuario
class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido1: Optional[str] = None
    apellido2: Optional[str] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    calle: Optional[str] = None
    numero: Optional[int] = None
    piso: Optional[str] = None
    codigopostal: Optional[str] = None
    ciudad: Optional[str] = None

    class Config:
        from_attributes = True
