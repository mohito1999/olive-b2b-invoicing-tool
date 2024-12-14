from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.models.customer import Customer

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a customer
@router.post("/customers/")
def create_customer(name: str, company_name: str, email: str, phone_number: str = None, address: str = None, db: Session = Depends(get_db)):
    existing_customer = db.query(Customer).filter(Customer.email == email).first()
    if existing_customer:
        raise HTTPException(status_code=400, detail="Customer already exists")
    
    new_customer = Customer(
        name=name,  # POC name
        company_name=company_name,
        email=email,
        phone_number=phone_number,
        address=address
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

# List all customers
@router.get("/customers/")
def list_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()

@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return {"detail": "Customer deleted successfully"}