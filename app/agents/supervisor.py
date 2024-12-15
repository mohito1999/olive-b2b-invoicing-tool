from langgraph.graph import MessagesState
from app.llm_setup import get_llm_response

# Define Available Agents
AGENT_MAPPING = {
    "invoice": "invoice_agent",
    "customer": "customer_agent",
    "end": "END"
}

# LLM-Powered Supervisor Logic
def supervisor(state: MessagesState) -> MessagesState:
    query = state["messages"][-1].content.lower()
    print(f"[Supervisor] Received Query: {query}")

    # LLM Prompt for Routing
    prompt = f"""
    You are an AI-based supervisor managing a business process automation system. 
    Based on the following query, decide which agent should handle it:

    Available agents:
    - Invoice Agent (handles invoice creation)
    - Customer Agent (handles customer management)
    
    Query: "{query}"

    Respond with only the next agent's name like `invoice_agent`, `customer_agent`, or `END` if no further action is required.
    """

    try:
        # Use Azure OpenAI to decide the next agent
        response = get_llm_response(prompt)
        next_agent = response.strip().lower()
        print(f"[Supervisor] Routed to: {next_agent}")

        if next_agent in AGENT_MAPPING.values():
            state["next_node"] = next_agent
        else:
            print("[Supervisor] Invalid route. Ending session.")
            state["next_node"] = "END"

    except Exception as e:
        print(f"[Supervisor] Error during routing: {str(e)}")
        state["next_node"] = "END"

    return state
