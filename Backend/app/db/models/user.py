from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from db.client import Base



Base = declarative_base()
#definimos clase de usuario (el modelo de usuario)
class User(Base):
    __tablename__ = "usuario"  

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(40), nullable=True)
    apellido1 = Column(String(40), nullable=True)
    apellido2 = Column(String(40), nullable=True)
    email = Column(String(100), unique=True, nullable=True, index=True)
    hashed_password = Column(String(255), nullable=True)
    latitud = Column(DECIMAL(9, 6), nullable=True)
    longitud = Column(DECIMAL(9, 6), nullable=True)
    calle = Column(String(40), nullable=True)
    numero = Column(String(40), nullable=True)
    piso = Column(String(40), nullable=True)
    codigopostal = Column(Integer, nullable=True)
    ciudad = Column(String(50), nullable=True)


