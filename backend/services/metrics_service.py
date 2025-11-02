# metrics_service.py (Corrigido)

from datetime import date
from typing import List, Optional
from repositories.metrics_repository import MetricsRepository
from schemas.metrics import MetricsOverview
from sqlalchemy.orm import Session # Session não é mais usada no __init__

class MetricsService:
    # MUDANÇA 1: O __init__ agora recebe o Repositório, não a Session
    def __init__(self, repository: MetricsRepository):
        """
        Inicializa o serviço com o repositório já injetado.
        """
        # MUDANÇA 2: Apenas atribui o repositório
        self.repository = repository
    
    def get_overview_metrics(
        self, 
        start_date: date, 
        end_date: date, 
        store_ids: Optional[List[int]] = None, 
        channel_ids: Optional[List[int]] = None
    ) -> MetricsOverview:
        
        # 1. Lógica de Negócio (ex: validar datas)
        if start_date > end_date:
            raise ValueError("Data inicial não pode ser maior que a data final")
            
        # 2. Chama o repositório (que faz o SQL)
        metrics_data = self.repository.get_overview(
            start_date=start_date,
            end_date=end_date,
            store_ids=store_ids,
            channel_ids=channel_ids
        )
        
        # 3. Converte o resultado do banco (Row) para o schema Pydantic (DTO)
        # BÔNUS: Use .model_validate() que é o padrão do Pydantic V2+
        # (substituto do .from_attributes() / orm_mode)
        if metrics_data:
            return MetricsOverview.model_validate(metrics_data)
        
        # Retorna um schema vazio se a query não retornar nada
        return MetricsOverview(total_sales=0, revenue=0, avg_ticket=0, conversion_rate=0)