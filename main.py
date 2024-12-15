import sys
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from app.config import engine, Base
from app.models import (
    user, customer, invoice, transaction, inventory, invoice_item, organization
)
from app.api import (
    user_api, customer_api, invoice_api, transaction_api, inventory_api, organization_api, chat_api
)

# Load environment variables
load_dotenv()

# Validate Critical Environment Variables
if not os.getenv("OPENAI_API_KEY"):
    raise EnvironmentError("OPENAI_API_KEY is missing. Please check your .env file.")

# Debug Logs
print("System Path:", sys.path)
print("Loaded API Key:", os.getenv("OPENAI_API_KEY"))

# Initialize FastAPI
app = FastAPI(debug=True)

# Create Tables
print("[Main] Creating database tables...")
Base.metadata.create_all(bind=engine)
print("[Main] Database tables created.")

# Register API Routers
app.include_router(user_api, prefix="/api", tags=["Users"])
app.include_router(customer_api, prefix="/api", tags=["Customers"])
app.include_router(invoice_api, prefix="/api", tags=["Invoices"])
app.include_router(transaction_api, prefix="/api", tags=["Transactions"])
app.include_router(inventory_api, prefix="/api", tags=["Inventory"])
app.include_router(chat_api.router, prefix="/api", tags=["Chat"])
app.include_router(organization_api.router, prefix="/api", tags=["Organizations"])

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the B2B Invoicing Tool!"}

# Health Check Endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running smoothly"}
