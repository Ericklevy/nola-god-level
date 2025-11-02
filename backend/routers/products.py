from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

import schemas.product as schemas
import services.product_service as product_service
from database import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/ranking", response_model=List[schemas.ProductRankingItem])
def get_products_ranking(
    start_date: date,
    end_date: date,
    limit: int = 10,
    store_ids: Optional[List[int]] = Query(None), 
    channel_ids: Optional[List[int]] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retorna o ranking de produtos mais vendidos (Top N) por faturamento,
    com filtros de data, lojas e canais.
    """
    ranking = product_service.get_products_ranking(
        db=db,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        store_ids=store_ids,
        channel_ids=channel_ids
    )
    return ranking

@router.get("/customizations", response_model=List[schemas.TopCustomizationItem])
def get_top_customizations(
    start_date: date,
    end_date: date,
    limit: int = 10,
    store_ids: Optional[List[int]] = Query(None), 
    channel_ids: Optional[List[int]] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retorna o ranking dos itens/complementos (customizações) mais
    vendidos, com filtros.
    """
    top_items = product_service.get_top_customizations(
        db=db,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        store_ids=store_ids,
        channel_ids=channel_ids
    )
    return top_items