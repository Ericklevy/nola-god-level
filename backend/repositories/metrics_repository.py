from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date
from typing import List, Optional
from .base_repository import BaseRepository
from models.sales import Sale # Precisamos dos modelos para as queries

class MetricsRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_overview(
        self, 
        start_date: date, 
        end_date: date, 
        store_ids: Optional[List[int]] = None, 
        channel_ids: Optional[List[int]] = None
    ):
        query = text("""
            SELECT
                -- 1. Total de pedidos (Concluídos + Cancelados)
                COUNT(*) as total_sales,
                
                -- 2. Receita (revenue) - SOMA APENAS VENDAS 'COMPLETED'
                COALESCE(SUM(
                    CASE 
                        WHEN sale_status_desc = 'COMPLETED' THEN total_amount 
                        ELSE 0 
                    END
                ), 0.00) as revenue,
                
                -- 3. Ticket Médio (avg_ticket) - MÉDIA APENAS VENDAS 'COMPLETED'
                COALESCE(AVG(
                    CASE 
                        WHEN sale_status_desc = 'COMPLETED' THEN total_amount 
                        ELSE NULL -- NULL é ignorado pelo AVG
                    END
                ), 0.00) as avg_ticket,
                
                -- 4. Taxa de Conversão (Correta como estava)
                COALESCE(
                    SUM(CASE WHEN sale_status_desc = 'COMPLETED' THEN 1 ELSE 0 END)::float / NULLIF(COUNT(*), 0), 0
                ) * 100 as conversion_rate
            FROM sales
            WHERE
                created_at BETWEEN :start_date AND :end_date
                -- O WHERE principal ainda precisa de ambos para a Taxa de Conversão
                AND sale_status_desc IN ('COMPLETED', 'CANCELLED')
                AND (:store_ids IS NULL OR store_id = ANY(:store_ids))
                AND (:channel_ids IS NULL OR channel_id = ANY(:channel_ids))
        """)
        
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "store_ids": store_ids,
            "channel_ids": channel_ids
        }
        
        return self.db.execute(query, params).first()
