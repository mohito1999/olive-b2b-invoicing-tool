from langgraph.graph import MessagesState
import requests
import json
from app.llm_setup import get_llm_response

def customer_agent(state: MessagesState) -> MessagesState:
    # Access the content attribute directly
    query = state["messages"][-1].content

    # Parse the query to extract customer details using LLM
    customer_details = parse_customer_details_with_llm(query)

    # Define the API endpoint and headers
    api_endpoint = "http://localhost:8000/api/customers/"
    headers = {"Content-Type": "application/json"}

    try:
        # Make the API call to create a customer
        response = requests.post(api_endpoint, headers=headers, data=json.dumps(customer_details))

        # Check if the request was successful
        if response.status_code == 201:
            response_content = {"role": "system", "content": "Customer created successfully."}
        else:
            response_content = {"role": "system", "content": f"Failed to create customer: {response.text}"}

    except Exception as e:
        response_content = {"role": "system", "content": f"Error creating customer: {str(e)}"}

    # Append the response to the state messages
    state["messages"].append(response_content)
    state["next_node"] = "supervisor"
    return state

def parse_customer_details_with_llm(query: str) -> dict:
    # Define a prompt to instruct the LLM
    prompt = f"Extract the customer details from the following text: {query}\n\n" \
             "Return the details in JSON format with keys: name, company_name, email, phone_number, address."

    # Get the response from the LLM
    response = get_llm_response(prompt)

    # Convert the response to a dictionary
    try:
        customer_details = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("Failed to parse LLM response into JSON.")

    return customer_details

# Example usage
if __name__ == "__main__":
    query = "create a customer with name being Mohit Motwani, company name being Roshni Corporation, email being mohitmotwani1999@gmail.com, phone number being 7019573521 and address being Dubai, UAE"
    customer_details = parse_customer_details_with_llm(query)
    print(customer_details)