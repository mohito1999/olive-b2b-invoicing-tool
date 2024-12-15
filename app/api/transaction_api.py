from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.models.transaction import Transaction
from app.models.invoice import Invoice
from app.models.user import User

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a transaction
@router.post("/transactions/")
def create_transaction(invoice_id: int, amount_paid: float, organization_id: int, db: Session = Depends(get_db)):
    # Fetch the invoice
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.organization_id == organization_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # Create a new transaction
    new_transaction = Transaction(
        invoice_id=invoice_id,
        amount_paid=amount_paid,
        organization_id=organization_id
    )
    db.add(new_transaction)

    # Update the invoice's paid amount and status
    invoice.paid_amount += amount_paid
    if invoice.paid_amount >= invoice.amount_due:
        invoice.status = "Paid"
    else:
        invoice.status = "Partially Paid"

    # Commit the changes
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

# List all transactions
@router.get("/transactions/")
def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()

@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transaction)
    db.commit()
    return {"detail": "Transaction deleted successfully"}