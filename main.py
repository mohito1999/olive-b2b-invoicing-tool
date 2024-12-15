import sys
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from langgraph.graph import StateGraph, MessagesState, START
from langchain.schema import HumanMessage
from app.agents.supervisor import supervisor
from app.agents.customer_agent import customer_agent
from app.config import engine, Base
from app.models import (
    user, customer, invoice, transaction, inventory, invoice_item, organization
)
from app.api import (
    user_api, customer_api, invoice_api, transaction_api, inventory_api, organization_api, chat_api
)


# Load environment variables
load_dotenv()

# Debug: Print system paths and API key for verification
print("System Path:", sys.path)
print("Loaded API Key:", os.getenv("OPENAI_API_KEY"))

# Initialize FastAPI
app = FastAPI(debug=True)

# Define State Graph
builder = StateGraph(MessagesState)
builder.add_node(supervisor)
builder.add_node(customer_agent)
builder.add_edge(START, "supervisor")

# Compile the graph
compiled_supervisor = builder.compile()

# Debug log to verify the compiled supervisor type
print("Compiled Supervisor Type:", type(compiled_supervisor))

# Create all tables
Base.metadata.create_all(bind=engine)

# Register API routers
app.include_router(user_api, prefix="/api", tags=["Users"])
app.include_router(customer_api, prefix="/api", tags=["Customers"])
app.include_router(invoice_api, prefix="/api", tags=["Invoices"])
app.include_router(transaction_api, prefix="/api", tags=["Transactions"])
app.include_router(inventory_api, prefix="/api", tags=["Inventory"])
app.include_router(chat_api.router, prefix="/api", tags=["Chat"])
app.include_router(organization_api.router, prefix="/api", tags=["Organizations"])



# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the B2B Invoicing Tool!"}
