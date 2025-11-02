# store_service.py (Corrigido)

from datetime import date
from typing import List, Optional
from repositories.store_repository import StoreRepository
import schemas.store as schemas
# A Session não é mais necessária aqui no init
# from sqlalchemy.orm import Session 

class StoreService:
    def __init__(self, repository: StoreRepository): # MUDANÇA 1: Receba o repositório
        """
        Inicializa o serviço com o repositório já criado.
        """
        self.repository = repository # MUDANÇA 2: Apenas atribua o repositório
                                     # Não crie um novo aqui.

    def get_store_analytics(
        self, 
        start_date: date, 
        end_date: date, 
        store_ids: Optional[List[int]], 
        channel_ids: Optional[List[int]]
    ) -> List[schemas.StoreAnalytics]:
        
        # 1. O Serviço chama o Repositório (que faz o SQL)
        analytics_data = self.repository.get_analytics(
            start_date, end_date, store_ids, channel_ids
        )
        
        # 2. O Serviço converte os dados para o schema da API
        # NOTA: O seu schema precisa ter .from_attributes() ou .model_validate()
        # Se .from_attributes() não existir, use .model_validate()
        
        # Usando model_validate para garantir compatibilidade com Pydantic V2+
        # e tratando os dados que vêm do SQLAlchemy (Row objects)
        return [schemas.StoreAnalytics.model_validate(item) for item in analytics_data]