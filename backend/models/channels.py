from sqlalchemy import Column, Integer, String, CHAR
from sqlalchemy.orm import relationship
from database import Base

class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(CHAR(1)) # 'P' ou 'D'

    sales = relationship("Sale", back_populates="channel")