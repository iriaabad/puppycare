from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from fastapi import HTTPException
from db.models.models import Cuidador
from db.models.models import Reserva
from schemas.reserva import ReservaCreate, ReservaUpdate

def get_reserva(db: Session, id_reserva: int):
    return db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()

def get_reservas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Reserva).offset(skip).limit(limit).all()

def create_reserva(db: Session, reserva: ReservaCreate):
    # Obtener la capacidad del cuidador
    cuidador = db.query(Cuidador).filter(Cuidador.id_cuidador == reserva.cuidador_id_cuidador).first()
    if not cuidador:
        raise HTTPException(status_code=404, detail="Cuidador no encontrado")

    # Calcular cuántas mascotas ya están reservadas en ese rango de fechas
    mascotas_reservadas = db.query(func.sum(Reserva.cantidad_mascotas)).filter(
        Reserva.cuidador_id_cuidador == reserva.cuidador_id_cuidador,
        and_(
            Reserva.fecha_inicio < reserva.fecha_fin,
            Reserva.fecha_fin > reserva.fecha_inicio
        )
    ).scalar() or 0  # Si no hay reservas, devolver 0

    # Verificar si hay capacidad suficiente
    if mascotas_reservadas + reserva.cantidad_mascotas > cuidador.capacidad_mascota:
        raise HTTPException(status_code=400, detail="El cuidador no tiene capacidad suficiente para esta reserva")

    # Crear la reserva si hay espacio disponible
    db_reserva = Reserva(**reserva.model_dump())
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva


def update_reserva(db: Session, id_reserva: int, reserva_update: ReservaUpdate):
    db_reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
    if not db_reserva:
        return None

    # Obtener la capacidad del cuidador
    cuidador = db.query(Cuidador).filter(Cuidador.id_cuidador == db_reserva.cuidador_id_cuidador).first()
    if not cuidador:
        raise HTTPException(status_code=404, detail="Cuidador no encontrado")

    # Obtener la nueva cantidad de mascotas y fechas de la actualización
    nueva_cantidad_mascotas = reserva_update.cantidad_mascotas or db_reserva.cantidad_mascotas
    nueva_fecha_inicio = reserva_update.fecha_inicio or db_reserva.fecha_inicio
    nueva_fecha_fin = reserva_update.fecha_fin or db_reserva.fecha_fin

    # Calcular cuántas mascotas ya están reservadas en ese rango (excluyendo la reserva actual)
    mascotas_reservadas = db.query(func.sum(Reserva.cantidad_mascotas)).filter(
        Reserva.cuidador_id_cuidador == db_reserva.cuidador_id_cuidador,
        and_(
            Reserva.fecha_inicio < nueva_fecha_fin,
            Reserva.fecha_fin > nueva_fecha_inicio
        ),
        Reserva.id_reserva != id_reserva  # Excluir la reserva actual
    ).scalar() or 0  # Si no hay reservas, devolver 0

    # Verificar si hay capacidad suficiente
    if mascotas_reservadas + nueva_cantidad_mascotas > cuidador.capacidad:
        raise HTTPException(status_code=400, detail=f"El cuidador no dispone de capacidad para las fechas marcadas ({nueva_fecha_inicio} - {nueva_fecha_fin}). "
                   f"Capacidad total: {cuidador.capacidad_mascota}, ya reservadas: {mascotas_reservadas}."
)

    # Aplicar la actualización
    for key, value in reserva_update.model_dump().items():
        if value is not None:  # Solo actualizar si el valor no es None
            setattr(db_reserva, key, value)

    db.commit()
    db.refresh(db_reserva)
    return db_reserva


def delete_reserva(db: Session, id_reserva: int):
    db_reserva = get_reserva(db, id_reserva)
    if not db_reserva:
        return None
    db.delete(db_reserva)
    db.commit()
    return db_reserva
