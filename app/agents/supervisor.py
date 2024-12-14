from typing import Literal
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END
from app.agents.customer_agent import customer_agent
import os
from dotenv import load_dotenv

load_dotenv()  

# Initialize LLM with the correct environment variable
model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Supervisor Logic
def supervisor(state: MessagesState) -> MessagesState:
    # Access the content attribute directly
    query = state["messages"][-1].content

    # Example response (replace with LLM logic)
    if "customer" in query.lower():
        state["next_node"] = "customer_agent"
    else:
        state["next_node"] = END

    return state
