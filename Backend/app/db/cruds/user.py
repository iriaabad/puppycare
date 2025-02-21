import email
from http import client
from pydantic import EmailStr
from sqlalchemy.orm import Session
from db.models.user import User
from schemas.user import UserCreate, UserResponse


def anadir_usuario_a_bd(db: Session, user: UserCreate, hashed_password: str):
    # Crear el objeto usuario
    db_user = User(
        nombre=user.nombre,
        apellido1=user.apellido1,
        apellido2=user.apellido2, 
        email=user.email,
        hashed_password=hashed_password,  
        latitud=user.latitud,
        longitud=user.longitud,
        calle=user.calle,
        numero=user.numero,
        piso=user.piso,
        codigopostal=user.codigopostal,
        ciudad=user.ciudad
    )
    db.add(db_user)  # Añadir el usuario a la sesión
    db.commit()  # Confirmar los cambios
    db.refresh(db_user)  # Para obtener el objeto actualizado con su ID, por ejemplo
    return db_user  # Retorna el usuario añadido

# Buscar el usuario por el email
def buscar_usuario_en_bd_por_email(db: Session, email: EmailStr):
    """Busca un usuario en la base de datos por su email."""
    return db.query(User).filter(User.email == email).first()


# Buscar el usuario por el id_usuario
def buscar_user_por_id(db: Session, id: int):
    return db.query(User).filter(User.id_usuario == id).first()


#Busca usuario y devuelve campos del usuario
def buscar_user_completo(id: int, db: Session) -> UserResponse:
    #Busca un usuario en la base de datos y devuelve la respuesta en formato UserResponse
    user = db.query(User).filter(User.id_usuario == id).first()  # Realiza la consulta a la base de datos
    if user:
        return UserResponse(nombre=user.nombre, email=user.email, apellido1=user.apellido1)  # Retorna el esquema UserResponse
    return None  # Si no se encuentra el usuario, devuelve None

