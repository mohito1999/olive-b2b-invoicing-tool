from langgraph.agents import Supervisor
from app.agents.customer_agent import CustomerAgent
from app.agents.invoice_agent import InvoiceAgent

class MainSupervisor(Supervisor):
    def __init__(self):
        super().__init__(name="MainSupervisor")
        self.register_agent(CustomerAgent())
        self.register_agent(InvoiceAgent())

    async def route_request(self, query: str):
        return await self.handle_query(query)
