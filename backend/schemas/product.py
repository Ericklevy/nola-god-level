from pydantic import BaseModel
from decimal import Decimal

# Schema para o item da lista do ranking
class ProductRankingItem(BaseModel):
    product_id: int
    product_name: str
    category_name: str | None # Categoria pode ser nula
    quantity_sold: Decimal
    revenue: Decimal

    class Config:
        from_attributes = True

class TopCustomizationItem(BaseModel):
    item_id: int
    item_name: str
    times_added: int
    revenue_generated: Decimal

    class Config:
        from_attributes = True