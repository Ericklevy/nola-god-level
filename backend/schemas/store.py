from pydantic import BaseModel
from decimal import Decimal

class StoreBase(BaseModel):
    name: str
    city: str | None = None
    state: str | None = None

class Store(StoreBase):
    id: int
    is_active: bool
    latitude: Decimal | None = None
    longitude: Decimal | None = None

    class Config:
        from_attributes = True # Antigo orm_mode

class StoreAnalytics(BaseModel):
    store_id: int
    store_name: str
    city: str | None
    state: str | None
    total_sales: int
    revenue: Decimal
    avg_ticket: Decimal

    class Config:
        from_attributes = True