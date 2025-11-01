from pydantic import BaseModel
from decimal import Decimal

# Schema para o item da lista de análise de canais
class ChannelAnalytics(BaseModel):
    channel_id: int
    channel_name: str
    total_sales: int
    revenue: Decimal
    avg_ticket: Decimal

    class Config:
        from_attributes = True