from sqlalchemy.orm import Session
from db.models.models import Calendario
from schemas.calendario import CalendarioCreate, CalendarioUpdate

def get_calendario(db: Session, id_calendario: int):
    return db.query(Calendario).filter(Calendario.id_calendario == id_calendario).first()

def get_calendarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Calendario).offset(skip).limit(limit).all()

def create_calendario(db: Session, calendario: CalendarioCreate):
    db_calendario = Calendario(**calendario.model_dump())
    db.add(db_calendario)
    db.commit()
    db.refresh(db_calendario)
    return db_calendario

def update_calendario(db: Session, id_calendario: int, calendario_update: CalendarioUpdate):
    db_calendario = db.query(Calendario).filter(Calendario.id_calendario == id_calendario).first()
    if not db_calendario:
        return None

    for key, value in calendario_update.model_dump(exclude_unset=True).items():
        setattr(db_calendario, key, value)

    db.commit()
    db.refresh(db_calendario)
    return db_calendario
