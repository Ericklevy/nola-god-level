from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

import schemas.metrics as schemas # Importa o schema de resposta
import services.metrics_service as metrics_service # Importa a lógica de negócio
from database import get_db

router = APIRouter(
    prefix="/metrics", # O prefixo será /api/metrics
    tags=["Metrics"]  # Tag para a documentação /docs
)

@router.get("/overview", response_model=schemas.MetricsOverview)
def get_overview(
    start_date: date,
    end_date: date,
    # Query(None) é a forma moderna de declarar parâmetros de lista opcionais
    store_ids: Optional[List[int]] = Query(None), 
    channel_ids: Optional[List[int]] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Calcula os KPIs de visão geral (overview) para o dashboard principal
    com base nos filtros de data, lojas e canais.
    """
    metrics = metrics_service.get_overview_metrics(
        db=db,
        start_date=start_date,
        end_date=end_date,
        store_ids=store_ids,
        channel_ids=channel_ids
    )
    
    return metrics