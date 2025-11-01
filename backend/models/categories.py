from sqlalchemy import Column, Integer, String, CHAR
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(CHAR(1)) # 'P' para Produto, 'I' para Item

    products = relationship("Product", back_populates="category")