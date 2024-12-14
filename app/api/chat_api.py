from fastapi import APIRouter, HTTPException
from langgraph.graph import StateGraph, MessagesState, START
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

@router.post("/chat/")
async def chat_with_ai(query: str):
    try:
        state = MessagesState(messages=[{"role": "user", "content": query}])
        # Use the correct method to execute the compiled graph
        result = compiled_supervisor.invoke(state)  # Replace 'invoke' with the correct method if needed
        return {"response": result["messages"][-1]["content"]}
    except Exception as e:
        import traceback
        print("Error Details:", str(e))
        print("Full Traceback:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
