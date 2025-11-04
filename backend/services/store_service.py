# store_service.py (Corrigido)

from datetime import date
from typing import List, Optional
from repositories.store_repository import StoreRepository
import schemas.store as schemas
from sqlalchemy.orm import Session 

class StoreService:
    def __init__(self, repository: StoreRepository):
        """
        Inicializa o serviço com o repositório já criado.
        """
        self.repository = repository

    def get_store_analytics(
        self, 
        start_date: date, 
        end_date: date, 
        store_ids: Optional[List[int]], 
        channel_ids: Optional[List[int]]
    ) -> List[schemas.StoreAnalytics]:
        
        analytics_data = self.repository.get_analytics(
            start_date, end_date, store_ids, channel_ids
        )
        
        return [schemas.StoreAnalytics.model_validate(item) for item in analytics_data]