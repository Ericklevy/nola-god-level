# time_service.py (Corrigido)

from datetime import date
from typing import List, Optional
from repositories.time_repository import TimeRepository
import schemas.time_analysis as schemas
from sqlalchemy.orm import Session # Não é mais necessário para o __init__

class TimeService:
    # MUDANÇA 1: Corrigir a Injeção de Dependência
    def __init__(self, repository: TimeRepository):
        """
        Inicializa o serviço com o repositório já injetado.
        """
        # Apenas atribui o repositório que veio do router
        self.repository = repository

    def get_sales_heatmap(
        self, 
        start_date: date, 
        end_date: date, 
        store_ids: Optional[List[int]], 
        channel_ids: Optional[List[int]]
    ) -> List[schemas.HeatmapDataPoint]:
        
        # MUDANÇA 2: Corrigir o nome do método
        # O Serviço chama o Repositório (que faz o SQL)
        heatmap_data = self.repository.get_sales_heatmap( # <--- 'get_heatmap' virou 'get_sales_heatmap'
            start_date, end_date, store_ids, channel_ids
        )
        
        # BÔNUS: Usando .model_validate() que é o padrão do Pydantic V2+
        return [schemas.HeatmapDataPoint.model_validate(item) for item in heatmap_data]

    def get_sales_timeline(
        self, 
        start_date: date, 
        end_date: date,
        group_by: str,
        store_ids: Optional[List[int]], 
        channel_ids: Optional[List[int]]
    ) -> List[schemas.TimelineDataPoint]:
        
        # A lógica de validação está correta aqui
        if group_by not in ["day", "week", "month"]:
            group_by = "day"
            
        # MUDANÇA 3: Corrigir o nome do método
        timeline_data = self.repository.get_sales_timeline( # <--- 'get_timeline' virou 'get_sales_timeline'
            start_date, end_date, group_by, store_ids, channel_ids
        )
        
        # BÔNUS: Usando .model_validate()
        return [schemas.TimelineDataPoint.model_validate(item) for item in timeline_data]