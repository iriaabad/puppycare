
import email
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from db.cruds.user import UserCreate, buscar_usuario_en_bd_por_email, anadir_usuario_a_bd, actualizar_usuario_en_bd
from db.cruds.cliente import create_cliente
from db.client import get_db, SessionLocal
from schemas.user import UserBase, UserCreate, UserResponse, UserUpdate
from schemas.cliente import ClienteBase, ClienteCreate
from passlib.context import CryptContext
from db.models.models import User, Cliente
from pydantic import BaseModel


router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


# Crear un contexto para el hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Crear un usuario en la base de datos
@router.post("/create", response_model= UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    existing_user = buscar_usuario_en_bd_por_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario con ese email ya existe",
        )
    
    # Hashear la contraseña
    hashed_password = pwd_context.hash(user.password)
    
    # Crear el nuevo usuario en la base de datos con la contraseña hasheada
    new_user = anadir_usuario_a_bd(db=db, user=user, hashed_password=hashed_password)
    print("Usuario creado:", new_user)

    if new_user is None:
        raise HTTPException(status_code=500, detail="Error al crear usuario.")  # <-- Evitar que retorne None
    
    # Crear el cliente usando el id_usuario del nuevo usuario
    cliente_data = ClienteCreate(usuario_id_usuario=new_user.id_usuario)
    new_cliente = create_cliente(db, cliente_data)
    
    # Devuelve la información del usuario recién creado
    return UserResponse.model_validate(new_user)


@router.get("/user/{id_usuario}", response_model= UserResponse) 
def get_user(id_usuario: int, db: Session = Depends(get_db)):
    # Buscar el usuario en la base de datos
    user = db.query(User).filter(User.id_usuario == id_usuario).first()

    # Si no se encuentra el usuario, lanzar un error 404
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Devolver los datos del usuario en formato JSON
    return UserResponse.model_validate(user)

@router.put("/user/{id_usuario}")
def update_user(id_usuario: int, user_actualizar: UserUpdate, db: Session = Depends(get_db)):
    # Buscar el usuario en la base de datos
    user_existente = db.query(User).filter(User.id_usuario == id_usuario).first()

    # Si no se encuentra el usuario, lanzar un error 404
    if user_existente is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Llamar a la función para actualizar el usuario
    updated_user = actualizar_usuario_en_bd(db=db, id_usuario=id_usuario, user_actualizar=user_actualizar)

    if updated_user is None:  
        raise HTTPException(status_code=500, detail="Error al actualizar usuario.")  # <-- Evitar que retorne None
    
    # Devolver los datos del usuario actualizado en formato JSON
    return UserResponse.model_validate(updated_user)
