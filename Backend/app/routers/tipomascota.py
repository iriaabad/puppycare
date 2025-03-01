# routes/tipomascota.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.tipo_mascota import TipoMascotaCreate, TipoMascotaResponse, TipoMascotaUpdate
from db.cruds.tipo_mascota import get_tipo_mascota, get_tipos_mascota
from db.client import get_db


router = APIRouter(prefix="/tipos-mascota", tags=["Tipo Mascota"])

@router.get("/", response_model=list[TipoMascotaResponse])
def read_tipos_mascota(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_tipos_mascota(db, skip, limit)

@router.get("/{id_tipo_mascota}", response_model=TipoMascotaResponse)
def read_tipo_mascota(id_tipo_mascota: int, db: Session = Depends(get_db)):
    tipo = get_tipo_mascota(db, id_tipo_mascota)
    if not tipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de mascota no encontrado")
    return tipo


