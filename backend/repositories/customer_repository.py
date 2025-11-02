from sqlalchemy.orm import Session
from sqlalchemy import text, func, desc
from datetime import date
from typing import List, Optional
from .base_repository import BaseRepository
from models.sales import Sale
from models.customers import Customer

class CustomerRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_top_customers(
        self, 
        start_date: date, 
        end_date: date, 
        limit: int
    ):
        query = (
            self.db.query(
                Customer.id.label("customer_id"),
                Customer.customer_name,
                Customer.email,
                func.coalesce(func.sum(Sale.total_amount), 0.00).label("total_spent"),
                func.count(Sale.id).label("total_orders"),
                func.coalesce(func.avg(Sale.total_amount), 0.00).label("avg_ticket"),
                func.max(Sale.created_at).label("last_order_date")
            )
            .join(Sale, Customer.id == Sale.customer_id)
            .filter(
                Sale.created_at.between(start_date, end_date),
                Sale.sale_status_desc == 'COMPLETED'
            )
        )
        return (
            query.group_by(Customer.id, Customer.customer_name, Customer.email)
            .order_by(desc("total_spent"))
            .limit(limit)
            .all()
        )

    def get_at_risk_segment(
        self, 
        start_date: date, 
        end_date: date,
        limit: int
    ):
        rfm_cte = text("""
            WITH CustomerRFM AS (
                SELECT
                    c.id as customer_id,
                    c.customer_name,
                    c.email,
                    COUNT(s.id) as frequency,
                    SUM(s.total_amount) as monetary,
                    MAX(s.created_at) as last_order_date,
                    EXTRACT(DAY FROM (:end_date - MAX(s.created_at))) as recency
                FROM customers c
                JOIN sales s ON c.id = s.customer_id
                WHERE
                    s.created_at BETWEEN :start_date AND :end_date
                    AND s.sale_status_desc = 'COMPLETED'
                GROUP BY
                    c.id, c.customer_name, c.email
            )
        """)
        
        query = text(rfm_cte.text + """
            SELECT
                customer_id,
                customer_name,
                email,
                frequency as total_orders,
                monetary as total_spent,
                recency as days_since_last_order
            FROM CustomerRFM
            WHERE
                frequency >= 3
                AND recency > 30
            ORDER BY
                recency DESC,
                monetary DESC
            LIMIT :limit
        """)

        params = {
            "start_date": start_date,
            "end_date": end_date,
            "limit": limit
        }
        return self.db.execute(query, params).all()
