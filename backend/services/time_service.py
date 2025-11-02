from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date
from typing import List, Optional

def get_sales_heatmap(
    db: Session, 
    start_date: date, 
    end_date: date, 
    store_ids: Optional[List[int]] = None, 
    channel_ids: Optional[List[int]] = None
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
    results = db.execute(query, params).all()
    return results

def get_sales_timeline(
    db: Session, 
    start_date: date, 
    end_date: date,
    group_by: str = "day",
    store_ids: Optional[List[int]] = None, 
    channel_ids: Optional[List[int]] = None
):
    if group_by not in ["day", "week", "month"]:
        group_by = "day"
        
    query = text(f"""
        SELECT
            DATE_TRUNC(:group_by, created_at)::date as timestamp,
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
        "group_by": group_by,
        "start_date": start_date,
        "end_date": end_date,
        "store_ids": store_ids,
        "channel_ids": channel_ids
    }
    results = db.execute(query, params).all()
    return results