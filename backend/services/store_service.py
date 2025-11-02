from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import date
from typing import List, Optional

from models.sales import Sale
from models.stores import Store

def get_store_analytics(
    db: Session, 
    start_date: date, 
    end_date: date, 
    store_ids: Optional[List[int]] = None, 
    channel_ids: Optional[List[int]] = None
):
    query = (
        db.query(
            Store.id.label("store_id"),
            Store.name.label("store_name"),
            Store.city,
            Store.state,
            func.count(Sale.id).label("total_sales"),
            func.coalesce(func.sum(Sale.total_amount), 0.00).label("revenue"),
            func.coalesce(func.avg(Sale.total_amount), 0.00).label("avg_ticket")
        )
        .join(Sale, Store.id == Sale.store_id)
        .filter(
            Sale.created_at.between(start_date, end_date),
            Sale.sale_status_desc == 'COMPLETED'
        )
    )
    if store_ids:
        query = query.filter(Store.id.in_(store_ids))
    if channel_ids:
        query = query.filter(Sale.channel_id.in_(channel_ids))
    results = (
        query.group_by(Store.id, Store.name, Store.city, Store.state)
        .order_by(desc("revenue"))
        .all()
    )
    return results