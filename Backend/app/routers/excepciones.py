##Excepciones
from fastapi import HTTPException, status

auth_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credenciales de autenticación inválidas",
    headers={"WWW-Authenticate": "Bearer"}
)

