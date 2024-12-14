from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from app.config import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    amount_due = Column(Float, nullable=False)
    gst_percentage = Column(Float, default=18.0)
    status = Column(String, default="Pending")
    issued_date = Column(DateTime, default=datetime.utcnow)
    paid_amount = Column(Float, default=0.0)

    # Define the reverse relationship
    customer = relationship("Customer", back_populates="invoices")

    # Define the reverse relationship with cascade delete
    invoice_items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="invoice", cascade="all, delete-orphan")
