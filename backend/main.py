from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, get_db # Importa direto do database.py
from routers import stores, metrics, products , time_analysis , channels , customers
# Importa os módulos que criamos
import models
import schemas


app = FastAPI(
    title="Nola - Analytics para Restaurantes",
    description="API para o desafio God Level Coder"
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
        db.execute("SELECT 1")
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