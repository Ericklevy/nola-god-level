from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

import schemas.customer as schemas
from services.customer_service import CustomerService
from repositories.customer_repository import CustomerRepository
from database import get_db

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

# --- Dependência (Injeção de Dependência) ---
def get_customer_service(db: Session = Depends(get_db)):
    """
    Cria e injeta o serviço de cliente.
    """
    repo = CustomerRepository(db)
    return CustomerService(repo)

# --- Endpoints ---

@router.get("/top", response_model=List[schemas.TopCustomer])
def get_top_customers_ranking(
    start_date: date,
    end_date: date,
    limit: int = 10,
    service: CustomerService = Depends(get_customer_service)
):
    """
    Retorna o ranking de top clientes por valor total gasto.
    """
    return service.get_top_customers(
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )

@router.get("/segments", response_model=schemas.CustomerSegment)
def get_customer_segments(
    start_date: date,
    end_date: date,
    segment: str = "at_risk",
    limit: int = 50,
    service: CustomerService = Depends(get_customer_service)
):
    """
    Retorna uma lista de clientes que se encaixam em um segmento
    específico (ex: 'at_risk').
    """
    return service.get_customer_segment(
        segment_type=segment,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )
