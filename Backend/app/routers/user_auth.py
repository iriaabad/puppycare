import email
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from typing import Annotated
import jwt
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWK, PyJWKError, decode,encode
from datetime import datetime, timedelta
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlmodel import Session
from db.models.user import User
from db.models.auth import Token, TokenData
from schemas.user import UserResponse
from db.cruds.user import buscar_usuario_en_bd_por_email
from db.client import SessionLocal, get_db
from .excepciones import auth_exception


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRACION_MINUTOS = 30
SECRET = "f400e41e9995b5b60849ad9406956e4fe2772a6a78b39d15c23858ec90fb8077"

router = APIRouter(prefix="/auth",
                   tags=["auth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")



crypt = CryptContext(schemes=["bcrypt"])


async def current_user(user: User = Depends()):
        
        return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    #Buscar usuario por email
        user = buscar_usuario_en_bd_por_email(db, form.username)    
        
        if not user:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

        if not crypt.verify(form.password, user.hashed_password): 
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcta"
        )

        access_token = {
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRACION_MINUTOS)
    }

        return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer"
    }

async def get_current_user(token: Annotated[str, Depends(oauth2)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise auth_exception
        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise auth_exception
    user = buscar_usuario_en_bd_por_email(db, email=token_data.username)
    if user is None:
        raise auth_exception
    return user


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    # Aquí current_user ya es el usuario validado
    return current_user
