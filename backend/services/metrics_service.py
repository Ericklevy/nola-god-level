from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date
from typing import List, Optional

def get_overview_metrics(
    db: Session, 
    start_date: date, 
    end_date: date, 
    store_ids: Optional[List[int]] = None, 
    channel_ids: Optional[List[int]] = None
):
    query = text("""
        SELECT
            COUNT(*) as total_sales,
            COALESCE(SUM(total_amount), 0.00) as revenue,
            COALESCE(AVG(total_amount), 0.00) as avg_ticket,
            COALESCE(
                SUM(CASE WHEN sale_status_desc = 'COMPLETED' THEN 1 ELSE 0 END)::float / NULLIF(COUNT(*), 0), 0
            ) * 100 as conversion_rate
        FROM sales
        WHERE
            created_at BETWEEN :start_date AND :end_date
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
    
    result = db.execute(query, params).first()
    return result