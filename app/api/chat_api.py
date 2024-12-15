from fastapi import APIRouter, HTTPException
from langgraph.graph import StateGraph, MessagesState, START
from langchain.schema import HumanMessage
from app.agents.supervisor import supervisor
from app.agents.customer_agent import customer_agent

router = APIRouter()

# Build the Graph
builder = StateGraph(MessagesState)
builder.add_node(supervisor)
builder.add_node(customer_agent)
builder.add_edge(START, "supervisor")

# Compile the Supervisor
compiled_supervisor = builder.compile()

@router.post("/api/chat/")
async def chat_with_ai(query: str):
    try:
        # Correct state initialization
        state = MessagesState(messages=[HumanMessage(content=query)])
        
        # Use the correct method to execute the compiled graph
        result = compiled_supervisor.invoke(state)  # Replace 'invoke' with the correct method if needed
        
        # Extract the last message correctly
        last_message = result["messages"][-1]
        
        # Ensure proper attribute access
        if hasattr(last_message, "content"):
            return {"response": last_message.content}
        else:
            raise ValueError("Last message has no content attribute.")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


