from sqlalchemy.orm import Session
from db.models.models import TipoEvento
from schemas.tipo_evento import TipoEventoCreate, TipoEventoResponse

def get_evento(db: Session, id_evento: int):
    return db.query(TipoEvento).filter(TipoEvento.id_evento == id_evento).first()

def get_eventos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TipoEvento).offset(skip).limit(limit).all()
