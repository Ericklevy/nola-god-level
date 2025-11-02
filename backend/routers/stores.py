from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

import models.stores as models
import schemas.store as schemas
from services.store_service import StoreService
from repositories.store_repository import StoreRepository
from database import get_db

router = APIRouter(
    prefix="/stores",
    tags=["Stores"]
)

# --- Dependência (Injeção de Dependência) ---
def get_store_service(db: Session = Depends(get_db)):
    """
    Cria e injeta o serviço de loja.
    """
    repo = StoreRepository(db)
    return StoreService(repo)

# --- Endpoints ---

@router.get("/ranking", response_model=List[schemas.StoreAnalytics])
def get_store_ranking(
    start_date: date,
    end_date: date,
    store_ids: Optional[List[int]] = Query(None), 
    channel_ids: Optional[List[int]] = Query(None),
    service: StoreService = Depends(get_store_service)
):
    """
    Retorna o ranking de lojas por performance (faturamento, vendas,
    ticket médio), com filtros.
    """
    return service.get_store_analytics(
        start_date=start_date,
        end_date=end_date,
        store_ids=store_ids,
        channel_ids=channel_ids
    )

@router.get("/{store_id}", response_model=schemas.Store)
def get_store(store_id: int, db: Session = Depends(get_db)):
    """
    Busca uma loja específica pelo ID. (Este não precisa de um serviço
    complexo, então pode acessar o banco diretamente para uma busca simples).
    """
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if store is None:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    return store

@router.get("/", response_model=List[schemas.Store])
def get_stores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Busca as lojas do banco de dados com paginação.
    """
    stores = db.query(models.Store).offset(skip).limit(limit).all()
    return stores
