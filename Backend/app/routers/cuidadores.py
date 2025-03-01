from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.client import get_db
from schemas.cuidador import CuidadorCreate, CuidadorUpdate, CuidadorResponse
from db.cruds.cuidador import get_cuidador, get_cuidadores, create_cuidador, update_cuidador, delete_cuidador

router = APIRouter(prefix="/cuidadores", tags=["Cuidadores"])

@router.get("/", response_model=list[CuidadorResponse])
def obtener_cuidadores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_cuidadores(db, skip, limit)

@router.get("/{id_cuidador}", response_model=CuidadorResponse)
def obtener_cuidador(id_cuidador: int, db: Session = Depends(get_db)):
    cuidador = get_cuidador(db, id_cuidador)
    if not cuidador:
        raise HTTPException(status_code=404, detail="Cuidador no encontrado")
    return cuidador

@router.post("/", response_model=CuidadorResponse)
def crear_cuidador(cuidador: CuidadorCreate, db: Session = Depends(get_db)):
    return create_cuidador(db, cuidador)

@router.put("/{id_cuidador}", response_model=CuidadorResponse)
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
