from sqlalchemy.orm import Session
from db.models.models import Tamano
from schemas.tamano import TamanoCreate

def get_tamano(db: Session, id_tamano: int):
    return db.query(Tamano).filter(Tamano.id_tamano == id_tamano).first()

def get_tamanos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tamano).offset(skip).limit(limit).all()

def create_tamano(db: Session, tamano: TamanoCreate):
    db_tamano = Tamano(**tamano.model_dump())
    db.add(db_tamano)
    db.commit()
    db.refresh(db_tamano)
    return db_tamano
