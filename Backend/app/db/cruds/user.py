import email
from fastapi import HTTPException
from http import client
from pydantic import EmailStr
from sqlalchemy.orm import Session
from db.models.user import User
from schemas.user import UserCreate, UserResponse, UserUpdate


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

def actualizar_usuario_en_bd(db: Session, id_usuario: int, user_actualizar: UserUpdate):
    user_existente = db.query(User).filter(User.id_usuario == id_usuario).first()

    if not user_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Convertir el esquema Pydantic en un diccionario y excluir valores no proporcionados
    datos_actualizados = user_actualizar.dict(exclude_unset=True)

    # Evitar actualizar 'hashed_password' si no se proporciona
    if "hashed_password" in datos_actualizados:
        datos_actualizados.pop("hashed_password", None)

    # Aplicar los cambios a la instancia de la base de datos
    for key, value in datos_actualizados.items():
        setattr(user_existente, key, value)

    db.commit()
    db.refresh(user_existente)  # Asegurarse de obtener los datos actualizados desde la BD
    return user_existente