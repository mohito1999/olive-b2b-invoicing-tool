import requests
import json
import re
from langgraph.graph import MessagesState
from app.llm_setup import get_llm_response

# Invoice Agent Function
def invoice_agent(state: MessagesState) -> MessagesState:
    query = state["messages"][-1].content
    print(f"[Invoice Agent] Received Query: {query}")

    # Define Correct LLM Prompt
    prompt = f"""
    Extract ONLY the following details from this user request as a JSON object:

    Query: "{query}"

    Expected Format:
    {{
        "customer_id": "<customer_id>",
        "organization_id": "<organization_id>",
        "items": [
            {{
                "item_id": "<item_id>",
                "quantity": "<quantity>",
                "unit_price": "<unit_price>",
                "gst_percentage": "<gst_percentage>"
            }}
        ]
    }}
    Do NOT add explanations or placeholders.
    """

    try:
        llm_response = get_llm_response(prompt)
        print(f"[Invoice Agent] Raw Azure LLM Response: {llm_response}")

        # Strictly Parse and Ensure Correct Format
        cleaned_response = re.sub(r"```json|```", "", llm_response).strip()
        invoice_details = json.loads(cleaned_response)
        print(f"[Invoice Agent] Parsed Invoice Details: {invoice_details}")

    except (json.JSONDecodeError, KeyError) as e:
        response_message = f"Error parsing invoice details: {str(e)}"
        print(f"[Invoice Agent] {response_message}")
        state["messages"].append({"role": "system", "content": response_message})
        state["next_node"] = "supervisor"
        return state

    # Make the Invoice API Request
    try:
        invoice_api_url = f"http://127.0.0.1:8000/api/invoices/?customer_id={invoice_details['customer_id']}&organization_id={invoice_details['organization_id']}"
        print(f"[Invoice Agent] Sending POST Request to {invoice_api_url}...")

        # Send POST Request
        response = requests.post(
            url=invoice_api_url,
            headers={"Content-Type": "application/json"},
            json=invoice_details['items'],
            timeout=5
        )

        if response.status_code == 201:
            response_message = f"Invoice created successfully. ID={response.json()['detail']}"
        else:
            response_message = f"Failed to create invoice: {response.text}"

    except requests.exceptions.Timeout:
        response_message = "Error: Invoice API request timed out after 10s."

    except requests.exceptions.RequestException as e:
        response_message = f"Error: Invoice API request failed - {str(e)}"

    # Final Response Log
    print(f"[Invoice Agent] Final Response: {response_message}")
    state["messages"].append({"role": "system", "content": response_message})
    state["next_node"] = "supervisor"
    return state
