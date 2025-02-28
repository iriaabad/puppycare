from sqlalchemy import Boolean, Column, Integer, String, DECIMAL, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from schemas import cuidador, mascota

Base = declarative_base()

# Definimos la clase Usuario (User)
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

    # Relación con Cliente
    cliente = relationship("Cliente", back_populates="usuario", uselist=False)
    # Relación con usuario
    cuidador = relationship("Cuidador", back_populates="usuario")

# Definimos la clase Cliente
class Cliente(Base):
    __tablename__ = "cliente"
    
    id_cliente = Column(Integer, primary_key=True, index=True)
    usuario_id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)

    # Relación con User
    usuario = relationship("User", back_populates="cliente")
    mascotas = relationship("Mascota", back_populates="cliente")



class Cuidador(Base):
    __tablename__ = "cuidador"

    id_mascota = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    tarifa_dia = Column(DECIMAL(10, 2), nullable=True)
    capacidad_mascota = Column(Integer, nullable=True)
    descripcion = Column(String(255), nullable=True)
    disponibilidad_activa = Column(Boolean, default=True)

    # Relación con usuario
    usuario = relationship("User", back_populates="cuidador")


# Definimos la clase TipoMascota
class TipoMascota(Base):
    __tablename__ = "tipo_mascota"

    id_tipo_mascota = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tipo = Column(String(50), nullable=False)
    mascotas = relationship("Mascota", back_populates="tipo_mascota")



# Definimos la clase Tamano
class Tamano(Base):
    __tablename__ = "tamano"

    id_tamano = Column(Integer, primary_key=True, autoincrement=True, index=True)
    descripcion = Column(String(50), nullable=False)
    mascotas = relationship("Mascota", back_populates="tamano")

#Definimos la clase mascota
class Mascota(Base):
    __tablename__ = "mascota"

    id_mascota = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(100), nullable=False)
    tipo_mascota_id_tipo_mascota = Column(Integer, ForeignKey("tipo_mascota.id_tipo_mascota"), nullable=False)
    edad = Column(Integer, nullable=True)
    tamano_id_tamano = Column(Integer, ForeignKey("tamano.id_tamano"), nullable=True)
    necesidades_especiales = Column(String(255), nullable=True)
    cliente_id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=True)

    # Relaciones (suponiendo que existen los modelos TipoMascota, Tamano y Cliente)
    tipo_mascota = relationship("TipoMascota", back_populates="mascotas")
    tamano = relationship("Tamano", back_populates="mascotas")
    cliente = relationship("Cliente", back_populates="mascotas")

# Definimos la clase Reserva
class Reserva(Base):
    __tablename__ = "reservas"
    id_reserva = Column(Integer, primary_key=True, index=True)
    cliente_id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    cuidador_id_cuidador = Column(Integer, ForeignKey("cuidadores.id_cuidador"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    cantidad_mascotas = Column(Integer, nullable=False)
    precio_total = Column(Float, nullable=False)
    estado_reserva_id_estado = Column(Integer, ForeignKey("estados_reserva.id_estado"), nullable=False)