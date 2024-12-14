from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.models.transaction import Transaction
from app.models.invoice import Invoice

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Record a transaction
@router.post("/transactions/")
def create_transaction(invoice_id: int, amount_paid: float, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if amount_paid + invoice.paid_amount > invoice.amount_due:
        raise HTTPException(status_code=400, detail="Payment exceeds invoice amount")

    # Create a new transaction
    new_transaction = Transaction(
        invoice_id=invoice_id,
        amount_paid=amount_paid
    )
    db.add(new_transaction)

    # Update the invoice's paid amount and status
    invoice.paid_amount += amount_paid
    if invoice.paid_amount == 0:
        invoice.status = "Pending"
    elif invoice.paid_amount < invoice.amount_due:
        invoice.status = "Underpaid"
    elif invoice.paid_amount == invoice.amount_due:
        invoice.status = "Paid"

    db.commit()
    db.refresh(invoice)
    return new_transaction

@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transaction)
    db.commit()
    return {"detail": "Transaction deleted successfully"}

# List all transactions
@router.get("/transactions/")
def list_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return transactions