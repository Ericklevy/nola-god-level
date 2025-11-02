from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import date
from typing import List, Optional

from models.sales import Sale
from models.channels import Channel

def get_channel_analytics(
    db: Session, 
    start_date: date, 
    end_date: date, 
    store_ids: Optional[List[int]] = None, 
    channel_ids: Optional[List[int]] = None
):
    query = (
        db.query(
            Channel.id.label("channel_id"),
            Channel.name.label("channel_name"),
            func.count(Sale.id).label("total_sales"),
            func.coalesce(func.sum(Sale.total_amount), 0.00).label("revenue"),
            func.coalesce(func.avg(Sale.total_amount), 0.00).label("avg_ticket")
        )
        .join(Sale, Channel.id == Sale.channel_id)
        .filter(
            Sale.created_at.between(start_date, end_date),
            Sale.sale_status_desc == 'COMPLETED'
        )
    )
    if store_ids:
        query = query.filter(Sale.store_id.in_(store_ids))
    if channel_ids:
        query = query.filter(Channel.id.in_(channel_ids))
    results = (
        query.group_by(Channel.id, Channel.name)
        .order_by(desc("revenue"))
        .all()
    )
    return results