from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price_per_unit = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    organization = relationship("Organization", back_populates="inventory_items")
    invoice_items = relationship("InvoiceItem", back_populates="inventory")