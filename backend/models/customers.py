from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100))
    email = Column(String(100))
    phone_number = Column(String(50))
    birth_date = Column(Date)
    created_at = Column(DateTime)

    sales = relationship("Sale", back_populates="customer")