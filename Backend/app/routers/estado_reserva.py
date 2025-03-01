from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from db.client import get_db
from db.models.models import EstadoReserva
from schemas.estado_reserva import EstadoReserva, EstadoReservaCreate, EstadoReservaUpdate
from db.cruds.estado_reserva import get_estado, get_estados, create_estado, update_estado, delete_estado

router = APIRouter(prefix="/estados_reserva", tags=["Estados Reserva"])

@router.post("/", response_model=EstadoReserva)
def create_estado_endpoint(estado: EstadoReservaCreate, db: Session = Depends(get_db)):
    return create_estado(db, estado)

@router.get("/", response_model=List[EstadoReserva])
def read_estados_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_estados(db, skip, limit)

@router.get("/{id_estado}", response_model=EstadoReserva)
def read_estado_endpoint(id_estado: int, db: Session = Depends(get_db)):
    db_estado = get_estado(db, id_estado)
    if not db_estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return db_estado


