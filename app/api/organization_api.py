from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.models.organization import Organization

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/organizations/")
def create_organization(name: str, db: Session = Depends(get_db)):
    existing_org = db.query(Organization).filter(Organization.name == name).first()
    if existing_org:
        raise HTTPException(status_code=400, detail="Organization already exists")
    
    new_org = Organization(name=name)
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org

@router.get("/organizations/")
def list_organizations(db: Session = Depends(get_db)):
    return db.query(Organization).all()

@router.get("/organizations/{org_id}")
def get_organization(org_id: int, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.delete("/organizations/{org_id}")
def delete_organization(org_id: int, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    db.delete(org)
    db.commit()
    return {"detail": "Organization deleted successfully"}