from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a user
@router.post("/users/")
def create_user(username: str, email: str, password: str, organization_id: int, db: Session = Depends(get_db)):
    new_user = User(
        username=username,
        email=email,
        password=password,
        organization_id=organization_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# List all users
@router.get("/users/")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}