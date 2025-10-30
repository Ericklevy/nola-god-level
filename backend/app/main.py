from fastapi import FastAPI
import os
import psycopg2
from elasticsearch import Elasticsearch

app = FastAPI(title="Nola Backend API")

# Lê variáveis de ambiente
DB_URL = os.environ.get("DATABASE_URL")
ELASTIC_URL = os.environ.get("ELASTIC_URL")

# Tenta conectar para fins de exemplo
try:
    db_conn = psycopg2.connect(DB_URL)
    es_client = Elasticsearch(ELASTIC_URL)
except Exception as e:
    print(f"Error connecting to services: {e}")
    db_conn = None
    es_client = None


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Nola God Level Challenge"}

@app.get("/health")
def health_check():
    db_status = "connected" if db_conn else "disconnected"
    es_status = "connected" if es_client and es_client.ping() else "disconnected"
    
    return {
        "status": "ok",
        "services": {
            "database": db_status,
            "elasticsearch": es_status
        }
    }