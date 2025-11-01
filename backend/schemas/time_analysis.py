from pydantic import BaseModel
from decimal import Decimal
from datetime import date

class HeatmapDataPoint(BaseModel):
    day_of_week: int  # 0=Domingo, 1=Segunda, ..., 6=Sábado
    hour_of_day: int  # 0-23
    value: Decimal

    class Config:
        from_attributes = True

class TimelineDataPoint(BaseModel):
    timestamp: date  # Usamos 'date' para agrupar por dia/semana/mês
    value: Decimal

    class Config:
        from_attributes = True