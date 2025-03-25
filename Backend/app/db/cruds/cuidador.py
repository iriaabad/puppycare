from sqlalchemy.orm import Session, joinedload
from db.models.models import Cuidador, User, Reserva
from schemas.cuidador import CuidadorCreate, CuidadorUpdate
from typing import Optional, List
from datetime import datetime


def get_cuidador(db: Session, id_cuidador: int):
    return db.query(Cuidador).filter(Cuidador.id_cuidador == id_cuidador).first()


def parse_fecha(fecha_str: Optional[str]) -> Optional[datetime]:
    if fecha_str:
        try:
            return datetime.strptime(fecha_str, "%Y-%m-%d")
        except ValueError:
            return None
    return None

def get_cuidadores_disponibles(db: Session, fecha_inicio: Optional[str], fecha_fin: Optional[str],
                                cantidad_mascotas: Optional[int]) -> List:
                                
    # obtenemos TODOS los cuidadores
    cuidadores = db.query(Cuidador).all()
    cuidadores_disponibles = []

    fecha_inicio_dt = parse_fecha(fecha_inicio)
    fecha_fin_dt = parse_fecha(fecha_fin)
    cantidad_nueva = int(cantidad_mascotas) if cantidad_mascotas is not None else 0

    for cuidador in cuidadores:
        # En base a fechas y cantidad, comprobamos las reservas existentes
        if fecha_inicio_dt and fecha_fin_dt and cantidad_nueva:
            reservas = db.query(Reserva).filter(
                Reserva.cuidador_id_cuidador == cuidador.id_cuidador,
                Reserva.fecha_fin >= fecha_inicio_dt,
                Reserva.fecha_inicio <= fecha_fin_dt
            ).all()

            mascotas_reservadas = sum(reserva.cantidad_mascotas for reserva in reservas)
            # Solo incluir si la suma no supera la capacidad del cuidador
            if mascotas_reservadas + cantidad_nueva <= cuidador.capacidad_mascota:
                cuidadores_disponibles.append(cuidador)
        else:
            # Si no se especifican fechas o cantidad, devolvemos todos los cuidadores
            cuidadores_disponibles.append(cuidador)

    return cuidadores_disponibles



def get_cuidadores(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Cuidador).offset(skip).limit(limit).all()

def create_cuidador(db: Session, cuidador: CuidadorCreate):
    db_cuidador = Cuidador(**cuidador.model_dump())
    db.add(db_cuidador)
    db.commit()
    db.refresh(db_cuidador)
    return db_cuidador

def update_cuidador(db: Session, id_cuidador: int, cuidador: CuidadorUpdate):
    db_cuidador = db.query(Cuidador).filter(Cuidador.id_cuidador == id_cuidador).first()
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
