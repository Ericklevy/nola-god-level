from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional


import schemas.customer as schemas
import services.customer_service as customer_service
from database import get_db

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

@router.get("/top", response_model=List[schemas.TopCustomer])
def get_top_customers_ranking(
    start_date: date,
    end_date: date,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Retorna o ranking de top clientes por valor total gasto.
    """
    top_customers = customer_service.get_top_customers(
        db=db,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )
    return top_customers

@router.get("/segments", response_model=schemas.CustomerSegment)
def get_customer_segments(
    start_date: date,
    end_date: date,
    segment: str = "at_risk", # Define "at_risk" como padrão
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Retorna uma lista de clientes que se encaixam em um segmento
    específico (ex: 'at_risk').

    - **at_risk**: Clientes com 3+ pedidos que não compram há > 30 dias.
    """

    customers = customer_service.get_customer_segment(
        db=db,
        segment_type=segment,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )

    return {
        "segment_name": segment,
        "customer_count": len(customers),
        "customers": customers
    }