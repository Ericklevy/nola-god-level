from pydantic import BaseModel
from decimal import Decimal
from datetime import date, datetime
from typing import List
# Schema para o item da lista de top clientes
class TopCustomer(BaseModel):
    customer_id: int
    customer_name: str | None
    email: str | None
    total_spent: Decimal
    total_orders: int
    avg_ticket: Decimal
    last_order_date: datetime | None

    class Config:
        from_attributes = True

# Define o cliente individual dentro de um segmento
class CustomerSegmentData(BaseModel):
    customer_id: int
    customer_name: str | None
    email: str | None
    total_orders: int
    total_spent: Decimal
    days_since_last_order: int

    class Config:
        from_attributes = True

# Define a resposta final da API
class CustomerSegment(BaseModel):
    segment_name: str
    customer_count: int
    customers: List[CustomerSegmentData] # Lista de clientes no segmento

    class Config:
        from_attributes = True # Garanta que está assim