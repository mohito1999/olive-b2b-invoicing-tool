import sys
print(sys.path)


from fastapi import FastAPI
from app.config import engine, Base
from app.models import (
    user, customer, invoice, transaction, inventory, invoice_item
)
from app.api import (
    user_api, customer_api, invoice_api, transaction_api, inventory_api
)

# Initialize FastAPI
app = FastAPI()

# Create all tables
Base.metadata.create_all(bind=engine)

# Register API routers
app.include_router(user_api, prefix="/api", tags=["Users"])
app.include_router(customer_api, prefix="/api", tags=["Customers"])
app.include_router(invoice_api, prefix="/api", tags=["Invoices"])
app.include_router(transaction_api, prefix="/api", tags=["Transactions"])
app.include_router(inventory_api, prefix="/api", tags=["Inventory"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the B2B Invoicing Tool!"}
