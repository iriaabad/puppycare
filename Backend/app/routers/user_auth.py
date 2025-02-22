import email
from urllib import response
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI, Response, Cookie, Request
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
from fastapi.responses import  JSONResponse



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

         # Generar el payload con la expiración del token
        expiracion_fecha = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRACION_MINUTOS)
        payload = {
        "sub": user.email,  # 'sub' es un campo estándar que identifica al sujeto (usuario)
        "exp": expiracion_fecha  # Fecha de expiración del token
        }

        # Codificar el token JWT con el payload y la clave secreta
        access_token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)


         # Guardar el token en una cookie
        response.establecer_cookie(
        key="access_token",  # Nombre de la cookie
        value=access_token,  # Almaceno el token
        max_age=ACCESS_TOKEN_EXPIRACION_MINUTOS,  # Misma duración que el token
        expires=datetime.utcnow() + ACCESS_TOKEN_EXPIRACION_MINUTOS,  # Misma fecha de expiracion
        httponly=True,  # Hace que la cookie solo sea accesible por el servidor, no a través de JavaScript
        secure=True,  # Solo se enviará a través de HTTPS
        samesite="Strict",  # Esto ayuda a proteger contra ataques CSRF (se puede cambiar a "Lax" para menos restricciones)
    )
        
        return JSONResponse(content={"message": "Usuario logado correctamente"})

     

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


#obtiene el token y valida el usuario
@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    # Aquí current_user ya es el usuario validado
    return current_user


#Obtiene la validación del token desde la cookie
@router.get("/users/me")
async def read_users_me(request: Request ):
    # Obtener el token de la cookie
    token = request.cookies.get("access_token")

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found in cookies",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar y decodificar el token
    user = verificar_token(token) #Uso la funcion definida para ese fin

    return {"user": user}


#   Función para verificar el token
async def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )