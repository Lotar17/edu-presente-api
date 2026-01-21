from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import create_db_and_tables
from app.routers import usuario, auth

app = FastAPI()

origins = [
  "http://localhost:4200",
  "http://localhost:8000",
]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

print("--- REGISTRANDO ROUTERS ---")
app.include_router(usuario.router)
print("Usuario registrado")
app.include_router(auth.router, tags=["Autenticación"])
print("Auth registrado")             
print("--- RUTAS DISPONIBLES: ---")
for route in app.routes:
    print(route.path)                
print("--------------------------")

