from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.config import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    amount_due = Column(Float, nullable=False)
    gst_percentage = Column(Float, nullable=True)
    status = Column(String, nullable=True)
    paid_amount = Column(Float, default=0.0)
    issued_date = Column(DateTime, nullable=True)

    customer = relationship("Customer", back_populates="invoices")
    organization = relationship("Organization", back_populates="invoices")
    transactions = relationship("Transaction", back_populates="invoice", cascade="all, delete-orphan")
    invoice_items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")