from sqlalchemy.orm import Session
from db.models.user import User
from schemas.user import UserCreate


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

    
    # Agregar el usuario a la base de datos
    db.add(db_user)
    db.commit()  # Confirmar los cambios
    db.refresh(db_user)  # Refrescar para obtener los valores actualizados del objeto
    return db_user

# Buscar el usuario por el email
def search_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()