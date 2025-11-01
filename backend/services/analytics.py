from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import func, desc
from datetime import date
from typing import List, Optional
from models.products import Product
from models.product_sales import ProductSale
from models.sales import Sale
from models.categories import Category
from models.channels import Channel
from models.stores import Store
from models.customers import Customer
from models.items import Item
from models.item_product_sales import ItemProductSale

def get_overview_metrics(
    db: Session, 
    start_date: date, 
    end_date: date, 
    store_ids: Optional[List[int]] = None, 
    channel_ids: Optional[List[int]] = None
):
    # Esta é a query SQL otimizada, como sugerido no PDF [cite: 424-432]
    # Usamos COALESCE para evitar erros se a soma for NULA (0 vendas)
    query = text("""
        SELECT
            COUNT(*) as total_sales,
            COALESCE(SUM(total_amount), 0) as revenue,
            COALESCE(AVG(total_amount), 0) as avg_ticket,
            COALESCE(
                SUM(CASE WHEN sale_status_desc = 'COMPLETED' THEN 1 ELSE 0 END)::float / NULLIF(COUNT(*), 0), 0
            ) * 100 as conversion_rate
        FROM sales
        WHERE
            created_at BETWEEN :start_date AND :end_date
            AND sale_status_desc IN ('COMPLETED', 'CANCELLED')
            -- Filtros opcionais
            AND (:store_ids IS NULL OR store_id = ANY(:store_ids))
            AND (:channel_ids IS NULL OR channel_id = ANY(:channel_ids))
    """)
    
    # Prepara os parâmetros para a query
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "store_ids": store_ids,
        "channel_ids": channel_ids
    }
    
    # Executa a query e busca o primeiro (e único) resultado
    result = db.execute(query, params).first()
    
    return result

def get_products_ranking(
    db: Session, 
    start_date: date, 
    end_date: date, 
    limit: int = 10,
    store_ids: Optional[List[int]] = None, 
    channel_ids: Optional[List[int]] = None
):
    query = (
        db.query(
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            Category.name.label("category_name"),
            func.sum(ProductSale.quantity).label("quantity_sold"),
            func.sum(ProductSale.total_price).label("revenue")
        )
        .join(ProductSale, Product.id == ProductSale.product_id)
        .join(Sale, ProductSale.sale_id == Sale.id)
        .outerjoin(Category, Product.category_id == Category.id) # outerjoin pois categoria pode ser nula
        .filter(
            Sale.created_at.between(start_date, end_date),
            Sale.sale_status_desc == 'COMPLETED'
        )
    )

    # Aplica filtros opcionais
    if store_ids:
        query = query.filter(Sale.store_id.in_(store_ids))

    if channel_ids:
        query = query.filter(Sale.channel_id.in_(channel_ids))

    # Agrupa, ordena e limita
    results = (
        query.group_by(Product.id, Product.name, Category.name)
        .order_by(desc("revenue")) # Ordena por faturamento [cite: 578]
        .limit(limit)
        .all()
    )

    return results

def get_sales_heatmap(
    db: Session, 
    start_date: date, 
    end_date: date, 
    store_ids: Optional[List[int]] = None, 
    channel_ids: Optional[List[int]] = None
):
    # EXTRACT(DOW FROM ...) -> 0=Domingo, 1=Segunda, ... 6=Sábado
    # EXTRACT(HOUR FROM ...) -> 0-23
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

def get_channel_analytics(
    db: Session, 
    start_date: date, 
    end_date: date, 
    store_ids: Optional[List[int]] = None, 
    channel_ids: Optional[List[int]] = None
):
    # Query baseada no exemplo do PDF 
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

    # Aplica filtros opcionais
    if store_ids:
        query = query.filter(Sale.store_id.in_(store_ids))

    if channel_ids:
        query = query.filter(Channel.id.in_(channel_ids))

    # Agrupa e ordena
    results = (
        query.group_by(Channel.id, Channel.name)
        .order_by(desc("revenue"))
        .all()
    )

    return results

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
        .join(Sale, Store.id == Sale.store_id) # Junta Sale na Store
        .filter(
            Sale.created_at.between(start_date, end_date),
            Sale.sale_status_desc == 'COMPLETED'
        )
    )

    # Aplica filtros opcionais
    if store_ids:
        query = query.filter(Store.id.in_(store_ids))

    if channel_ids:
        query = query.filter(Sale.channel_id.in_(channel_ids))

    # Agrupa e ordena
    results = (
        query.group_by(Store.id, Store.name, Store.city, Store.state)
        .order_by(desc("revenue"))
        .all()
    )

    return results

def get_top_customers(
    db: Session, 
    start_date: date, 
    end_date: date, 
    limit: int = 10
):
    query = (
        db.query(
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

    results = (
        query.group_by(Customer.id, Customer.customer_name, Customer.email)
        .order_by(desc("total_spent"))
        .limit(limit)
        .all()
    )

    return results

def get_top_customizations(
    db: Session, 
    start_date: date, 
    end_date: date, 
    limit: int = 10,
    store_ids: Optional[List[int]] = None, 
    channel_ids: Optional[List[int]] = None
):
    query = (
        db.query(
            Item.id.label("item_id"),
            Item.name.label("item_name"),
            func.count(ItemProductSale.id).label("times_added"),
            func.coalesce(func.sum(ItemProductSale.additional_price * ItemProductSale.quantity), 0.00).label("revenue_generated")
        )
        .join(ItemProductSale, Item.id == ItemProductSale.item_id)
        .join(ProductSale, ItemProductSale.product_sale_id == ProductSale.id)
        .join(Sale, ProductSale.sale_id == Sale.id)
        .filter(
            Sale.created_at.between(start_date, end_date),
            Sale.sale_status_desc == 'COMPLETED'
        )
    )

    # Aplica filtros opcionais
    if store_ids:
        query = query.filter(Sale.store_id.in_(store_ids))

    if channel_ids:
        query = query.filter(Sale.channel_id.in_(channel_ids))

    # Agrupa, ordena e limita
    results = (
        query.group_by(Item.id, Item.name)
        .order_by(desc("times_added")) # Ordena por quantas vezes foi adicionado
        .limit(limit)
        .all()
    )

    return results


# ... (outras funções de analytics) ...

def get_customer_segment(
    db: Session, 
    segment_type: str, # "at_risk"
    start_date: date, 
    end_date: date,
    limit: int = 50 # Limita a lista de clientes
):
    # Usamos 'CURRENT_DATE' para calcular a recência (dias desde a última compra)
    # O 'end_date' aqui é usado para definir a "data de hoje" da análise.

    # 1. Subquery (CTE) para calcular RFM de cada cliente
    rfm_cte = text("""
        WITH CustomerRFM AS (
            SELECT
                c.id as customer_id,
                c.customer_name,
                c.email,
                COUNT(s.id) as frequency,
                SUM(s.total_amount) as monetary,
                MAX(s.created_at) as last_order_date,
            -- Calcula dias desde a última compra
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

    # 2. Query principal que usa a CTE para filtrar o segmento
    if segment_type == "at_risk":
        # "Em Risco": Comprou 3+ vezes, mas não compra há mais de 30 dias
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
                recency DESC, -- Mostra os mais "esquecidos" primeiro
                monetary DESC
            LIMIT :limit
        """)

    # (Futuramente, você pode adicionar 'else if segment_type == "vips": ...')

    else:
        return [] # Retorna vazio se o segmento não for conhecido

    params = {
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit
    }

    results = db.execute(query, params).all()
    return results


def get_sales_timeline(
    db: Session, 
    start_date: date, 
    end_date: date,
    group_by: str = "day", # 'day', 'week', ou 'month'
    store_ids: Optional[List[int]] = None, 
    channel_ids: Optional[List[int]] = None
):
    # Valida o parâmetro group_by para evitar SQL Injection
    if group_by not in ["day", "week", "month"]:
        group_by = "day"

    # DATE_TRUNC trunca a data para o início do dia/semana/mês
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