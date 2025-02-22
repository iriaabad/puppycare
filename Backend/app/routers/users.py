
import email
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from db.cruds.user import UserCreate, buscar_usuario_en_bd_por_email, anadir_usuario_a_bd
from db.client import get_db, SessionLocal
from schemas.user import UserBase, UserCreate, UserResponse
from passlib.context import CryptContext
from jwt import PyJWK, PyJWKError, encode



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
    

    #Devuelve la información del new user que acabamos de crear
    return UserResponse.from_orm(new_user)


