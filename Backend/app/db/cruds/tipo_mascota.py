from sqlalchemy.orm import Session
from db.models.models import TipoMascota
from schemas.tipo_mascota import TipoMascotaCreate, TipoMascotaUpdate

#obtener tipo de mascota por id
def get_tipo_mascota(db: Session, id_tipo_mascota: int):
    return db.query(TipoMascota).filter(TipoMascota.id_tipo_mascota == id_tipo_mascota).first()

#obtener todos los tipos de mascota
def get_tipos_mascota(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TipoMascota).offset(skip).limit(limit).all()

