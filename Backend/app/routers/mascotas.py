from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.models.models import Mascota
from schemas.mascota import MascotaCreate, MascotaUpdate, MascotaResponse
from db.cruds.mascota import get_mascota, get_mascotas, create_mascota, update_mascota, delete_mascota
from db.client import get_db

router = APIRouter(prefix="/mascotas", tags=["Mascotas"])

@router.get("/", response_model=list[MascotaResponse])
def read_mascotas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_mascotas(db, skip, limit)

@router.get("/{id_mascota}", response_model=MascotaResponse,)
def read_mascota(id_mascota: int, db: Session = Depends(get_db)):
    mascota = get_mascota(db, id_mascota)
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota not found")
    return mascota

@router.get("/cliente/{id_cliente}", response_model=list[MascotaResponse])
def read_mascotas_cliente(id_cliente: int, db: Session = Depends(get_db)):
    db_mascotas = db.query(Mascota).filter(Mascota.cliente_id_cliente == id_cliente).all()
    
    if not db_mascotas:
        raise HTTPException(status_code=404, detail="No se encontraron mascotas para este cliente")
    
    return [MascotaResponse.model_validate(mascota) for mascota in db_mascotas]

@router.post("/", response_model=MascotaResponse)
def create_mascota_endpoint(mascota: MascotaCreate, db: Session = Depends(get_db)):
    return create_mascota(db, mascota)

@router.put("/{id_mascota}", response_model=MascotaResponse)
def update_mascota_endpoint(id_mascota: int, mascota: MascotaUpdate, db: Session = Depends(get_db)):
    updated = update_mascota(db, id_mascota, mascota)
    if not updated:
        raise HTTPException(status_code=404, detail="Mascota not found")
    return updated

@router.delete("/{id_mascota}")
def delete_mascota_endpoint(id_mascota: int, db: Session = Depends(get_db)):
    deleted = delete_mascota(db, id_mascota)
    if not deleted:
        raise HTTPException(status_code=404, detail="Mascota not found")
    return {"detail": "Mascota deleted"}
