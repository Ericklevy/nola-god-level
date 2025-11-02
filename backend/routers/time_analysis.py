from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional, Literal

import schemas.time_analysis as schemas
from services.time_service import TimeService # MUDANÇA: Importa a CLASSE
from repositories.time_repository import TimeRepository # NOVO
from database import get_db

router = APIRouter(
    prefix="/time-analysis",
    tags=["Time Analysis"]
)

# --- Dependência (Injeção de Dependência) ---
def get_time_service(db: Session = Depends(get_db)):
    """
    Cria e injeta o serviço de análise temporal.
    """
    repo = TimeRepository(db)
    return TimeService(repo)

# --- Endpoints ---

@router.get("/heatmap", response_model=List[schemas.HeatmapDataPoint])
def get_time_analysis_heatmap(
    start_date: date,
    end_date: date,
    store_ids: Optional[List[int]] = Query(None), 
    channel_ids: Optional[List[int]] = Query(None),
    # MUDANÇA: O serviço é injetado aqui
    service: TimeService = Depends(get_time_service)
):
    """
    Retorna os dados para o heatmap de vendas (Dia da Semana x Hora).
    - day_of_week: 0=Domingo, 1=Segunda, ..., 6=Sábado
    - hour_of_day: 0-23
    - value: Faturamento total no período
    """
    # MUDANÇA: O router chama o serviço
    return service.get_sales_heatmap(
        start_date=start_date,
        end_date=end_date,
        store_ids=store_ids,
        channel_ids=channel_ids
    )

@router.get("/timeline", response_model=List[schemas.TimelineDataPoint])
def get_sales_timeline_data(
    start_date: date,
    end_date: date,
    group_by: Literal["day", "week", "month"] = "day",
    store_ids: Optional[List[int]] = Query(None), 
    channel_ids: Optional[List[int]] = Query(None),
    # MUDANÇA: O serviço é injetado aqui
    service: TimeService = Depends(get_time_service)
):
    """
    Retorna dados de série temporal (timestamp, valor) para o faturamento,
    agrupado por 'day', 'week', ou 'month'.
    """
    # MUDANÇA: O router chama o serviço
    return service.get_sales_timeline(
        start_date=start_date,
        end_date=end_date,
        group_by=group_by,
        store_ids=store_ids,
        channel_ids=channel_ids
    )