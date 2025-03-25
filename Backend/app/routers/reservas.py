from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from db.client import get_db
from db.models.models import Reserva, Calendario, EventoCalendario, Cuidador, EstadoReserva, User
from schemas.reserva import ReservaCreate, ReservaResponse, ReservaUpdate, ReservaBase
from db.cruds.reserva import get_reserva, get_reservas, create_reserva, update_reserva, delete_reserva, get_reservas_cliente

router = APIRouter(prefix="/reservas", tags=["Reservas"])

@router.post("/", response_model=ReservaResponse)
def create_reserva_endpoint(reserva: ReservaCreate, db: Session = Depends(get_db)):

  
    # Crear la reserva
    nueva_reserva = Reserva(**reserva.model_dump())
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)

    # Buscar el calendario del cuidador
    calendario = db.query(Calendario).filter(Calendario.cuidador_id_cuidador == nueva_reserva.cuidador_id_cuidador).first()

    if not calendario:
        raise HTTPException(status_code=404, detail="Calendario del cuidador no encontrado")

    # Crear un nuevo evento en el calendario del cuidador
    nuevo_evento = EventoCalendario(
        calendario_id=calendario.id_calendario,
        reserva_id_reserva=nueva_reserva.id_reserva,
        fecha_inicio=nueva_reserva.fecha_inicio,
        fecha_fin=nueva_reserva.fecha_fin,
        evento_id_evento=1  # Tipo: Reserva
    )
    db.add(nuevo_evento)
    db.commit()

    return nueva_reserva

@router.get("/", response_model=List[ReservaResponse])
def read_reservas_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_reservas(db, skip, limit)

@router.get("/reserva/{id_reserva}", response_model=ReservaResponse)
def read_reserva_endpoint(id_reserva: int, db: Session = Depends(get_db)):
    db_reserva = get_reserva(db, id_reserva)
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return db_reserva


@router.get("/cliente/{id_cliente}", response_model=List[ReservaResponse])
def read_reservas_cliente(id_cliente: int, db: Session = Depends(get_db)):
    db_reservas = get_reservas_cliente(db, id_cliente=id_cliente, skip=0, limit=100) 
    if not db_reservas:
        raise HTTPException(status_code=404, detail="No se encontraron reservas para este cliente")
    return [ReservaResponse.model_validate(reserva) for reserva in db_reservas]



@router.put("/reserva/{id_reserva}", response_model=ReservaResponse)
def update_reserva_endpoint(id_reserva: int, reserva_update: ReservaUpdate, db: Session = Depends(get_db)):
    db_reserva = update_reserva(db, id_reserva, reserva_update)
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return db_reserva

@router.delete("/{id_reserva}", response_model=ReservaResponse)
def delete_reserva_endpoint(id_reserva: int, db: Session = Depends(get_db)):
    db_reserva = delete_reserva(db, id_reserva)
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return db_reserva
