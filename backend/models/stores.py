from sqlalchemy import Column, Integer, String, Boolean, DECIMAL
from sqlalchemy.orm import relationship
from database import Base # Importa a Base do database.py

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String)
    state = Column(String(2))
    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))
    is_active = Column(Boolean, default=True)

    sales = relationship("Sale", back_populates="store")