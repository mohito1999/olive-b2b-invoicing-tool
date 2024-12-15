from langgraph.graph import StateGraph, MessagesState, START, END
from app.agents.supervisor import supervisor
from app.agents.invoice_agent import invoice_agent
from app.agents.customer_agent import customer_agent

# Define State Graph
builder = StateGraph(MessagesState)
builder.add_node("supervisor", supervisor)
builder.add_node("invoice_agent", invoice_agent)
builder.add_node("customer_agent", customer_agent)

# Define Transitions
builder.add_edge(START, "supervisor")
builder.add_edge("supervisor", "invoice_agent")
builder.add_edge("supervisor", "customer_agent")
builder.add_edge("supervisor", END)

# Compile the Graph
print("Compiling State Graph...")
graph = builder.compile()
print("State Graph Compiled.")
