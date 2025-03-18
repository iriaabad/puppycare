from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from db.client import get_db
from db.models.models import TipoEvento
from schemas.tipo_evento import TipoEventoCreate, TipoEventoResponse
from db.cruds.tipo_evento import get_evento, get_eventos

router = APIRouter(prefix="/tipo_evento", tags=["TipoEventos"])

@router.get("/", response_model=List[TipoEventoResponse])
def read_eventos_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_eventos(db, skip, limit)

@router.get("/{id_evento}", response_model=TipoEventoResponse)
def read_evento_endpoint(id_evento: int, db: Session = Depends(get_db)):
    db_evento = get_evento(db, id_evento)
    if not db_evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return db_evento

