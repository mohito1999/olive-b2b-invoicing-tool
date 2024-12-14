from langgraph.tools import APITool

create_customer_tool = APITool(
    name="create_customer_tool",
    description="Create a customer in the database",
    endpoint="http://localhost:8000/api/customers/",
    method="POST"
)
