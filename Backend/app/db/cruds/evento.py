from sqlalchemy.orm import Session
from db.models.models import Evento
from schemas.evento import EventoCreate, EventoResponse

def get_evento(db: Session, id_evento: int):
    return db.query(Evento).filter(Evento.id_evento == id_evento).first()

def get_eventos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Evento).offset(skip).limit(limit).all()
