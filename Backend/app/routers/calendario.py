from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.client import get_db
from db.models.models import EventoCalendario, Calendario, Cuidador, TipoEvento
from schemas.calendario import CalendarioCreate, CalendarioUpdate, CalendarioResponse
from db.cruds.calendario import get_calendario, get_calendarios, create_calendario, update_calendario

router = APIRouter(prefix="/calendario", tags=["Calendario"])
@router.post("/", response_model=CalendarioResponse)
def create_calendario_endpoint(calendario: CalendarioCreate, db: Session = Depends(get_db)):
    return create_calendario(db, calendario)

@router.get("/", response_model=List[CalendarioResponse])
def read_calendarios_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_calendarios(db, skip, limit)

@router.get("/{id_calendario}", response_model=CalendarioResponse)
def read_calendario_endpoint(id_calendario: int, db: Session = Depends(get_db)):
    db_calendario = get_calendario(db, id_calendario)
    if not db_calendario:
        raise HTTPException(status_code=404, detail="Calendario no encontrado")
    return db_calendario

@router.get("/eventos_por_cuidador/{id_cuidador}")
def get_eventos_por_cuidador(id_cuidador: int, db: Session = Depends(get_db)):
    resultados = (
        db.query(EventoCalendario, TipoEvento)
        .join(Calendario, EventoCalendario.calendario_id == Calendario.id_calendario)
        .join(Cuidador, Calendario.cuidador_id_cuidador == Cuidador.id_cuidador)
        .join(TipoEvento, EventoCalendario.evento_id_evento == TipoEvento.id_evento)
        .filter(Cuidador.id_cuidador == id_cuidador)
        .all()
    )
    return [
        {
            "id_evento": evento.id_evento,
            "reserva_id_reserva": evento.reserva_id_reserva,
            "fecha_inicio": evento.fecha_inicio,
            "fecha_fin": evento.fecha_fin,
            "evento_id_evento": evento.evento_id_evento,
            "evento": TipoEvento.descripcion
        }
        for evento, tipo_evento in resultados
    ]


@router.put("/{id_calendario}", response_model=CalendarioResponse)
def update_calendario_endpoint(id_calendario: int, calendario_update: CalendarioUpdate, db: Session = Depends(get_db)):
    db_calendario = update_calendario(db, id_calendario, calendario_update)
    if not db_calendario:
        raise HTTPException(status_code=404, detail="Calendario no encontrado")
    return db_calendario

