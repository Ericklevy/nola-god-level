from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, index=True)
    sale_status_desc = Column(String, nullable=False, index=True)
    
    store_id = Column(Integer, ForeignKey("stores.id"), index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), index=True)
    
    store = relationship("Store", back_populates="sales")
    channel = relationship("Channel", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    
    product_sales = relationship("ProductSale", back_populates="sale")