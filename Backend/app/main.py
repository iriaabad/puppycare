#Inicializar el servidor con: uvicorn main:app --reload
# Detener el server: CTRL+C
# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user_auth, users, excepciones, cuidadores, mascotas, tamano, tipomascota




app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost/",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_auth.router)
app.include_router(users.router)
app.include_router(cuidadores.router)
app.include_router(mascotas.router)
app.include_router(tipomascota.router)
app.include_router(tamano.router)


@app.get("/")
async def main():
    return {"message": "PuppyCare"}
 