#Inicializar el servidor con: uvicorn main:app --reload
# Detener el server: CTRL+C
# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user_auth, users, excepciones




app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000"
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





@app.get("/")
async def main():
    return {"message": "Hello World"}
 