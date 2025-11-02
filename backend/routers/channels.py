from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

import schemas.channel as schemas
from services.channel_service import ChannelService
from repositories.channel_repository import ChannelRepository
from database import get_db

router = APIRouter(
    prefix="/channels",
    tags=["Channels"]
)

# --- Dependência (Injeção de Dependência) ---
def get_channel_service(db: Session = Depends(get_db)):
    """
    Cria e injeta o serviço de canal.
    """
    repo = ChannelRepository(db)
    return ChannelService(repo)

# --- Endpoints ---

@router.get("/analytics", response_model=List[schemas.ChannelAnalytics])
def get_channel_analytics(
    start_date: date,
    end_date: date,
    store_ids: Optional[List[int]] = Query(None), 
    channel_ids: Optional[List[int]] = Query(None),
    service: ChannelService = Depends(get_channel_service)
):
    """
    Retorna a análise de métricas agrupada por canal.
    """
    return service.get_channel_analytics(
        start_date=start_date,
        end_date=end_date,
        store_ids=store_ids,
        channel_ids=channel_ids
    )
