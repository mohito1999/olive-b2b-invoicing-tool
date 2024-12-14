from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.config import SessionLocal
from app.models.inventory import Inventory

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create an item
@router.post("/inventory/")
def create_item(
    name: str,
    description: str,
    price_per_unit: float,
    stock_quantity: Optional[int] = Query(0),
    db: Session = Depends(get_db)
):
    new_item = Inventory(
        name=name,
        description=description,
        price_per_unit=price_per_unit,
        stock_quantity=stock_quantity
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# List all items
@router.get("/inventory/")
def list_items(db: Session = Depends(get_db)):
    return db.query(Inventory).all()

# Get item by ID
@router.get("/inventory/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item