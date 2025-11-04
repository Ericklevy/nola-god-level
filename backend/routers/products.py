from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

import schemas.product as schemas
from services.product_service import ProductService 
from repositories.product_repository import ProductRepository 
from database import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

def get_product_service(db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    return ProductService(repo)

@router.get("/ranking", response_model=List[schemas.ProductRankingItem])
def get_products_ranking(
    start_date: date,
    end_date: date,
    # REMOVEMOS limit e skip daqui
    store_ids: Optional[List[int]] = Query(None), 
    channel_ids: Optional[List[int]] = Query(None),
    service: ProductService = Depends(get_product_service)
):
    """
    Retorna o ranking de TODOS os produtos mais vendidos por faturamento.
    """
    return service.get_products_ranking(
        start_date=start_date,
        end_date=end_date,
        # REMOVEMOS limit e skip daqui
        store_ids=store_ids,
        channel_ids=channel_ids
    )

@router.get("/customizations", response_model=List[schemas.TopCustomizationItem])
def get_top_customizations(
    start_date: date,
    end_date: date,
    limit: int = 10, # Mantemos o limit aqui, pois 10 está bom
    store_ids: Optional[List[int]] = Query(None), 
    channel_ids: Optional[List[int]] = Query(None),
    service: ProductService = Depends(get_product_service)
):
    return service.get_top_customizations(
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        store_ids=store_ids,
        channel_ids=channel_ids
    )