from sqlalchemy.orm import Session, joinedload
from db.models.models import Mascota
from schemas.mascota import MascotaCreate, MascotaUpdate

def get_mascota(db: Session, id_mascota: int):
    return db.query(Mascota)\
             .options(joinedload(Mascota.tipo_mascota), joinedload(Mascota.tamano))\
             .filter(Mascota.id_mascota == id_mascota)\
             .first()

def get_mascotas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Mascota)\
             .options(
                 joinedload(Mascota.tipo_mascota),  # Carga el objeto tipo_mascota relacionado
                 joinedload(Mascota.tamano)         # Carga el objeto tamano relacionado
             )\
             .offset(skip)\
             .limit(limit)\
             .all()

def create_mascota(db: Session, mascota: MascotaCreate):
    db_mascota = Mascota(**mascota.model_dump())
    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

def update_mascota(db: Session, id_mascota: int, mascota: MascotaUpdate):
    db_mascota = get_mascota(db, id_mascota)
    if not db_mascota:
        return None
    for key, value in mascota.dict(exclude_unset=True).items():
        setattr(db_mascota, key, value)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

def delete_mascota(db: Session, id_mascota: int):
    db_mascota = get_mascota(db, id_mascota)
    if not db_mascota:
        return None
    db.delete(db_mascota)
    db.commit()
    return db_mascota
