from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

import schemas.product as schemas
from services.product_service import ProductService # MUDANÇA: Importa a CLASSE
from repositories.product_repository import ProductRepository # NOVO
from database import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# --- Dependência (Injeção de Dependência) ---
def get_product_service(db: Session = Depends(get_db)):
    """
    Cria e injeta o serviço de produto.
    O FastAPI chama get_db, e passa o 'db' para esta função.
    """
    repo = ProductRepository(db)
    return ProductService(repo)

# --- Endpoints ---

@router.get("/ranking", response_model=List[schemas.ProductRankingItem])
def get_products_ranking(
    start_date: date,
    end_date: date,
    limit: int = 10,
    store_ids: Optional[List[int]] = Query(None), 
    channel_ids: Optional[List[int]] = Query(None),
    # MUDANÇA: O serviço é injetado aqui
    service: ProductService = Depends(get_product_service)
):
    """
    Retorna o ranking de produtos mais vendidos (Top N) por faturamento.
    """
    # MUDANÇA: O router agora é "burro" e apenas chama o serviço
    return service.get_products_ranking(
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        store_ids=store_ids,
        channel_ids=channel_ids
    )

@router.get("/customizations", response_model=List[schemas.TopCustomizationItem])
def get_top_customizations(
    start_date: date,
    end_date: date,
    limit: int = 10,
    store_ids: Optional[List[int]] = Query(None), 
    channel_ids: Optional[List[int]] = Query(None),
    # MUDANÇA: O serviço é injetado aqui
    service: ProductService = Depends(get_product_service)
):
    """
    Retorna o ranking dos itens/complementos (customizações) mais vendidos.
    """
    # MUDANÇA: O router chama o serviço
    return service.get_top_customizations(
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        store_ids=store_ids,
        channel_ids=channel_ids
    )
