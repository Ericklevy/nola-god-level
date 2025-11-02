# channel_service.py (Corrigido)

from datetime import date
from typing import List, Optional
from repositories.channel_repository import ChannelRepository
import schemas.channel as schemas
from sqlalchemy.orm import Session # Não é mais usado no __init__

class ChannelService:
    # MUDANÇA 1: Recebe o Repositório, não a sessão
    def __init__(self, repository: ChannelRepository):
        """
        Inicializa o serviço com o repositório já injetado.
        """
        # MUDANÇA 2: Apenas atribui o repositório
        self.repository = repository

    def get_channel_analytics(
        self, 
        start_date: date, 
        end_date: date, 
        store_ids: Optional[List[int]], 
        channel_ids: Optional[List[int]]
    ) -> List[schemas.ChannelAnalytics]:
        
        # 1. O Serviço chama o Repositório (que faz o SQL)
        analytics_data = self.repository.get_analytics(
            start_date, end_date, store_ids, channel_ids
        )
        
        # 2. O Serviço converte os dados para o schema da API
        # BÔNUS: .model_validate() é o substituto moderno do .from_attributes()
        return [schemas.ChannelAnalytics.model_validate(item) for item in analytics_data]