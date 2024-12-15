from langgraph import APITool

create_invoice_tool = APITool(
    name="create_invoice_tool",
    description="Create an invoice in the database",
    endpoint="http://localhost:8000/api/invoices/",
    method="POST"
)

# Add more tools as needed

