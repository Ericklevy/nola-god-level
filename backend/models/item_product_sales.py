from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ItemProductSale(Base):
    __tablename__ = "item_product_sales"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Float, nullable=False)
    additional_price = Column(Float, nullable=False)
    price = Column(Float, nullable=False) # Preço total (qty * additional_price)

    product_sale_id = Column(Integer, ForeignKey("product_sales.id"), index=True)
    item_id = Column(Integer, ForeignKey("items.id"), index=True)

    # Relacionamentos
    product_sale = relationship("ProductSale", back_populates="item_sales")
    item = relationship("Item", back_populates="item_sales")