from sqlalchemy.orm import Session
from db.models.models import Cliente
from schemas.cliente import ClienteCreate

def get_cliente(db: Session, id_cliente: int):
    return db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()


def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cliente).offset(skip).limit(limit).all()

def create_cliente(db: Session, cliente: ClienteCreate):
    db_cliente = Cliente(usuario_id_usuario=cliente.usuario_id_usuario)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def update_cliente(db: Session, id_cliente: int, cliente_update: ClienteCreate):
    db_cliente = get_cliente(db, id_cliente)
    if db_cliente:
        db_cliente.usuario_id_usuario = cliente_update.usuario_id_usuario
        db.commit()
        db.refresh(db_cliente)
    return db_cliente

def delete_cliente(db: Session, id_cliente: int):
    db_cliente = get_cliente(db, id_cliente)
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
    return db_cliente
