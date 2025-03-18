from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from db.client import get_db
from typing import List
from schemas.evento_calendario import EventoCalendarioCreate, EventoCalendarioUpdate, EventoCalendarioResponse
from db.cruds.evento_calendario import (
    create_evento_calendario,
    get_evento_calendario,
    get_eventos_by_calendario,
    update_evento_calendario,
    delete_evento_calendario
)
from db.models.models import EventoCalendario, Calendario, Cuidador, TipoEvento

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



@router.get("/eventos_por_cuidador/{id_cuidador}", response_model=List[dict])
def get_eventos_por_cuidador(id_cuidador: int, db: Session = Depends(get_db)):
    resultados = (
        db.query(EventoCalendario, TipoEvento)
        .join(Calendario, EventoCalendario.calendario_id == Calendario.id_calendario)
        .join(Cuidador, Calendario.cuidador_id_cuidador == Cuidador.id_cuidador)
        .options(joinedload(EventoCalendario.tipo_evento))
        .join(TipoEvento, EventoCalendario.evento_id_evento == TipoEvento.id_tipo_evento)
        .filter(Cuidador.id_cuidador == id_cuidador)
        .all()
    )
    
    return [
        {
            "id_evento": evento.id_evento,
            "calendario_id": evento.calendario_id,
            "reserva_id_reserva": evento.reserva_id_reserva,
            "fecha_inicio": evento.fecha_inicio,
            "fecha_fin": evento.fecha_fin,
            # Generamos el título concatenando el tipo de evento y las fechas.
            "title": f"{tipo_evento.descripcion} {evento.fecha_inicio} - {evento.fecha_fin}"
        }
        for evento, tipo_evento in resultados
    ]

#@router.get("/eventos_por_cuidador/{id_cuidador}", response_model=List[EventoCalendarioResponse])
#def get_eventos_por_cuidador(id_cuidador: int, db: Session = Depends(get_db)):
    resultados = (
        db.query(EventoCalendario)
        .join(Calendario, EventoCalendario.calendario_id == Calendario.id_calendario)
        .join(Cuidador, Calendario.cuidador_id_cuidador == Cuidador.id_cuidador)
        .options(joinedload(EventoCalendario.tipo_evento))  # Carga la relación
        .filter(Cuidador.id_cuidador == id_cuidador)
        .all()
    )
    
    return resultados


#@router.get("/eventos_por_cuidador/{id_cuidador}", response_model=List[EventoCalendarioResponse])
#def get_eventos_por_cuidador(id_cuidador: int, db: Session = Depends(get_db)):
    resultados = (
        db.query(EventoCalendario, TipoEvento)
        .join(Calendario, EventoCalendario.calendario_id == Calendario.id_calendario)
        .join(Cuidador, Calendario.cuidador_id_cuidador == Cuidador.id_cuidador)
        .join(TipoEvento, EventoCalendario.evento_id_evento == TipoEvento.id_tipo_evento)
        .filter(Cuidador.id_cuidador == id_cuidador)
        .all()
    )

    eventos = []
    for evento, tipo_evento in resultados:
        # Asignamos el objeto TipoEvento al atributo tipo_evento del evento
        evento.id_evento = tipo_evento
        eventos.append(evento)
    return eventos

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
