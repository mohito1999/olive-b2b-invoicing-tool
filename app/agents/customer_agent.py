from langgraph.agents import BaseAgent
from app.tools.api_tools import create_customer_tool

class CustomerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="CustomerAgent")
        self.register_tool(create_customer_tool)
    
    async def handle(self, query: str):
        if "create customer" in query.lower():
            return await self.use_tool("create_customer_tool", query)
        return "I'm not sure how to handle that request."
