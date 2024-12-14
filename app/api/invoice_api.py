from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.models.invoice import Invoice
from app.models.customer import Customer
from app.models.inventory import Inventory
from app.models.invoice_item import InvoiceItem

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create an invoice with items
@router.post("/invoices/")
def create_invoice(
    customer_id: int,
    items: list[dict],  # Example: [{"item_id": 1, "quantity": 2, "unit_price": 100.0}]
    gst_percentage: float = 18.0,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Create a new invoice
    new_invoice = Invoice(
        customer_id=customer_id,
        gst_percentage=gst_percentage,
        amount_due=0.0  # Will be updated after adding items
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    total_amount_due = 0

    for item_data in items:
        item = db.query(Inventory).filter(Inventory.id == item_data["item_id"]).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Item {item_data['item_id']} not found")

        # Use the provided unit_price or default to the item's price_per_unit
        unit_price = item_data.get("unit_price", item.price_per_unit)
        line_total = unit_price * item_data["quantity"]
        total_amount_due += line_total

        # Create invoice-item association
        invoice_item = InvoiceItem(
            invoice_id=new_invoice.id,
            item_id=item.id,
            quantity=item_data["quantity"],
            unit_price=unit_price
        )
        db.add(invoice_item)

    # Update the invoice amount
    new_invoice.amount_due = total_amount_due
    db.commit()
    db.refresh(new_invoice)
    return new_invoice

# List all invoices
@router.get("/invoices/")
def list_invoices(db: Session = Depends(get_db)):
    return db.query(Invoice).all()

# Get an invoice by ID
@router.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.delete("/invoices/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # Manually delete related invoice items
    db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).delete()

    # Now delete the invoice
    db.delete(invoice)
    db.commit()
    return {"detail": "Invoice and related items deleted successfully"}