from sqlalchemy.orm import Session
from db.models.models import Cuidador
from schemas.cuidador import CuidadorCreate, CuidadorUpdate

def get_cuidador(db: Session, id_cuidador: int):
    return db.query(Cuidador).filter(Cuidador.usuario_id_usuario == id_cuidador).first()

def get_cuidadores(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Cuidador).offset(skip).limit(limit).all()

def create_cuidador(db: Session, cuidador: CuidadorCreate):
    db_cuidador = Cuidador(**cuidador.model_dump())
    db.add(db_cuidador)
    db.commit()
    db.refresh(db_cuidador)
    return db_cuidador

def update_cuidador(db: Session, id_cuidador: int, cuidador: CuidadorUpdate):
    db_cuidador = db.query(Cuidador).filter(Cuidador.usuario_id_usuario == id_cuidador).first()
    if not db_cuidador:
        return None

    for key, value in cuidador.model_dump(exclude_unset=True).items():
        setattr(db_cuidador, key, value)

    db.commit()
    db.refresh(db_cuidador)
    return db_cuidador

def delete_cuidador(db: Session, id_cuidador: int):
    db_cuidador = db.query(Cuidador).filter(Cuidador.usuario_id_usuario == id_cuidador).first()
    if not db_cuidador:
        return None

    db.delete(db_cuidador)
    db.commit()
    return db_cuidador
