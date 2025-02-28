import email
import re
from urllib import response
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI, Response, Cookie, Request
from typing import Annotated
from fastapi import responses
import jwt
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWK, PyJWKError, decode,encode
from datetime import datetime, timedelta
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from sqlalchemy import false
from sqlmodel import Session
from db.models.models import User
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
async def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):

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
        expiracion_fecha = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRACION_MINUTOS)
        payload = {
        "sub": user.email,  # 'sub' es un campo estándar que identifica al sujeto (usuario)
        "exp": expiracion_fecha  # Fecha de expiración del token
        }


        # Codificar el token JWT con el payload y la clave secreta
        access_token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)

        response = JSONResponse(content={"message": "Usuario logado correctamente"})

        # Usar la función para establecer la cookie
        set_access_token_cookie(response, access_token)


        return response

     

def set_access_token_cookie(response: Response, access_token: str):
    # Calcula la fecha de expiración en formato GMT
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRACION_MINUTOS * 60)
    expire_str = expire_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    max_age = ACCESS_TOKEN_EXPIRACION_MINUTOS * 60

    # Construye manualmente el valor del header Set-Cookie
    cookie_value = (
        f"access_token={access_token}; "
        f"Max-Age={max_age}; "
        f"Expires={expire_str}; "
        #"HttpOnly; "        # Indica que la cookie no es accesible vía JavaScript (he tenido que activarlo para que funcione)
        "Secure; "          # Asegúrate de usar True en producción si tienes HTTPS
        "Path=/; "
        "SameSite=None; "   # Permite el uso cross-site
        "Partitioned"       # Inyecta el atributo Partitioned
    )

    # Agrega el header manualmente
    response.headers.append("Set-Cookie", cookie_value)
    


@router.get("/check-cookie")
async def check_cookie(request: Request):
    print(request.cookies)  # Log para ver las cookies que se están recibiendo
    token = request.cookies.get("access_token")
    if token:
        return {"cookie": token}
    return {"message": "Cookie no encontrada"}


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


@router.get("/users/me")
async def read_users_me(request: Request, db: Session = Depends(get_db)):
    # Obtener el token de la cookie
    token = request.cookies.get("access_token")

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found in cookies",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar y decodificar el token
    payload = verificar_token(token)

    # Obtener el usuario de la base de datos
    user = buscar_usuario_en_bd_por_email(db, email=payload["sub"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Devolver los datos del usuario
    return {
        "id_usuario": user.id_usuario,
        "email": user.email,
        "nombre": user.nombre,
        "apellido1": user.apellido1,
        "apellido2": user.apellido2,
    }




def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
