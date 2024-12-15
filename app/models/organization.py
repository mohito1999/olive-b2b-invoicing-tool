from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="organization")
    customers = relationship("Customer", back_populates="organization")
    invoices = relationship("Invoice", back_populates="organization")
    transactions = relationship("Transaction", back_populates="organization")
    inventory_items = relationship("Inventory", back_populates="organization")