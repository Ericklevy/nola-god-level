from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

import schemas.metrics as schemas
from services.metrics_service import MetricsService
from repositories.metrics_repository import MetricsRepository
from database import get_db

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)

# --- Dependência (Injeção de Dependência) ---
def get_metrics_service(db: Session = Depends(get_db)):
    """
    Cria e injeta o serviço de métricas.
    """
    repo = MetricsRepository(db)
    return MetricsService(repo)

# --- Endpoints ---

@router.get("/overview", response_model=schemas.MetricsOverview)
def get_overview(
    start_date: date,
    end_date: date,
    store_ids: Optional[List[int]] = Query(None), 
    channel_ids: Optional[List[int]] = Query(None),
    service: MetricsService = Depends(get_metrics_service) # Injeta o serviço
):
    """
    Calcula os KPIs de visão geral (overview) para o dashboard principal
    com base nos filtros de data, lojas e canais.
    """
    # O router agora é "burro". Ele só passa a chamada para o serviço.
    return service.get_overview_metrics(
        start_date=start_date,
        end_date=end_date,
        store_ids=store_ids,
        channel_ids=channel_ids
    )
