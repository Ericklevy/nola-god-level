from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

import schemas.channel as schemas
import services.channel_service as channel_service
from database import get_db

router = APIRouter(
    prefix="/channels",
    tags=["Channels"]
)

@router.get("/analytics", response_model=List[schemas.ChannelAnalytics])
def get_channel_analytics(
    start_date: date,
    end_date: date,
    store_ids: Optional[List[int]] = Query(None), 
    channel_ids: Optional[List[int]] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retorna a análise de métricas (vendas, faturamento, ticket médio)
    agrupada por canal.
    """
    analytics_data = channel_service.get_channel_analytics(
        db=db,
        start_date=start_date,
        end_date=end_date,
        store_ids=store_ids,
        channel_ids=channel_ids
    )
    return analytics_data