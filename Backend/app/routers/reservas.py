from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from db.client import get_db
from db.models.models import Reserva
from schemas.reserva import Reserva, ReservaCreate, ReservaUpdate
from db.cruds.reserva import get_reserva, get_reservas, create_reserva, update_reserva, delete_reserva

router = APIRouter(prefix="/reservas", tags=["Reservas"])

@router.post("/", response_model=Reserva)
def create_reserva_endpoint(reserva: ReservaCreate, db: Session = Depends(get_db)):
    return create_reserva(db, reserva)

@router.get("/", response_model=List[Reserva])
def read_reservas_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_reservas(db, skip, limit)

@router.get("/{id_reserva}", response_model=Reserva)
def read_reserva_endpoint(id_reserva: int, db: Session = Depends(get_db)):
    db_reserva = get_reserva(db, id_reserva)
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return db_reserva

@router.put("/{id_reserva}", response_model=Reserva)
def update_reserva_endpoint(id_reserva: int, reserva_update: ReservaUpdate, db: Session = Depends(get_db)):
    db_reserva = update_reserva(db, id_reserva, reserva_update)
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return db_reserva

@router.delete("/{id_reserva}", response_model=Reserva)
def delete_reserva_endpoint(id_reserva: int, db: Session = Depends(get_db)):
    db_reserva = delete_reserva(db, id_reserva)
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return db_reserva
