from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import date
from typing import List, Optional
from .base_repository import BaseRepository
from models.products import Product
from models.product_sales import ProductSale
from models.sales import Sale
from models.categories import Category
from models.items import Item
from models.item_product_sales import ItemProductSale

class ProductRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_ranking(
        self, 
        start_date: date, 
        end_date: date, 
        # REMOVEMOS limit e skip daqui
        store_ids: Optional[List[int]], 
        channel_ids: Optional[List[int]]
    ):
        query = (
            self.db.query(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                Category.name.label("category_name"),
                func.sum(ProductSale.quantity).label("quantity_sold"),
                func.sum(ProductSale.total_price).label("revenue")
            )
            .join(ProductSale, Product.id == ProductSale.product_id)
            .join(Sale, ProductSale.sale_id == Sale.id)
            .outerjoin(Category, Product.category_id == Category.id)
            .filter(
                Sale.created_at.between(start_date, end_date),
                Sale.sale_status_desc == 'COMPLETED'
            )
        )
        if store_ids:
            query = query.filter(Sale.store_id.in_(store_ids))
        if channel_ids:
            query = query.filter(Sale.channel_id.in_(channel_ids))
        
        return (
            query.group_by(Product.id, Product.name, Category.name)
            .order_by(desc("revenue"))
            # REMOVEMOS .offset() E .limit() DAQUI
            .all()
        )

    def get_top_customizations(
        self, 
        start_date: date, 
        end_date: date, 
        limit: int,
        store_ids: Optional[List[int]], 
        channel_ids: Optional[List[int]]
    ):
        query = (
            self.db.query(
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
        if store_ids:
            query = query.filter(Sale.store_id.in_(store_ids))
        if channel_ids:
            query = query.filter(Sale.channel_id.in_(channel_ids))
            
        return (
            query.group_by(Item.id, Item.name)
            .order_by(desc("times_added"))
            .limit(limit)
            .all()
        )