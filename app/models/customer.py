from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    organization = relationship("Organization", back_populates="customers")
    invoices = relationship("Invoice", back_populates="customer")