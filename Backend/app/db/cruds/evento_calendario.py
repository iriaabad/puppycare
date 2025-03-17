from sqlalchemy.orm import Session
from typing import List, Optional
from db.models.models import EventoCalendario
from schemas.evento_calendario import EventoCalendarioCreate, EventoCalendarioUpdate

def create_evento_calendario(db: Session, evento: EventoCalendarioCreate) -> EventoCalendario:
    db_evento = EventoCalendario(**evento.dict())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

def get_evento_calendario(db: Session, evento_id: int) -> Optional[EventoCalendario]:
    return db.query(EventoCalendario).filter(EventoCalendario.id_evento == evento_id).first()

def get_eventos_by_calendario(db: Session, calendario_id: int) -> List[EventoCalendario]:
    return db.query(EventoCalendario).filter(EventoCalendario.calendario_id == calendario_id).all()

def update_evento_calendario(db: Session, evento_id: int, evento_update: EventoCalendarioUpdate) -> Optional[EventoCalendario]:
    db_evento = db.query(EventoCalendario).filter(EventoCalendario.id_evento == evento_id).first()
    if not db_evento:
        return None
    for key, value in evento_update.dict(exclude_unset=True).items():
        setattr(db_evento, key, value)
    db.commit()
    db.refresh(db_evento)
    return db_evento

def delete_evento_calendario(db: Session, evento_id: int) -> bool:
    db_evento = db.query(EventoCalendario).filter(EventoCalendario.id_evento == evento_id).first()
    if not db_evento:
        return False
    db.delete(db_evento)
    db.commit()
    return True