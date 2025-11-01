from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional , Literal
from database import get_db

import schemas.time_analysis as schemas
import services.analytics as analytics_service


router = APIRouter(
    prefix="/time-analysis",
    tags=["Time Analysis"]
)

@router.get("/heatmap", response_model=List[schemas.HeatmapDataPoint])
def get_time_analysis_heatmap(
    start_date: date,
    end_date: date,
    store_ids: Optional[List[int]] = Query(None), 
    channel_ids: Optional[List[int]] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retorna os dados para o heatmap de vendas (Dia da Semana x Hora).
    - day_of_week: 0=Domingo, 1=Segunda, ..., 6=Sábado
    - hour_of_day: 0-23
    - value: Faturamento total no período
    """
    heatmap_data = analytics_service.get_sales_heatmap(
        db=db,
        start_date=start_date,
        end_date=end_date,
        store_ids=store_ids,
        channel_ids=channel_ids
    )
    return heatmap_data

@router.get("/timeline", response_model=List[schemas.TimelineDataPoint])
def get_sales_timeline_data(
    start_date: date,
    end_date: date,
    # 'Literal' força a API a aceitar apenas esses valores
    group_by: Literal["day", "week", "month"] = "day",
    store_ids: Optional[List[int]] = Query(None), 
    channel_ids: Optional[List[int]] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retorna dados de série temporal (timestamp, valor) para o faturamento,
    agrupado por 'day', 'week', ou 'month'.
    """
    timeline_data = analytics_service.get_sales_timeline(
        db=db,
        start_date=start_date,
        end_date=end_date,
        group_by=group_by,
        store_ids=store_ids,
        channel_ids=channel_ids
    )
    return timeline_data