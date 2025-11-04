from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine, get_db # Importa direto do database.py
from routers import stores, metrics, products , time_analysis , channels , customers
# Importa os módulos que criamos
import models
import schemas


app = FastAPI(
    title="Nola - Analytics para Restaurantes",
    description="API para o desafio God Level Coder"
)

origins = [
    "http://localhost:3000", # Endereço do frontend React (se rodar na porta 3000)
    "http://localhost:5173", # Endereço do frontend React (se rodar na porta 5173)
    "https://nola-god-level.onrender.com", # Endereço do backend no Render
    # Adicione aqui a URL do seu frontend quando ele estiver no ar (ex: no Vercel)
    "https://nola-god-level-alpha.vercel.app", # Exemplo de frontend no Vercel
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Permite as origens da lista
    allow_credentials=True,      # Permite cookies (se usar)
    allow_methods=["*"],         # Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],         # Permite todos os cabeçalhos
)

# --- Inclui os Roteadores ---
app.include_router(stores.router, prefix="/api")
app.include_router(metrics.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(time_analysis.router, prefix="/api")
app.include_router(channels.router, prefix="/api")
app.include_router(customers.router, prefix="/api")

# --- Endpoint de Saúde ---
@app.get("/api/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail={
            "status": "error",
            "database": "disconnected",
            "error": str(e)
        })

@app.get("/api")
def get_root():
    return {"message": "Bem-vindo à API Nola Analytics"}