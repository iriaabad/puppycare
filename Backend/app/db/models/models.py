from sqlalchemy import Boolean, Column, Integer, String, DECIMAL, ForeignKey, Float, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

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
    reservas = relationship("Reserva", back_populates="cliente")



class Cuidador(Base):
    __tablename__ = "cuidador"

    id_cuidador = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    tarifa_dia = Column(DECIMAL(10, 2), nullable=True)
    capacidad_mascota = Column(Integer, nullable=True)
    descripcion = Column(String(255), nullable=True)
    disponibilidad_activa = Column(Boolean, default=True)

    # Relación con usuario
    usuario = relationship("User", back_populates="cuidador")
    reservas = relationship("Reserva", back_populates="cuidador")
    calendario = relationship("Calendario", back_populates="cuidador", uselist=False)

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



class Reserva(Base):
    __tablename__ = "reserva"
    
    id_reserva = Column(Integer, primary_key=True, index=True)
    cliente_id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    cuidador_id_cuidador = Column(Integer, ForeignKey("cuidador.id_cuidador"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    cantidad_mascotas = Column(Integer, nullable=False)
    precio_total = Column(Float, nullable=False)
    estado_reserva_id_estado = Column(Integer, ForeignKey("estado_reserva.id_estado"), nullable=False)

    # Relación con otros modelos
    cliente = relationship("Cliente", back_populates="reservas")
    cuidador = relationship("Cuidador", back_populates="reservas")
    estado_reserva = relationship("EstadoReserva", back_populates="reservas")
    eventos = relationship("EventoCalendario", back_populates="reserva")
    
# Definimos la clase EstadoReserva
class EstadoReserva(Base):
    __tablename__ = "estado_reserva"

    id_estado = Column(Integer, primary_key=True, autoincrement=True, index=True)
    descripcion = Column(String(50), nullable=False)
    reservas = relationship("Reserva", back_populates="estado_reserva")


#definimos la clase Calendario
class Calendario(Base):
    __tablename__ = "calendario"

    id_calendario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cuidador_id_cuidador = Column(Integer, ForeignKey("cuidador.id_cuidador"), nullable=False)
   
    # Relaciones
    cuidador = relationship("Cuidador", back_populates="calendario")
    eventos_calendario = relationship("EventoCalendario", back_populates="calendario")


class EventoCalendario(Base):
    __tablename__ = "evento_calendario"

    id_evento = Column(Integer, primary_key=True, index=True)
    calendario_id = Column(Integer, ForeignKey("calendario.id_calendario"), nullable=False)
    reserva_id_reserva = Column(Integer, ForeignKey("reserva.id_reserva"), nullable=True)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    evento_id_evento = Column(Integer, ForeignKey("tipo_evento.id_tipo_evento"), nullable=False)  

    # Relaciones
    calendario = relationship("Calendario", back_populates="eventos_calendario")
    reserva = relationship("Reserva", back_populates="eventos") 
    tipo_evento = relationship("TipoEvento", back_populates="eventos_calendario")


 
 # Definimos la clase Evento
class TipoEvento(Base):
    __tablename__ = "tipo_evento"

    id_tipo_evento = Column(Integer, primary_key=True, autoincrement=True, index=True)
    descripcion = Column(String(50), nullable=False)
     
    # Relaciones
    eventos_calendario = relationship("EventoCalendario", back_populates="tipo_evento")  # Relación con EventoCalendario