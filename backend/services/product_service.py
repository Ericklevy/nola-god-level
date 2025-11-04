# product_service.py (Corrigido)

from datetime import date
from typing import List, Optional
from repositories.product_repository import ProductRepository
import schemas.product as schemas
from sqlalchemy.orm import Session # Não é mais usado no __init__

class ProductService:
    # MUDANÇA 1: Recebe o repositório, não a sessão 'db'
    def __init__(self, repository: ProductRepository):
        """
        Inicializa o serviço com o repositório já injetado.
        """
        # MUDANÇA 2: Apenas atribui o repositório recebido
        self.repository = repository

    def get_products_ranking(
        self, 
        start_date: date, 
        end_date: date, 
        limit: int,
        store_ids: Optional[List[int]], 
        channel_ids: Optional[List[int]]
    ) -> List[schemas.ProductRankingItem]:
        
        # 1. Chama o repositório (que faz o SQL)
        ranking_data = self.repository.get_ranking(
            start_date, end_date, limit, store_ids, channel_ids
        )
        
        # 2. Converte cada item da lista para o schema Pydantic
        # BÔNUS: .model_validate() é o substituto moderno do .from_attributes()
        return [schemas.ProductRankingItem.model_validate(item) for item in ranking_data]

    def get_top_customizations(
        self, 
        start_date: date, 
        end_date: date, 
        limit: int,
        store_ids: Optional[List[int]], 
        channel_ids: Optional[List[int]]
    ) -> List[schemas.TopCustomizationItem]:
        
        # 1. Chama o repositório (que faz o SQL)
        customizations_data = self.repository.get_top_customizations(
            start_date, end_date, limit, store_ids, channel_ids
        )
        
        # 2. Converte os resultados para o schema Pydantic
        # BÔNUS: .model_validate() é o substituto moderno do .from_attributes()
        return [schemas.TopCustomizationItem.model_validate(item) for item in customizations_data]