from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.client import get_db
from typing import List, Optional
from db.models.models import Cuidador, Calendario
from schemas.cuidador import CuidadorCreate, CuidadorUpdate, CuidadorResponse
from db.cruds.cuidador import get_cuidador, get_cuidadores, create_cuidador, update_cuidador, delete_cuidador, get_cuidadores_disponibles

router = APIRouter(prefix="/cuidadores", tags=["Cuidadores"])

@router.get("/", response_model=list[CuidadorResponse])
def obtener_cuidadores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_cuidadores(db, skip, limit)

@router.get("/select/", response_model=List[CuidadorResponse])
def get_cuidadores(usuario_id_usuario: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Cuidador)
    if usuario_id_usuario is not None:
        query = query.filter(Cuidador.usuario_id_usuario == usuario_id_usuario)
    cuidadores = query.all()
    return cuidadores

    

@router.get("/obtener/disponibles/", response_model=List[CuidadorResponse])
def get_cuidadores_disponibles_endpoint(
    fecha_inicio: Optional[str] = Query(None, description="Fecha de inicio (opcional)"),
    fecha_fin: Optional[str] = Query(None, description="Fecha de fin (opcional)"),
    cantidad_mascotas: Optional[int] = Query(None, description="Cantidad de mascotas (opcional)"),
    db: Session = Depends(get_db)
):
    return get_cuidadores_disponibles(db, fecha_inicio, fecha_fin, cantidad_mascotas)


@router.get("/recibir/{id_cuidador}", response_model=CuidadorResponse)
def obtener_cuidador(id_cuidador: int, db: Session = Depends(get_db)):
    cuidador = get_cuidador(db, id_cuidador)
    if not cuidador:
        raise HTTPException(status_code=404, detail="Cuidador no encontrado")
    return cuidador

@router.get("/user/{id_user}", response_model=CuidadorResponse)
def obtener_cuidador(id_user: int, db: Session = Depends(get_db)):
    cuidador = get_cuidador(db, id_user)
    if not cuidador:
        raise HTTPException(status_code=404, detail="Cuidador no encontrado")
    return cuidador

@router.post("/", response_model=CuidadorResponse)
def crear_cuidador(cuidador: CuidadorCreate, db: Session = Depends(get_db)):
    nuevo_cuidador = create_cuidador(db, cuidador)

    # Crear una entrada en la tabla calendario para el nuevo cuidador
    nuevo_calendario = Calendario(cuidador_id_cuidador=nuevo_cuidador.id_cuidador)
    db.add(nuevo_calendario)
    db.commit()
    db.refresh(nuevo_calendario)

    return nuevo_cuidador
@router.put("/modificar/{id_cuidador}", response_model=CuidadorResponse)
def actualizar_cuidador(id_cuidador: int, cuidador: CuidadorUpdate, db: Session = Depends(get_db)):
    cuidador_actualizado = update_cuidador(db, id_cuidador, cuidador)
    if not cuidador_actualizado:
        raise HTTPException(status_code=404, detail="Cuidador no encontrado")
    return cuidador_actualizado

@router.delete("/{id_cuidador}")
def eliminar_cuidador(id_cuidador: int, db: Session = Depends(get_db)):
    cuidador_eliminado = delete_cuidador(db, id_cuidador)
    if not cuidador_eliminado:
        raise HTTPException(status_code=404, detail="Cuidador no encontrado")
    return {"message": "Cuidador eliminado correctamente"}
