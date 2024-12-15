from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.state_graph import graph
from langgraph.graph import MessagesState

router = APIRouter()

# Define request model
class ChatRequest(BaseModel):
    query: str

@router.post("/chat/")
async def chat_with_ai(request: ChatRequest):
    try:
        query = request.query
        print(f"[Chat API] Received Query: {query}")

        # Initialize and Invoke the State Graph
        state = MessagesState(messages=[{"role": "user", "content": query}])
        result = graph.invoke(state)

        # Extract Response
        last_message = result["messages"][-1]
        if "content" in last_message:
            print(f"[Chat API] Final Response: {last_message['content']}")
            return {"response": last_message["content"]}
        else:
            raise ValueError("No response content found.")

    except ValueError as ve:
        print(f"[Chat API] Value Error: {str(ve)}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(ve)}")

    except Exception as e:
        print(f"[Chat API] Unhandled Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
