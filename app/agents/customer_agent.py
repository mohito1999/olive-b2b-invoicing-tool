from langgraph.graph import MessagesState

def customer_agent(state: MessagesState) -> MessagesState:
    # Access the content attribute directly
    query = state["messages"][-1].content
    response = {"role": "system", "content": f"Customer created with details: {query}"}

    state["messages"].append(response)
    state["next_node"] = "supervisor"
    return state
