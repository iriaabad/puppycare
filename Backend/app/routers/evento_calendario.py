from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.client import get_db
from schemas.evento_calendario import EventoCalendarioCreate, EventoCalendarioUpdate, EventoCalendarioResponse
from db.cruds.evento_calendario import (
    create_evento_calendario,
    get_evento_calendario,
    get_eventos_by_calendario,
    update_evento_calendario,
    delete_evento_calendario
)

router = APIRouter(prefix="/eventos-calendario", tags=["Eventos Calendario"])

#Crear un evento en el calendario
@router.post("/", response_model=EventoCalendarioResponse)
def create_evento(evento: EventoCalendarioCreate, db: Session = Depends(get_db)):
    return create_evento_calendario(db, evento)

#Obtener un evento por ID
@router.get("/{evento_id}", response_model=EventoCalendarioResponse)
def get_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = get_evento_calendario(db, evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento

#Obtener todos los eventos de un calendario específico
@router.get("/calendario/{calendario_id}", response_model=list[EventoCalendarioResponse])
def get_eventos_de_calendario(calendario_id: int, db: Session = Depends(get_db)):
    return get_eventos_by_calendario(db, calendario_id)

# Actualizar un evento por ID
@router.put("/{evento_id}", response_model=EventoCalendarioResponse)
def update_evento(evento_id: int, evento_update: EventoCalendarioUpdate, db: Session = Depends(get_db)):
    evento_actualizado = update_evento_calendario(db, evento_id, evento_update)
    if not evento_actualizado:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento_actualizado

# Eliminar un evento por ID
@router.delete("/{evento_id}")
def delete_evento(evento_id: int, db: Session = Depends(get_db)):
    if not delete_evento_calendario(db, evento_id):
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return {"message": "Evento eliminado correctamente"}
