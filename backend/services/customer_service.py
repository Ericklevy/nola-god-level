# customer_service.py (Corrigido)

from datetime import date
from typing import List, Optional
from repositories.customer_repository import CustomerRepository
import schemas.customer as schemas
from sqlalchemy.orm import Session # Não é mais usado no __init__

class CustomerService:
    # MUDANÇA 1: Recebe o Repositório, não a sessão
    def __init__(self, repository: CustomerRepository):
        """
        Inicializa o serviço com o repositório já injetado.
        """
        # MUDANÇA 2: Apenas atribui o repositório
        self.repository = repository

    def get_top_customers(
        self, 
        start_date: date, 
        end_date: date, 
        limit: int
    ) -> List[schemas.TopCustomer]:
        
        # 1. O Serviço chama o Repositório (que faz o SQL)
        customers_data = self.repository.get_top_customers(
            start_date, end_date, limit
        )
        
        # 2. O Serviço converte os dados para o schema da API
        # BÔNUS: .model_validate() é o substituto moderno do .from_attributes()
        return [schemas.TopCustomer.model_validate(item) for item in customers_data]

    def get_customer_segment(
        self, 
        segment_type: str, 
        start_date: date, 
        end_date: date,
        limit: int
    ) -> schemas.CustomerSegment:
        
        # 3. O Serviço contém a LÓGICA DE NEGÓCIO
        if segment_type == "at_risk":
            # O repositório faz o "como"
            customers = self.repository.get_at_risk_segment(
                start_date, end_date, limit
            )
        # (Aqui você poderia adicionar 'else if segment_type == "vips": ...')
        else:
            customers = []
            
        # 4. O Serviço monta o objeto de resposta final
        # BÔNUS: .model_validate() é o substituto moderno do .from_attributes()
        return schemas.CustomerSegment(
            segment_name=segment_type,
            customer_count=len(customers),
            customers=[schemas.CustomerSegmentData.model_validate(c) for c in customers]
        )