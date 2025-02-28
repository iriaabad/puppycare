from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.tamano import TamanoCreate, TamanoResponse, TamanoUpdate
from db.cruds.tamano import get_tamano, get_tamanos, create_tamano
from db.client import get_db


router = APIRouter(prefix="/tamanos", tags=["Tamaños"])

@router.get("/", response_model=list[TamanoResponse])
def read_tamanos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_tamanos(db, skip, limit)

@router.get("/{id_tamano}", response_model=TamanoResponse)
def read_tamano(id_tamano: int, db: Session = Depends(get_db)):
    tamano = get_tamano(db, id_tamano)
    if not tamano:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tamaño no encontrado")
    return tamano



