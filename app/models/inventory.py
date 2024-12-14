from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.config import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price_per_unit = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
