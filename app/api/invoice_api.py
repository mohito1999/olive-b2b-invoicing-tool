from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.config import SessionLocal
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.models.transaction import Transaction
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Dependency for Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Ensure Session Close


# Pydantic Model for Invoice Item Input
class InvoiceItemInput(BaseModel):
    item_id: int
    quantity: int
    unit_price: Optional[float] = None
    gst_percentage: Optional[float] = 0.0


# Create Invoice API with Immediate Return
@router.post("/invoices/")
def create_invoice(
    customer_id: int,
    organization_id: int,
    items: List[InvoiceItemInput],
    db: Session = Depends(get_db)
):
    print(f"[Invoices API] Received Create Request: Customer={customer_id}, Org={organization_id}, Items={items}")

    try:
        # Calculate Total Amount Due
        total_amount_due = 0.0

        for item_input in items:
            item_total = item_input.unit_price * (1 + (item_input.gst_percentage / 100)) * item_input.quantity
            total_amount_due += item_total
            print(f"[Invoices API] Calculated Item Total: Item={item_input.item_id}, Amount={item_total}")

        # Create Invoice Record
        new_invoice = Invoice(
            customer_id=customer_id,
            organization_id=organization_id,
            amount_due=total_amount_due
        )
        db.add(new_invoice)
        db.commit()
        db.refresh(new_invoice)
        print(f"[Invoices API] Invoice Created: ID={new_invoice.id}")

        # Create Invoice Items
        for item_input in items:
            new_invoice_item = InvoiceItem(
                invoice_id=new_invoice.id,
                item_id=item_input.item_id,
                quantity=item_input.quantity,
                unit_price=item_input.unit_price,
                gst_percentage=item_input.gst_percentage
            )
            db.add(new_invoice_item)
            print(f"[Invoices API] Created Invoice Item: {new_invoice_item}")

        db.commit()
        print(f"[Invoices API] Invoice Commit Successful for ID={new_invoice.id}")

        return {"detail": f"Invoice created successfully. ID={new_invoice.id}"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
# List All Invoices
@router.get("/invoices/")
def list_invoices(db: Session = Depends(get_db)):
    invoices = db.query(Invoice).all()
    print(f"[Invoices API] Retrieved {len(invoices)} Invoices")
    return invoices

# Delete an Invoice by ID
@router.delete("/invoices/{invoice_id}")
def delete_invoice(invoice_id: int, organization_id: int, db: Session = Depends(get_db)):
    print(f"[Invoices API] Delete Request Received for Invoice ID={invoice_id}, Org ID={organization_id}")

    # Find Invoice by ID and Org
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.organization_id == organization_id
    ).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # Delete Related Transactions
    deleted_transactions = db.query(Transaction).filter(Transaction.invoice_id == invoice_id).delete()
    print(f"[Invoices API] Deleted Transactions: {deleted_transactions}")

    # Delete Related Invoice Items
    deleted_items = db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).delete()
    print(f"[Invoices API] Deleted Invoice Items: {deleted_items}")

    # Delete the Invoice
    db.delete(invoice)
    db.commit()
    print(f"[Invoices API] Invoice ID={invoice_id} Deleted Successfully")
    return {"detail": "Invoice deleted successfully"}
