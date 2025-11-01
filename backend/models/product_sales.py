from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ProductSale(Base):
    __tablename__ = "product_sales"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Float, nullable=False)
    base_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    sale_id = Column(Integer, ForeignKey("sales.id"), index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)

    sale = relationship("Sale", back_populates="product_sales")
    product = relationship("Product", back_populates="product_sales")

    item_sales = relationship("ItemProductSale", back_populates="product_sale")