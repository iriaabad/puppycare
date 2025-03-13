from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.client import get_db
from typing import List, Optional
from db.models.models import Cliente 
from schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from db.cruds.cliente import get_cliente, get_clientes, create_cliente, update_cliente, delete_cliente

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/", response_model=list[ClienteResponse])
def obtener_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_clientes(db, skip, limit)


@router.get("/usuario/{id_usuario}", response_model=ClienteResponse)
def obtener_cliente_por_usuario(id_usuario: int, db: Session = Depends(get_db)):
    # Buscar cliente por id_usuario
    cliente = db.query(Cliente).filter(Cliente.usuario_id_usuario == id_usuario).first()
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    return cliente


@router.get("/{id_cliente}", response_model=ClienteResponse)
def obtener_cliente(id_cliente: int, db: Session = Depends(get_db)):
    cliente = get_cliente(db, id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cuidador no encontrado")
    return cliente



#Revisar pendiente
@router.get("/select/", response_model=List[ClienteResponse])
def get_clientes(usuario_id_usuario: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Cliente)
    if usuario_id_usuario is not None:
        query = query.filter(Cliente.usuario_id_usuario == usuario_id_usuario)
    clientes = query.all()
    return clientes


@router.post("/", response_model=ClienteResponse)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return create_cliente(db, cliente)

@router.put("/{id_cliente}", response_model=ClienteResponse)
def actualizar_cliente(id_cliente: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    cliente_actualizado = update_cliente(db, id_cliente, cliente)
    if not cliente_actualizado:
        raise HTTPException(status_code=404, detail="Cuidador no encontrado")
    return cliente_actualizado

@router.delete("/{id_cliente}")
def eliminar_cliente(id_cliente: int, db: Session = Depends(get_db)):
    cliente_eliminado = delete_cliente(db, id_cliente)
    if not cliente_eliminado:
        raise HTTPException(status_code=404, detail="Cuidador no encontrado")
    return {"message": "Cuidador eliminado correctamente"}
