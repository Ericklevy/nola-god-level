from pydantic import BaseModel
from decimal import Decimal

# Define o formato de saída para o endpoint /api/metrics/overview
class MetricsOverview(BaseModel):
    total_sales: int
    revenue: Decimal
    avg_ticket: Decimal
    conversion_rate: float

    class Config:
        from_attributes = True