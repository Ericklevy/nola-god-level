from datetime import date
from typing import List, Optional
from repositories.product_repository import ProductRepository
import schemas.product as schemas
from sqlalchemy.orm import Session

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_products_ranking(
        self, 
        start_date: date, 
        end_date: date, 
        # REMOVEMOS limit e skip daqui
        store_ids: Optional[List[int]], 
        channel_ids: Optional[List[int]]
    ) -> List[schemas.ProductRankingItem]:
        
        ranking_data = self.repository.get_ranking(
            start_date, end_date, store_ids, channel_ids # REMOVEMOS limit e skip daqui
        )
        
        return [schemas.ProductRankingItem.model_validate(item) for item in ranking_data]

    def get_top_customizations(
        self, 
        start_date: date, 
        end_date: date, 
        limit: int,
        store_ids: Optional[List[int]], 
        channel_ids: Optional[List[int]]
    ) -> List[schemas.TopCustomizationItem]:
        
        customizations_data = self.repository.get_top_customizations(
            start_date, end_date, limit, store_ids, channel_ids
        )
        
        return [schemas.TopCustomizationItem.model_validate(item) for item in customizations_data]