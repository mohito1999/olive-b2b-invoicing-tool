from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.models.invoice import Invoice
from app.models.transaction import Transaction  # Import the Transaction model
from app.models.customer import Customer
from app.models.user import User
from app.models.inventory import Inventory
from app.models.invoice_item import InvoiceItem
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for item input
class InvoiceItemInput(BaseModel):
    item_id: int
    quantity: int
    unit_price: Optional[float] = None  # Optional field for overriding price
    gst_percentage: Optional[float] = 0.0  # GST percentage for the item

# Create an invoice
@router.post("/invoices/")
def create_invoice(customer_id: int, organization_id: int, items: List[InvoiceItemInput], db: Session = Depends(get_db)):
    # Calculate the total amount due
    total_amount_due = 0.0
    for item_input in items:
        inventory_item = db.query(Inventory).filter(Inventory.id == item_input.item_id).first()
        if not inventory_item:
            raise HTTPException(status_code=404, detail=f"Item with ID {item_input.item_id} not found")
        
        # Use the provided unit_price if available, otherwise use the inventory's unit_price
        unit_price = item_input.unit_price if item_input.unit_price is not None else inventory_item.unit_price
        
        # Calculate the price including GST
        gst_multiplier = 1 + (item_input.gst_percentage / 100)
        total_price_with_gst = unit_price * gst_multiplier * item_input.quantity
        
        total_amount_due += total_price_with_gst

    # Create the invoice
    new_invoice = Invoice(
        customer_id=customer_id,
        organization_id=organization_id,
        amount_due=total_amount_due
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    # Create invoice items
    for item_input in items:
        unit_price = item_input.unit_price if item_input.unit_price is not None else inventory_item.unit_price
        new_invoice_item = InvoiceItem(
            invoice_id=new_invoice.id,
            item_id=item_input.item_id,
            quantity=item_input.quantity,
            unit_price=unit_price,
            gst_percentage=item_input.gst_percentage
        )
        db.add(new_invoice_item)

    db.commit()
    return new_invoice


# List all invoices
@router.get("/invoices/")
def list_invoices(db: Session = Depends(get_db)):
    return db.query(Invoice).all()

# Delete an invoice by ID
@router.delete("/invoices/{invoice_id}")
def delete_invoice(invoice_id: int, organization_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.organization_id == organization_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Delete related transactions
    db.query(Transaction).filter(Transaction.invoice_id == invoice_id).delete()

    db.delete(invoice)
    db.commit()
    return {"detail": "Invoice deleted successfully"}