from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a la base de datos (ajústalo a tu base de datos MariaDB)
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:@localhost/Puppycarebbdd"

#"mysql://root:@localhost:3306/Puppycarebbdd?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock"

# Crear el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"charset": "utf8mb4"})

# Crear la base para los modelos
Base = declarative_base()

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
