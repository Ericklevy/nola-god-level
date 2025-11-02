# time_repository.py (Corrigido)

from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date
from typing import List, Optional
from .base_repository import BaseRepository

class TimeRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)

    # RENOMEADO AQUI (de get_heatmap para get_sales_heatmap)
    def get_sales_heatmap(
        self, 
        start_date: date, 
        end_date: date, 
        store_ids: Optional[List[int]], 
        channel_ids: Optional[List[int]]
    ):
        query = text("""
            SELECT
                EXTRACT(DOW FROM created_at) as day_of_week,
                EXTRACT(HOUR FROM created_at) as hour_of_day,
                COALESCE(SUM(total_amount), 0.00) as value
            FROM sales
            WHERE
                created_at BETWEEN :start_date AND :end_date
                AND sale_status_desc = 'COMPLETED'
                AND (:store_ids IS NULL OR store_id = ANY(:store_ids))
                AND (:channel_ids IS NULL OR channel_id = ANY(:channel_ids))
            GROUP BY
                day_of_week, hour_of_day
            ORDER BY
                day_of_week, hour_of_day
        """)
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "store_ids": store_ids,
            "channel_ids": channel_ids
        }
        return self.db.execute(query, params).all()

    # RENOMEADO AQUI (de get_timeline para get_sales_timeline)
    def get_sales_timeline(
        self, 
        start_date: date, 
        end_date: date,
        group_by: str,
        store_ids: Optional[List[int]], 
        channel_ids: Optional[List[int]]
    ):
        if group_by not in ["day", "week", "month"]:
            group_by = "day"
            
        # Corrigindo a injeção de 'group_by' para ser segura
        # Não podemos usar parâmetros (:group_by) para DATE_TRUNC
        # Então, garantimos que o valor é seguro (linha acima) e usamos f-string
        query = text(f"""
            SELECT
                DATE_TRUNC('{group_by}', created_at)::date as timestamp,
                COALESCE(SUM(total_amount), 0.00) as value
            FROM sales
            WHERE
                created_at BETWEEN :start_date AND :end_date
                AND sale_status_desc = 'COMPLETED'
                AND (:store_ids IS NULL OR store_id = ANY(:store_ids))
                AND (:channel_ids IS NULL OR channel_id = ANY(:channel_ids))
            GROUP BY
                timestamp
            ORDER BY
                timestamp ASC
        """)
        params = {
            # "group_by": group_by, # Removido dos params, injetado via f-string
            "start_date": start_date,
            "end_date": end_date,
            "store_ids": store_ids,
            "channel_ids": channel_ids
        }
        return self.db.execute(query, params).all() 