from sqlalchemy.orm import Session
from db.models.models import EstadoReserva
from schemas.estado_reserva import EstadoReservaCreate, EstadoReservaUpdate

def get_estado(db: Session, id_estado: int):
    return db.query(EstadoReserva).filter(EstadoReserva.id_estado == id_estado).first()

def get_estados(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EstadoReserva).offset(skip).limit(limit).all()


